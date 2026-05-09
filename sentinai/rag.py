import json
import os
from typing import List
import chromadb

from .config import CHROMA_DB_DIR, EMBEDDING_MODEL
from .embedder import SentenceTransformerEmbeddings


def _load_references():
    path = os.path.join(os.path.dirname(__file__), "data", "references.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


class ReferenceRetriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.collection = self._ensure_collection()

    def _ensure_collection(self):
        collection_name = "sentinai_references"
        embeddings = SentenceTransformerEmbeddings(EMBEDDING_MODEL)
        try:
            return self.client.get_collection(collection_name)
        except Exception:
            collection = self.client.create_collection(name=collection_name, embedding_function=embeddings)
            refs = _load_references()
            if refs:
                ids, texts, metadatas = [], [], []
                for idx, item in enumerate(refs):
                    ids.append(str(idx))
                    texts.append(item["text"])
                    metadatas.append({"title": item["title"], "source": item["source"]})
                collection.add(ids=ids, documents=texts, metadatas=metadatas)
            return collection

    def retrieve(self, query: str, k: int = 4):
        hits = self.collection.query(query_texts=[query], n_results=k)
        results = []
        for doc, metadata in zip(hits["documents"][0], hits["metadatas"][0]):
            results.append({"title": metadata.get("title", "Reference"), "snippet": doc[:320], "source": metadata.get("source")})
        return results
