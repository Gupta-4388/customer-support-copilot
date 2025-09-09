# rag.py
from dotenv import load_dotenv
load_dotenv()
import os
from typing import List, Dict
import chromadb

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")


def get_client():
    """
    Create a persistent Chroma client.
    """
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client


def create_or_get_collection(name="docs"):
    """
    Retrieve an existing collection or create a new one.
    If OPENAI_KEY is set, use OpenAI embeddings.
    """
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
    """
    Add documents to a Chroma collection.
    """
    col = create_or_get_collection(collection_name)
    try:
        col.add(documents=texts, metadatas=metadatas, ids=ids)
        col.persist()
    except Exception as e:
        print("Chroma ingest failed:", e)


def answer_query(query: str, collection_name="docs", top_k: int = 3):
    """
    Query the collection and return top_k results along with sources.
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

        out["answer"] = "\n\n".join(docs[:top_k]) if docs else "No relevant docs found."
        out["sources"] = list(dict.fromkeys(sources))
    except Exception as e:
        out["answer"] = f"Error during retrieval: {e}"

    return out


if __name__ == "__main__":
    # Quick local test
    docs = ["Short doc: how to add a column in Atlan UI."]
    metas = [{"source": "local-doc-example"}]
    ids = ["doc-1"]

    ingest_documents(docs, metas, ids)
    print(answer_query("how to add a column"))
