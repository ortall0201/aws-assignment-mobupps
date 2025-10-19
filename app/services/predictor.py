from typing import List
from app.models.schemas import Neighbor, Prediction


class PerformancePredictor:
    def __init__(self, arm: str):
        self.arm = arm
        # דמו: אפשר לטעון כאן מודל אמיתי (pickle/onnx). כרגע נשתמש בהיוריסטיקה.

    def predict(self, app: dict, neighbors: List[Neighbor]) -> Prediction:
        base = 0.5
        boost = min(0.4, sum(n.similarity for n in neighbors[:5]) / 5 * 0.4)
        score = base + boost
        segments = self._infer_segments(app, neighbors)
        return Prediction(score=float(round(score, 3)), segments=segments)

    def _infer_segments(self, app: dict, neighbors: List[Neighbor]):
        # דמו: פילוח לפי קטגוריה/תכונות אם קיימות
        segs = set()
        cat = (app.get("category") or "").lower()
        if "game" in cat or "Games" in cat:
            segs.add("gamers")
        if "fitness" in cat:
            segs.add("fitness_lovers")
        feats = set((app.get("features") or []))
        if "sharing" in feats:
            segs.add("social")
        if not segs:
            segs.add("tech-savvy")
        return sorted(list(segs))