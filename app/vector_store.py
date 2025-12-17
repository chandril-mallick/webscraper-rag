import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

class VectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(384)
        self.texts = []

    def add_texts(self, texts):
        if not texts:
            return

        embeddings = model.encode(texts)
        self.index.add(np.array(embeddings).astype("float32"))
        self.texts.extend(texts)

    def search(self, query, k=5):
        # ✅ SAFETY CHECK
        if len(self.texts) == 0:
            return []

        k = min(k, len(self.texts))  # prevent out of range

        q_emb = model.encode([query])
        _, indices = self.index.search(
            np.array(q_emb).astype("float32"), k
        )

        return [self.texts[i] for i in indices[0] if i < len(self.texts)]
