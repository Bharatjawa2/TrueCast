import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from .config import Settings

SET = Settings()

# Initialize Chroma persistent client & collection
_client = chromadb.PersistentClient(
    path=SET.VECTOR_DIR,
    settings=ChromaSettings(anonymized_telemetry=False)
)
_collection = _client.get_or_create_collection(
    "news",
    metadata={"hnsw:space": "cosine"}
)

# Load embedding model
_model = SentenceTransformer(SET.MODEL_EMBED)

def _chunk(text, max_tokens=700, overlap=120):
    """Split text into overlapping chunks."""
    words = text.split()
    step = max_tokens - overlap
    for i in range(0, len(words), step):
        chunk = ' '.join(words[i:i + max_tokens])
        if len(chunk) > 50:
            yield chunk

def embed_and_add(article: dict):
    """Embed and add article chunks to Chroma collection."""
    chunks = list(_chunk(article['text']))
    if not chunks:
        return
    embs = _model.encode(chunks, normalize_embeddings=True).tolist()
    ids = [f"{article['id']}_{i}" for i in range(len(chunks))]
    metas = [{
        "url": article['url'],
        "site": article['site'],
        "title": article['title'],
        "published": article['published'],
        "chunk_id": i
    } for i in range(len(chunks))]
    _collection.add(
        ids=ids,
        embeddings=embs,
        metadatas=metas,
        documents=chunks
    )

def query(q: str, k: int = 8):
    """Query the Chroma collection and return top-k hits."""
    q_emb = _model.encode([q], normalize_embeddings=True).tolist()[0]
    res = _collection.query(query_embeddings=[q_emb], n_results=k)
    hits = []
    for i in range(len(res['ids'][0])):
        hits.append({
            'id': res['ids'][0][i],
            'text': res['documents'][0][i],
            'score': float(res['distances'][0][i]),
            **res['metadatas'][0][i]
        })
    return hits
