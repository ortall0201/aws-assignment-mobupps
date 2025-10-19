from fastapi import APIRouter, Depends
from time import perf_counter
from app.models.schemas import SimilarRequest, SimilarResponse, PredictRequest, PredictResponse
from app.config import settings
from app.services.ab_test import ABTestController, ABPolicy
from app.services.embeddings import EmbeddingsStore
from app.services.similarity import SimilarityService
from app.services.predictor import PerformancePredictor


router = APIRouter()


_emb_store = EmbeddingsStore(settings.EMB_V1_PATH, settings.EMB_V2_PATH)
_ab = ABTestController(ABPolicy(v1_weight=settings.AB_SPLIT_V1, sticky=True))
_sim = SimilarityService(_emb_store)


@router.post("/find-similar", response_model=SimilarResponse)
def find_similar(req: SimilarRequest):
    # 1) הפקת embedding לשאילתה
    query_vec = _emb_store.vectorize(req.app.dict())
    # 2) בחירת זרוע A/B
    arm = _ab.pick_arm(req.partner_id, req.app_id)
    # 3) שליפת שכנים
    k = req.top_k or settings.DEFAULT_TOP_K
    neighbors = _sim.topk_neighbors(query_vec, k, req.filters, arm)
    return {"neighbors": [n.dict() for n in neighbors], "ab_arm": arm}


@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    t0 = perf_counter()
    predictor = PerformancePredictor(req.ab_arm)
    pred = predictor.predict(req.app.dict(), req.neighbors)
    latency_ms = int((perf_counter() - t0) * 1000)
    return {"ab_arm": req.ab_arm, "prediction": pred.dict(), "latency_ms": latency_ms}