from app.services.predictor import PerformancePredictor
from app.models.schemas import Neighbor


def test_predict_output():
    p = PerformancePredictor("v2")
    neighbors = [Neighbor(app_id="x", similarity=0.9)]
    out = p.predict({"category":"Health & Fitness", "features":["sharing"]}, neighbors)
    assert 0.5 <= out.score <= 0.9
    assert isinstance(out.segments, list)