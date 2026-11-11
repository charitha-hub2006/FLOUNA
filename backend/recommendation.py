from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_restaurants(query, preferences, restaurants):
    if not restaurants:
        return []

    filtered = []
    budget = preferences.get("budget")
    time_limit = preferences.get("delivery_time")
    min_rating = preferences.get("min_rating")

    for r in restaurants:
        if not isinstance(r, dict):
            continue
        if budget is not None and r.get("cost", 0) > budget:
            continue
        if time_limit is not None and r.get("time", 999) > time_limit:
            continue
        if min_rating is not None and r.get("rating", 0) < min_rating:
            continue
        filtered.append(r)

    if not filtered:
        return []

    corpus = []
    for r in filtered:
        items_str = " ".join(r.get("items", [])) if isinstance(r.get("items"), list) else ""
        text = f"{r.get('name', '')} {r.get('cuisine', '')} {items_str}"
        corpus.append(text)

    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([query] + corpus)
        query_vec = tfidf_matrix[0:1]
        doc_vecs = tfidf_matrix[1:]
        sim_scores = cosine_similarity(query_vec, doc_vecs)[0]
    except Exception:
        sim_scores = [0.0] * len(filtered)

    ranked_results = []
    for idx, r in enumerate(filtered):
        text_score = float(sim_scores[idx]) if idx < len(sim_scores) else 0.0
        norm_rating = float(r.get("rating", 0)) / 5.0
        final_score = round((text_score * 0.5 + norm_rating * 0.5) * 100, 1)

        exp_parts = []
        if text_score > 0:
            exp_parts.append(f"matches query '{query}'")
        if budget:
            exp_parts.append(f"stays under your ₹{budget} budget (₹{r.get('cost')})")
        if time_limit:
            exp_parts.append(f"delivers in {r.get('time')} mins")
        if r.get("rating"):
            exp_parts.append(f"has a {r.get('rating')}★ rating")

        explanation = f"Recommended because it {' and '.join(exp_parts)}." if exp_parts else "Good overall choice."

        item_data = dict(r)
        item_data["score"] = final_score
        item_data["explanation"] = explanation
        ranked_results.append(item_data)

    ranked_results.sort(key=lambda x: x["score"], reverse=True)
    return ranked_results
