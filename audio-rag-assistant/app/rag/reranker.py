from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(
        self,
        model_name: str = (
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        ),
    ):
        self.model = CrossEncoder(
            model_name
        )

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 5,
    ) -> list[dict]:

        if not documents:
            return []

        pairs = [
            (query, document["text"])
            for document in documents
        ]

        scores = self.model.predict(
            pairs
        )

        results = []

        for document, score in zip(
            documents,
            scores,
        ):
            item = dict(document)

            item["rerank_score"] = float(
                score
            )

            results.append(item)

        results.sort(
            key=lambda item: item["rerank_score"],
            reverse=True,
        )

        return results[:top_k]