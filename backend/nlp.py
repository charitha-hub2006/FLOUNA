import re

def extract_preferences(text):
    text = text.lower()
    prefs = {
        "budget": None,
        "delivery_time": None,
        "min_rating": None,
        "cuisine": None,
        "dietary": None
    }
    
    # Budget: matches "under $30", "under 30", "$30 or less", "budget 30"
    budget_match = re.search(r'(?:under|below|max|budget|\$)\s*\$?(\d+(?:\.\d+)?)|\$?(\d+(?:\.\d+)?)\s*(?:dollars|or less)', text)
    if budget_match:
        val = budget_match.group(1) or budget_match.group(2)
        if val:
            prefs["budget"] = float(val)
        
    # Delivery time: matches "40 mins", "40 minutes", "in 40 min"
    time_match = re.search(r'(\d+)\s*(?:min|minute)', text)
    if time_match:
        prefs["delivery_time"] = int(time_match.group(1))
        
    # Rating: matches "4.0 stars", "4 star", "at least 4.5"
    rating_match = re.search(r'(\d(?:\.\d)?)\s*star', text)
    if rating_match:
        prefs["min_rating"] = float(rating_match.group(1))
        
    # Cuisine
    cuisines = ["mexican", "indian", "italian", "american", "japanese", "chinese", "thai", "pizza", "burger"]
    for c in cuisines:
        if c in text:
            prefs["cuisine"] = c
            break
            
    # Dietary
    if "vegan" in text:
        prefs["dietary"] = "vegan"
    elif "vegetarian" in text or "veg" in text:
        prefs["dietary"] = "vegetarian"
        
    return prefs
