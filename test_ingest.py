from ingest import load_documents, chunk_text

docs = load_documents()
print("Loaded docs:", docs)

chunks = []
for doc in docs:
    chunks.extend(chunk_text(doc))

print("Chunks:", chunks)
