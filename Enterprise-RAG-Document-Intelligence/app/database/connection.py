import os
import psycopg
from pgvector.psycopg import register_vector

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://raguser:ragpassword@localhost:5435/ragdb"
)

def get_connection():
    conn = psycopg.connect(DATABASE_URL)
    register_vector(conn)
    return conn

def init_db():
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS document_chunks (
                id SERIAL PRIMARY KEY,
                filename TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding vector(384) NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx
            ON document_chunks
            USING hnsw (embedding vector_cosine_ops)
        """)
        conn.commit()
