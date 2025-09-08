# rag.py (Render-friendly)
from dotenv import load_dotenv
load_dotenv()
import os
from typing import List, Dict
import chromadb
from chromadb.utils import embedding_functions

# Load environment variables
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def get_client():
    """
    Create an in-memory Chroma client (no persistence) for Render.
    """
    client = chromadb.Client()
    return client

def create_or_get_collection(name="docs"):
    """
    Always create a fresh collection on Render to avoid schema conflicts.
    """
    client = get_client()
    try:
        # Delete if collection exists
        existing = client.get_collection(name=name, include={"embeddings": False})
        if existing:
            client.delete_collection(name)
    except Exception:
        pass

    # Use OpenAI embeddings if key is present
    if OPENAI_KEY:
        ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=OPENAI_KEY,
            model_name="text-embedding-3-small"
        )
        col = client.create_collection(name=name, embedding_function=ef)
    else:
        col = client.create_collection(name=name)
    return col

def ingest_documents(texts: List[str], metadatas: List[Dict[str, str]], ids: List[str], collection_name="docs"):
    """
    Add documents to a Chroma collection.
    """
    col = create_or_get_collection(collection_name)
    try:
        col.add(documents=texts, metadatas=metadatas, ids=ids)
    except Exception as e:
        print("Chroma ingest failed:", e)

def answer_query(query: str, collection_name="docs", top_k: int = 3):
    """
    Query the collection and return top_k results along with sources.
    Fallback to Atlan docs if no results.
    """
    col = create_or_get_collection(collection_name)
    out = {"answer": "", "sources": []}
    try:
        res = col.query(query_texts=[query], n_results=top_k)
        docs = []
        sources = []

        for docs_for_query in res.get("documents", []):
            for d in docs_for_query:
                if d:
                    docs.append(d)

        for metas_for_query in res.get("metadatas", []):
            for m in metas_for_query:
                if m and isinstance(m, dict) and m.get("source"):
                    sources.append(m.get("source"))

        if docs:
            out["answer"] = "\n\n".join(docs[:top_k])
            out["sources"] = list(dict.fromkeys(sources))
        else:
            # Fallback to Atlan docs
            if any(k in query.lower() for k in ["api", "sdk"]):
                out["answer"] = "You can find details in the Atlan Developer Hub."
                out["sources"] = ["https://developer.atlan.com/"]
            else:
                out["answer"] = "You can find details in Atlan's official documentation."
                out["sources"] = ["https://docs.atlan.com/"]

    except Exception as e:
        out["answer"] = f"Error during retrieval: {e}"

    return out

if __name__ == "__main__":
    docs = ["Short doc: how to add a column in Atlan UI."]
    metas = [{"source": "local-doc-example"}]
    ids = ["doc-1"]
    ingest_documents(docs, metas, ids)
    print(answer_query("how to add a column"))
