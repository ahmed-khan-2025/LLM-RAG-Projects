from functools import lru_cache
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(MODEL_NAME)

def embed_texts(texts):
    model = get_model()
    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    return [vector.tolist() for vector in vectors]
