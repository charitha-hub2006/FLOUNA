from backend.nlp import extract_preferences

def test_extract_budget():
    p = extract_preferences("I want mexican food under 20")
    assert p["budget"] == 20.0
    assert p["cuisine"] == "mexican"

def test_extract_complex():
    p = extract_preferences("indian food under $30 in 40 mins with 4.0 stars")
    assert p["budget"] == 30.0
    assert p["delivery_time"] == 40
    assert p["min_rating"] == 4.0
    assert p["cuisine"] == "indian"
