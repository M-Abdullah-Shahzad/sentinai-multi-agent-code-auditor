import json
import os

import chromadb

from .config import CHROMA_DB_DIR, EMBEDDING_MODEL
from .embedder import SentenceTransformerEmbeddings


def _load_references():
    path = os.path.join(os.path.dirname(__file__), "data", "references.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, list) else []


class ReferenceRetriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.collection = self._ensure_collection()

    def _ensure_collection(self):
        collection_name = "sentinai_references"
        embeddings = SentenceTransformerEmbeddings(EMBEDDING_MODEL)
        try:
            return self.client.get_collection(
                name=collection_name,
                embedding_function=embeddings,
            )
        except Exception:
            collection = self.client.create_collection(
                name=collection_name,
                embedding_function=embeddings,
            )
            refs = _load_references()
            if refs:
                ids, texts, metadatas = [], [], []
                for idx, item in enumerate(refs):
                    if not isinstance(item, dict) or not item.get("text"):
                        continue
                    ids.append(str(idx))
                    texts.append(str(item["text"]))
                    metadatas.append({
                        "title": str(item.get("title", "Reference")),
                        "source": str(item.get("source", "")),
                    })
                if ids:
                    collection.add(ids=ids, documents=texts, metadatas=metadatas)
            return collection

    def retrieve(self, query: str, k: int = 4):
        if not query or not query.strip():
            return []
        available = self.collection.count()
        if available <= 0:
            return []
        hits = self.collection.query(
            query_texts=[query],
            n_results=min(max(1, int(k)), available),
        )
        documents = (hits.get("documents") or [[]])[0]
        metadatas = (hits.get("metadatas") or [[]])[0]
        results = []
        for doc, metadata in zip(documents, metadatas):
            metadata = metadata or {}
            results.append({
                "title": metadata.get("title", "Reference"),
                "snippet": str(doc)[:320],
                "source": metadata.get("source"),
            })
        return results
