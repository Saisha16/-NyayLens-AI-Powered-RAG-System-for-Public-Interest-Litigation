from sentence_transformers import SentenceTransformer
import chromadb
import json

model = SentenceTransformer("all-mpnet-base-v2")
client = chromadb.Client()
collection = client.create_collection("legal_docs")

with open("data/legal_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

for chunk in chunks:
    embedding = model.encode(chunk["text"]).tolist()
    collection.add(
        documents=[chunk["text"]],
        ids=[chunk["id"]],
        metadatas=[{"source": chunk["source"]}]
    )

print("Vector DB built successfully")
