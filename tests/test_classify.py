# tests/test_classify.py
from classify import classify_ticket

def test_classify_returns_keys():
    txt = "How do I add a new column in Atlan? Need steps."
    r = classify_ticket(txt)
    assert isinstance(r, dict)
    assert "topic" in r and "sentiment" in r and "priority" in r

def test_priority_detection_p0():
    txt = "Production is down, 500 errors everywhere, urgent!"
    r = classify_ticket(txt)
    assert r["priority"] == "P0"
