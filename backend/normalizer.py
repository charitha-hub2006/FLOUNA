def extract_items_list(raw_items):
    """Safely extracts item names whether they are strings or dicts."""
    extracted = []
    if not isinstance(raw_items, list):
        return extracted
    for item in raw_items:
        if isinstance(item, str):
            extracted.append(item)
        elif isinstance(item, dict):
            extracted.append(item.get("name") or item.get("title") or item.get("dish_name") or "")
    return extracted

def normalize_item(provider_name, item):
    """
    Converts raw items from Provider A, B, or C into a unified schema.
    Handles fallbacks for names, titles, cuisines, and price keys across provider formats.
    """
    if not isinstance(item, dict):
        return None

    # Flexible name fallback logic
    name = item.get("restaurant_name") or item.get("name") or item.get("title") or item.get("restaurant") or "Unknown"

    if provider_name == "Provider A":
        return {
            "name": name,
            "cuisine": item.get("cuisine_type") or item.get("cuisine") or "General",
            "cost": float(item.get("avg_price", 0)),
            "time": int(item.get("est_delivery_minutes", 30)),
            "rating": float(item.get("rating", 0.0)),
            "provider": provider_name,
            "items": extract_items_list(item.get("popular_items", []))
        }
    elif provider_name == "Provider B":
        cost_val = item.get("cost_for_two")
        cost = float(cost_val / 2 if cost_val else item.get("price", 0))
        return {
            "name": name,
            "cuisine": item.get("category") or item.get("cuisine") or "General",
            "cost": cost,
            "time": int(item.get("delivery_time", 30)),
            "rating": float(item.get("stars") or item.get("rating") or 0.0),
            "provider": provider_name,
            "items": extract_items_list(item.get("menu", []))
        }
    elif provider_name == "Provider C":
        tags = item.get("tags", [])
        cuisine = tags[0] if isinstance(tags, list) and len(tags) > 0 else (item.get("cuisine") or "General")
        cost = float(item.get("price_usd") or item.get("cost") or item.get("price") or 0)
        time_val = item.get("prep_plus_delivery_mins") or item.get("delivery_time") or item.get("time") or 30
        return {
            "name": name,
            "cuisine": cuisine,
            "cost": cost,
            "time": int(time_val),
            "rating": float(item.get("score") or item.get("rating") or 0.0),
            "provider": provider_name,
            "items": extract_items_list(item.get("dishes") or item.get("items") or [])
        }
    else:
        return {
            "name": name,
            "cuisine": item.get("cuisine", "General"),
            "cost": float(item.get("cost", 0)),
            "time": int(item.get("time", 30)),
            "rating": float(item.get("rating", 0.0)),
            "provider": provider_name,
            "items": []
        }

def normalize_and_deduplicate(raw_provider_data):
    """
    Aggregates provider data, normalizes formats, and deduplicates based on restaurant name.
    """
    all_normalized = []
    
    for entry in raw_provider_data:
        if not isinstance(entry, dict):
            continue
        provider_name = entry.get("provider", "Unknown")
        items = entry.get("data", [])
        if isinstance(items, list):
            for item in items:
                normalized = normalize_item(provider_name, item)
                if normalized and normalized["name"] != "Unknown":
                    all_normalized.append(normalized)

    # Deduplication: Key by lowercase name, retain highest rated
    dedup_dict = {}
    for r in all_normalized:
        key = r["name"].strip().lower()
        if key not in dedup_dict:
            dedup_dict[key] = r
        else:
            if r["rating"] > dedup_dict[key]["rating"]:
                dedup_dict[key] = r

    return list(dedup_dict.values())
