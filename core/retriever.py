from .config import Settings
from .indexing import query
from sentence_transformers import CrossEncoder

SET = Settings()

# Load reranker if specified
_reranker = None
if SET.MODEL_RERANK:
    try:
        _reranker = CrossEncoder(SET.MODEL_RERANK)
    except Exception:
        _reranker = None

def retrieve_with_context(query_text: str, top_k: int = None):
    """Retrieve top-k chunks with optional reranking."""
    if top_k is None:
        top_k = SET.TOP_K
    hits = query(query_text, k=top_k * 2 if _reranker else top_k)

    if _reranker:
        pairs = [(query_text, h['text']) for h in hits]
        scores = _reranker.predict(pairs)
        for h, s in zip(hits, scores):
            h['rerank_score'] = float(s)
        hits.sort(key=lambda x: x['rerank_score'], reverse=True)
        hits = hits[:top_k]

    # Build context string
    context_str = "\n\n".join(
        f"[{h['site']}] {h['text']}" for h in hits
    )

    return context_str, hits
