from typing import List, Dict, Any
from app.models.schemas import Neighbor


class SimilarityService:
    def __init__(self, embeddings_store):
        self.embeddings_store = embeddings_store

    def topk_neighbors(self, query_vec: list[float], k: int, filters: Dict[str, List[str]] | None, arm: str) -> List[Neighbor]:
        # דמו: נשלוף מהמפה של embedding לפי arm. נניח שהיא מכילה {app_id: vector, meta: {...}}
        index = self.embeddings_store.get_by_arm(arm)
        # compute cosine sim בצורה נאיבית (לצורך דמו)
        from math import sqrt
        def cos(a,b):
            dot = sum(x*y for x,y in zip(a,b))
            na = sqrt(sum(x*x for x in a))
            nb = sqrt(sum(y*y for y in b))
            return dot / (na*nb + 1e-9)

        items = []
        for app_id, rec in index.items():
            vec = rec["vec"]
            meta = rec.get("meta", {})
            if filters:
                ok = all(str(meta.get(k2)) in set(v2) for k2, v2 in filters.items() if v2)
                if not ok:
                    continue
            sim = cos(query_vec, vec)
            items.append((app_id, sim))
        items.sort(key=lambda t: t[1], reverse=True)
        return [Neighbor(app_id=a, similarity=s) for a,s in items[:k]]