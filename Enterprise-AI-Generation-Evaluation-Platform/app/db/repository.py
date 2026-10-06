from app.db.connection import get_connection

def get_prompt(name: str, version: int | None = None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if version is None:
                cur.execute("SELECT version, system_instruction FROM prompt_versions WHERE name=%s AND active=TRUE ORDER BY version DESC LIMIT 1", (name,))
            else:
                cur.execute("SELECT version, system_instruction FROM prompt_versions WHERE name=%s AND version=%s", (name, version))
            row = cur.fetchone()
    return {"version": row[0], "system_instruction": row[1]} if row else None

def save_prompt(name, version, instruction, active=False):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if active:
                cur.execute("UPDATE prompt_versions SET active=FALSE WHERE name=%s", (name,))
            cur.execute("""
                INSERT INTO prompt_versions(name, version, system_instruction, active)
                VALUES (%s,%s,%s,%s)
                ON CONFLICT (name, version) DO UPDATE SET system_instruction=EXCLUDED.system_instruction, active=EXCLUDED.active
            """, (name, version, instruction, active))
        conn.commit()

def get_brand(brand_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT brand_name,tone,forbidden_terms,required_terms,safety_rules FROM brand_configs WHERE brand_name=%s", (brand_name,))
            row = cur.fetchone()
    if not row:
        return None
    return {"brand_name": row[0], "tone": row[1], "forbidden_terms": row[2] or [], "required_terms": row[3] or [], "safety_rules": row[4] or []}

def save_brand(data):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO brand_configs(brand_name,tone,forbidden_terms,required_terms,safety_rules)
            VALUES (%s,%s,%s,%s,%s)
            ON CONFLICT (brand_name) DO UPDATE SET tone=EXCLUDED.tone, forbidden_terms=EXCLUDED.forbidden_terms, required_terms=EXCLUDED.required_terms, safety_rules=EXCLUDED.safety_rules
            """, (data["brand_name"],data["tone"],data.get("forbidden_terms",[]),data.get("required_terms",[]),data.get("safety_rules",[])))
        conn.commit()

def insert_chunks(brand_name, filename, chunks, embeddings):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany("INSERT INTO document_chunks(brand_name,filename,content,embedding) VALUES (%s,%s,%s,%s::vector)", [(brand_name,filename,c,"["+",".join(map(str,e))+"]") for c,e in zip(chunks,embeddings)])
        conn.commit()
    return len(chunks)

def search_chunks(brand_name, query_embedding, top_k=5):
    vector_string = "[" + ",".join(map(str, query_embedding)) + "]"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT id,filename,content,1-(embedding <=> %s::vector) AS similarity
            FROM document_chunks WHERE brand_name=%s
            ORDER BY embedding <=> %s::vector LIMIT %s
            """, (vector_string,brand_name,vector_string,top_k))
            rows=cur.fetchall()
    return [{"id":r[0],"filename":r[1],"content":r[2],"similarity":float(r[3])} for r in rows]

def save_event(event):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO generation_events(request_id,brand_name,model,provider,prompt_version,input_tokens,output_tokens,estimated_cost_usd,latency_ms,quality_score,safety_pass,groundedness_score)
            VALUES (%(request_id)s,%(brand_name)s,%(model)s,%(provider)s,%(prompt_version)s,%(input_tokens)s,%(output_tokens)s,%(estimated_cost_usd)s,%(latency_ms)s,%(quality_score)s,%(safety_pass)s,%(groundedness_score)s)
            """, event)
        conn.commit()
