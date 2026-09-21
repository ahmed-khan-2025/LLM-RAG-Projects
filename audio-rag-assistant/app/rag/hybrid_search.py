import json
from pathlib import Path

from rank_bm25 import BM25Okapi


class BM25Search:
    def __init__(
        self,
        index_path: str = "data/bm25_index.json",
    ):
        self.index_path = Path(index_path)

        self.documents = []
        self.bm25 = None

        self.load()

    def build(
        self,
        documents: list[dict],
    ):

        existing = {
            item["id"]: item
            for item in self.documents
        }

        for document in documents:
            existing[document["id"]] = document

        self.documents = list(existing.values())

        self._rebuild()
        self.save()

    def _rebuild(self):

        if not self.documents:
            self.bm25 = None
            return

        corpus = [
            item["text"].lower().split()
            for item in self.documents
        ]

        self.bm25 = BM25Okapi(corpus)

    def search(
        self,
        query: str,
        top_k: int = 8,
    ) -> list[dict]:

        if self.bm25 is None:
            return []

        scores = self.bm25.get_scores(
            query.lower().split()
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )

        results = []

        for index in ranked_indices[:top_k]:

            item = dict(
                self.documents[index]
            )

            item["bm25_score"] = float(
                scores[index]
            )

            results.append(item)

        return results

    def save(self):

        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.index_path.write_text(
            json.dumps(
                self.documents,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def load(self):

        if not self.index_path.exists():
            return

        self.documents = json.loads(
            self.index_path.read_text(
                encoding="utf-8"
            )
        )

        self._rebuild()