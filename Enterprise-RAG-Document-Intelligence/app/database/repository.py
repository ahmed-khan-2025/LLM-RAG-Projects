from app.database.connection import get_connection


def insert_chunks(filename, chunks, embeddings):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO document_chunks (filename, content, embedding)
                VALUES (%s, %s, %s::vector)
                """,
                [
                    (
                        filename,
                        chunk,
                        "[" + ",".join(map(str, embedding)) + "]"
                    )
                    for chunk, embedding in zip(chunks, embeddings)
                ]
            )

        conn.commit()

    return len(chunks)


def search_chunks(query_embedding, top_k=5):
    vector_string = "[" + ",".join(map(str, query_embedding)) + "]"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    filename,
                    content,
                    1 - (embedding <=> %s::vector) AS similarity
                FROM document_chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (
                    vector_string,
                    vector_string,
                    top_k
                )
            )

            rows = cur.fetchall()

    return [
        {
            "id": row[0],
            "filename": row[1],
            "content": row[2],
            "similarity": float(row[3])
        }
        for row in rows
    ]