# ingest.py
from pathlib import Path
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib import robotparser
from dotenv import load_dotenv
import os

load_dotenv()

DATA_DIR = Path("data")
DOCS_DIR = DATA_DIR / "docs"
SAMPLE_FILE = DATA_DIR / "sample_tickets.jsonl"

def load_sample_tickets(path: Path = SAMPLE_FILE):
    """load JSONL tickets"""
    tickets = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tickets.append(json.loads(line))
    return tickets

def is_allowed_by_robots(url: str) -> bool:
    parsed = requests.utils.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except:
        print(f"Warning: couldn't read robots.txt at {robots_url}.")
        return True
    return rp.can_fetch("*", url)

def fetch_and_save(url: str, out_dir: Path = DOCS_DIR, rate_limit: float = 1.0):
    """fetch one page, save as plain text into data/docs"""
    out_dir.mkdir(parents=True, exist_ok=True)
    if not is_allowed_by_robots(url):
        raise PermissionError(f"Fetch blocked by robots.txt: {url}")
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    main = soup.find("main") or soup.find("article") or soup.body
    text = (main.get_text(separator="\n", strip=True)) if main else soup.get_text("\n", strip=True)
    safe = url.replace("://", "_").replace("/", "_")[:200]
    fname = out_dir / (safe + ".txt")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(text)
    time.sleep(rate_limit)
    return str(fname)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--list", action="store_true", help="List loaded tickets")
    p.add_argument("--fetch", nargs="+", help="URLs to fetch and save")
    args = p.parse_args()
    if args.list:
        ts = load_sample_tickets()
        print(f"Loaded {len(ts)} tickets.")
    if args.fetch:
        for u in args.fetch:
            try:
                out = fetch_and_save(u)
                print("Saved:", out)
            except Exception as e:
                print("Error fetching", u, ":", e)
