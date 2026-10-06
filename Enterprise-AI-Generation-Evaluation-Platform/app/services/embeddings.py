from functools import lru_cache
from sentence_transformers import SentenceTransformer
from app.config import settings

@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(settings.embedding_model)

def embed_texts(texts):
    vectors = get_model().encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return [v.tolist() for v in vectors]
