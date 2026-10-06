import psycopg
from pgvector.psycopg import register_vector
from app.config import settings

def get_connection():
    conn = psycopg.connect(settings.database_url)
    register_vector(conn)
    return conn

def init_db():
    with psycopg.connect(settings.database_url) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS prompt_versions (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            version INTEGER NOT NULL,
            system_instruction TEXT NOT NULL,
            active BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE(name, version)
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS brand_configs (
            id SERIAL PRIMARY KEY,
            brand_name TEXT UNIQUE NOT NULL,
            tone TEXT NOT NULL,
            forbidden_terms TEXT[] DEFAULT '{}',
            required_terms TEXT[] DEFAULT '{}',
            safety_rules TEXT[] DEFAULT '{}',
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS brand_assets (
            id SERIAL PRIMARY KEY,
            brand_name TEXT NOT NULL,
            filename TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            metadata JSONB DEFAULT '{}'::jsonb,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            brand_name TEXT NOT NULL,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding vector(384) NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
        """)
        conn.execute("""
        CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx
        ON document_chunks USING hnsw (embedding vector_cosine_ops)
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS generation_events (
            id BIGSERIAL PRIMARY KEY,
            request_id TEXT NOT NULL,
            brand_name TEXT,
            model TEXT NOT NULL,
            provider TEXT NOT NULL,
            prompt_version INTEGER NOT NULL,
            input_tokens INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            estimated_cost_usd DOUBLE PRECISION DEFAULT 0,
            latency_ms DOUBLE PRECISION NOT NULL,
            quality_score DOUBLE PRECISION,
            safety_pass BOOLEAN,
            groundedness_score DOUBLE PRECISION,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
        """)
        conn.execute("""
        INSERT INTO prompt_versions(name, version, system_instruction, active)
        VALUES ('brand-generation', 1,
        'You are a careful brand content assistant. Follow the supplied brand rules. Use retrieved context when provided. Never invent unsupported facts.', TRUE)
        ON CONFLICT (name, version) DO NOTHING
        """)
        conn.commit()
