import os
from backend.nlp import extract_preferences
from backend.normalizer import normalize_providers
from backend.recommendation import rank_restaurants

def test_cheapest_is_not_automatically_best():
    # User wants Indian food
    prefs = {"budget": 50, "delivery_time": 60, "min_rating": 3.0, "cuisine": "indian", "dietary": None}
    restaurants = [
        {"name": "Cheap Indian", "cuisine": "indian", "rating": 3.2, "time": 30, "cost": 10, "menu": "naan", "provider": "A"},
        {"name": "Best Indian", "cuisine": "indian", "rating": 4.9, "time": 25, "cost": 30, "menu": "chicken tikka masala spicy", "provider": "B"}
    ]
    res = rank_restaurants("spicy chicken tikka masala", prefs, restaurants)
    # The higher-rated, higher-relevance restaurant should win over the cheaper option
    assert res["ranked"][0]["name"] == "Best Indian"

def test_missing_preferences_returns_all_matching():
    query = "food"
    prefs = extract_preferences(query) # All preferences set to None
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    restaurants = normalize_providers(data_dir)
    res = rank_restaurants(query, prefs, restaurants)
    assert len(res["ranked"]) == len(restaurants)
