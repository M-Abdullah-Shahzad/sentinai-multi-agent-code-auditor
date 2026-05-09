from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbeddings:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input):
        if isinstance(input, str):
            embeddings = self.model.encode([input], convert_to_numpy=True, show_progress_bar=False)
            return embeddings[0].tolist()
        embeddings = self.model.encode(input, convert_to_numpy=True, show_progress_bar=False)
        return [embedding.tolist() for embedding in embeddings]
