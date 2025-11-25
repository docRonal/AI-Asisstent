# build_embeddings.py
"""
Берёт тексты в data/raw_texts/*.txt, разбивает на чанки, создаёт эмбеддинги и сохраняет в Chroma.
"""
import os
from sentence_transformers import SentenceTransformer
from utils import read_text_file, split_text, clean_text
from tqdm import tqdm
import chromadb
from chromadb.config import Settings

RAW_DIR = "data/raw_texts"
PERSIST_DIR = "data/chroma_store"

MODEL_NAME_EMBED = "all-MiniLM-L6-v2"  # компактная локальная модель

def gather_docs(raw_dir):
    docs = []
    meta = []
    for fname in os.listdir(raw_dir):
        path = os.path.join(raw_dir, fname)
        text = read_text_file(path)
        text = clean_text(text)
        if not text:
            continue
        chunks = split_text(text, chunk_size=1200, overlap=200)
        for i, c in enumerate(chunks):
            docs.append(c)
            meta.append({"source": path, "chunk": i})
    return docs, meta

def main():
    os.makedirs(PERSIST_DIR, exist_ok=True)
    model = SentenceTransformer(MODEL_NAME_EMBED)
    docs, meta = gather_docs(RAW_DIR)
    print(f"Docs to index: {len(docs)}")
    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=PERSIST_DIR))
    collection = client.get_or_create_collection("docs")
    batch_size = 256
    for i in tqdm(range(0, len(docs), batch_size)):
        batch_docs = docs[i:i+batch_size]
        batch_meta = meta[i:i+batch_size]
        embeddings = model.encode(batch_docs, show_progress_bar=False, convert_to_numpy=True)
        ids = [f"doc_{i+j}" for j in range(len(batch_docs))]
        collection.add(documents=batch_docs, metadatas=batch_meta, ids=ids, embeddings=embeddings.tolist())
    client.persist()
    print("Done, persisted to", PERSIST_DIR)

if __name__ == "__main__":
    main()
