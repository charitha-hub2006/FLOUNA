import os
from backend.normalizer import normalize_providers

def test_normalization():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    res = normalize_providers(data_dir)
    assert len(res) == 4 # Burger Joint deduplicated
    
    burger_joint = next(r for r in res if r["name"] == "Burger Joint")
    assert burger_joint["rating"] == 4.0 # Kept higher rating
