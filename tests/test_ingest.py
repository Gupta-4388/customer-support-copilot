# tests/test_ingest.py
from ingest import load_sample_tickets

def test_load_sample_count():
    ts = load_sample_tickets()
    assert isinstance(ts, list)
    assert len(ts) == 30
    assert all("id" in t and "body" in t for t in ts)
