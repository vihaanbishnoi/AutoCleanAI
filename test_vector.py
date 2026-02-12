from ingest import load_documents, chunk_text
from vector_store import VectorStore

docs = load_documents()
all_chunks = []

for doc in docs:
    all_chunks.extend(chunk_text(doc))

vs = VectorStore()
vs.build(all_chunks)

results = vs.search("machine learning")

print("Search Results:")
for r in results:
    print(r)
