from app.services.embeddings import EmbeddingsStore
from app.services.similarity import SimilarityService


# לצורך בדיקה, ניצור embedding index דמה בזיכרון


def test_topk_neighbors_smoke(tmp_path, monkeypatch):
    store = EmbeddingsStore("data/mock_embeddings_v1.pkl", "data/mock_embeddings_v2.pkl")
    # monkeypatch: הזרקה של אינדקס דמה
    fake_index = {f"app_{i}": {"vec": [i*0.01]*64, "meta": {"category": "Games"}} for i in range(100)}
    store._v1 = fake_index
    store._v2 = fake_index
    sim = SimilarityService(store)
    q = [0.5]*64
    res = sim.topk_neighbors(q, 10, {"category":["Games"]}, "v1")
    assert len(res) == 10