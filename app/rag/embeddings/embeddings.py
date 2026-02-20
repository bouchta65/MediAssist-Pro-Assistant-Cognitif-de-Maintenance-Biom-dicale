import json
import chromadb
from sentence_transformers import SentenceTransformer
import mlflow

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("Embeddings")

DATA_DIR = "data"
DB_DIR = "data/chroma_db"
MODEL_NAME = "intfloat/multilingual-e5-base"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def create_embeddings():
    model = SentenceTransformer(MODEL_NAME)
    client = chromadb.PersistentClient(path=DB_DIR)
    
    try:
        client.delete_collection("mediassist")
    except:
        pass
    
    collection = client.create_collection(name="mediassist", metadata={"hnsw:space": "cosine"})
    
    text_chunks = load_json(f"{DATA_DIR}/chunks.json")
    table_chunks = load_json(f"{DATA_DIR}/tables_chunks.json")
    
    docs, ids, metas = [], [], []
    
    for c in text_chunks:
        if c.get("content", "").strip():
            docs.append(c["content"])
            ids.append(f"text_{c['chunk_id']}")
            metas.append({"type": "text", "title": c.get("title", ""), "page": c.get("page", 0)})
    
    for c in table_chunks:
        if c.get("content", "").strip():
            docs.append(c["content"])
            ids.append(c["id"])
            metas.append({"type": c.get("type", "table"), "section": c.get("section", "")})
    
    print(f"Creating embeddings for {len(docs)} chunks...")

    with mlflow.start_run(run_name="embeddings"):

        mlflow.log_param("embedding_model", MODEL_NAME)
        mlflow.log_param("num_chunks", len(docs))
        
        embeddings = model.encode(docs, show_progress_bar=True)
        
        for i, emb in enumerate(embeddings[:5]):
            mlflow.log_text(str(emb.tolist()), f"sample_embedding_{i+1}.txt")
        
        collection.add(documents=docs, embeddings=embeddings.tolist(), ids=ids, metadatas=metas)
        
        mlflow.log_param("num_text_chunks", len(text_chunks))
        mlflow.log_param("num_table_chunks", len(table_chunks))

    print(f"Done. Stored {len(docs)} embeddings in ChromaDB")

create_embeddings()
