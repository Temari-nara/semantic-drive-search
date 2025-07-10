# search_service/embedding/local_embedder.py

from sentence_transformers import SentenceTransformer

class LocalEmbedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list:
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: list) -> list:
        return self.model.encode(texts).tolist()
