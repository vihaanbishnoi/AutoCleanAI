import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


class VectorStore:
    def __init__(self):
        self.index = None
        self.text_chunks = []

    def build(self, chunks):
        if not chunks:
            return

        embeddings = model.encode(chunks)
        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        self.text_chunks = chunks

    def search(self, query, k=3):
        if self.index is None:
            return []

        query_embedding = model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        D, I = self.index.search(query_embedding, k)

        results = []
        for idx in I[0]:
            if idx < len(self.text_chunks):
                results.append(self.text_chunks[idx])

        return results
