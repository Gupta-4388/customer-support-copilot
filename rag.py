from dotenv import load_dotenv
load_dotenv()
import os
from typing import List, Dict
import chromadb

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")

# Pre-defined topic-based answers
TOPIC_ANSWERS = {
    "Product": "You can find details in Atlan's official documentation.",
    "API/SDK": "Refer to Atlan Developer Hub for API/SDK details.",
    "Best practices": "Check out Atlan's best practices guide.",
    "How-to": "Follow the how-to guides available in Atlan documentation.",
    "SSO": "Refer to Atlan SSO setup guides for instructions."
}

# Topic-based sources (deterministic URLs)
TOPIC_SOURCES = {
    "Product": "https://docs.atlan.com/",
    "API/SDK": "https://developer.atlan.com/",
    "Best practices": "https://docs.atlan.com/best-practices/",
    "How-to": "https://docs.atlan.com/",
    "SSO": "https://docs.atlan.com/sso/"
}

def get_client():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client

def create_or_get_collection(name="docs"):
    client = get_client()
    try:
        col = client.get_collection(name)
    except Exception:
        if OPENAI_KEY:
            from chromadb.utils import embedding_functions
            ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=OPENAI_KEY,
                model_name="text-embedding-3-small"
            )
            col = client.create_collection(name=name, embedding_function=ef)
        else:
            col = client.create_collection(name=name)
    return col

def ingest_documents(texts: List[str], metadatas: List[Dict[str, str]], ids: List[str], collection_name="docs"):
    col = create_or_get_collection(collection_name)
    try:
        col.add(documents=texts, metadatas=metadatas, ids=ids)
        col.persist()
    except Exception as e:
        print("Chroma ingest failed:", e)

def answer_query(query: str, collection_name="docs", top_k: int = 3):
    col = create_or_get_collection(collection_name)
    out = {"answer": "", "source": None}  # only one source
    try:
        res = col.query(query_texts=[query], n_results=top_k)
        docs = []
        source = None

        for docs_for_query in res.get("documents", []):
            for d in docs_for_query:
                if d:
                    docs.append(d)

        # Take the first available source
        for metas_for_query in res.get("metadatas", []):
            for m in metas_for_query:
                if m and isinstance(m, dict) and m.get("source"):
                    source = m.get("source")
                    break
            if source:
                break

        out["answer"] = "\n\n".join(docs[:top_k]) if docs else "No relevant docs found."
        out["source"] = source

    except Exception as e:
        out["answer"] = f"Error during retrieval: {e}"
        out["source"] = None

    return out


if __name__ == "__main__":
    # Example ingestion
    docs = [
        "Atlan data catalog features overview",
        "Atlan developer API and SDK guide"
    ]
    metas = [
        {"source": "https://docs.atlan.com/"},
        {"source": "https://developer.atlan.com/"}
    ]
    ids = ["doc-1", "doc-2"]

    ingest_documents(docs, metas, ids)
    print(answer_query("how to use Atlan API or find features"))
