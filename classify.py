# classify.py
import os
import json
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

TOPICS = ["How-to", "Product", "Connector", "Lineage", "API/SDK", "SSO", "Glossary", "Best practices", "Sensitive data"]
SENTIMENTS = ["Frustrated", "Curious", "Angry", "Neutral"]
PRIORITIES = ["P0", "P1", "P2"]

def _heuristic_classify(text: str):
    t = text.lower()
    # topic
    topic = "Product"
    if any(k in t for k in ["how do", "how to", "how can i", "steps", "add a new", "tutorial"]):
        topic = "How-to"
    if any(k in t for k in ["connector", "snowflake", "fivetran", "dbt", "tableau", "connector failed", "crawl"]):
        topic = "Connector"
    if "lineage" in t:
        topic = "Lineage"
    if "api" in t or "endpoint" in t or "sdk" in t or "requests" in t:
        topic = "API/SDK"
    if "sso" in t or "okta" in t or "saml" in t:
        topic = "SSO"
    if "glossary" in t:
        topic = "Glossary"
    if "best practice" in t or "best practices" in t or "catalog hygiene" in t:
        topic = "Best practices"
    if "sensitive" in t or "pii" in t or "personal data" in t:
        topic = "Sensitive data"
    # sentiment
    if any(k in t for k in ["infuriating", "angry", "outrage", "unacceptable"]):
        sentiment = "Angry"
    elif any(k in t for k in ["frustrated", "urgent", "blocked", "please help", "need urgent", "can't", "cannot", "urgent"]):
        sentiment = "Frustrated"
    elif any(k in t for k in ["curious", "wonder", "how many", "what is", "interested"]):
        sentiment = "Curious"
    else:
        sentiment = "Neutral"
    # priority
    if any(k in t for k in ["urgent", "production", "p0", "p1", "down", "not working", "500", "401", "critical", "asap"]):
        pr = "P0"
    elif any(k in t for k in ["soon", "p1", "impact", "error", "fail"]):
        pr = "P1"
    else:
        pr = "P2"
    return {"topic": topic, "sentiment": sentiment, "priority": pr, "confidence": 0.6}

def classify_ticket(text: str):
    """Try OpenAI if key exists, otherwise heuristic"""
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY
            prompt = f"""
You are a classifier. Output only JSON with keys: topic, sentiment, priority, confidence.
Allowed topics: {TOPICS}
Allowed sentiment: {SENTIMENTS}
Allowed priority: {PRIORITIES}
Text: '''{text}'''
"""
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}],
                temperature=0.0,
                max_tokens=200,
            )
            raw = resp.choices[0].message.content.strip()
            try:
                return json.loads(raw)
            except:
                import re
                m = re.search(r"\{.*\}", raw, re.S)
                if m:
                    return json.loads(m.group(0))
        except Exception:
            # short fallback
            return _heuristic_classify(text)
    else:
        return _heuristic_classify(text)
