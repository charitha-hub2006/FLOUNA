import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp import extract_preferences
from normalizer import normalize_and_deduplicate
from recommendation import rank_restaurants

app = Flask(__name__)
CORS(app)

def load_all_providers():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    provider_files = [
        ("Provider A", "provider_a.json"),
        ("Provider B", "provider_b.json"),
        ("Provider C", "provider_c.json"),
    ]
    
    raw_data = []
    for provider_name, filename in provider_files:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                raw_data.append({
                    "provider": provider_name,
                    "data": json.load(f)
                })
    return raw_data

@app.route("/api/recommend", methods=["POST"])
def recommend():
    try:
        body = request.get_json() or {}
        user_query = body.get("query", "")

        preferences = extract_preferences(user_query)
        raw_providers = load_all_providers()
        normalized_data = normalize_and_deduplicate(raw_providers)
        ranked_data = rank_restaurants(user_query, preferences, normalized_data)

        return jsonify({
            "status": "success",
            "query": user_query,
            "extracted_preferences": preferences,
            "results": {
                "ranked": ranked_data
            }
        })
    except Exception as e:
        print(f"Error processing recommendation: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
