from fastapi import APIRouter, Depends
from time import perf_counter
from app.models.schemas import SimilarRequest, SimilarResponse, PredictRequest, PredictResponse
from app.config import settings
from app.services.ab_test import ABTestController, ABPolicy
from app.services.embeddings import EmbeddingsStore
from app.services.similarity import SimilarityService
from app.services.predictor import PerformancePredictor
from app.utils.logging import get_logger, log_ab_assignment
from app.instrumentation.metrics import record_ab_assignment


router = APIRouter()
logger = get_logger(__name__)


_emb_store = EmbeddingsStore(settings.EMB_V1_PATH, settings.EMB_V2_PATH)
_ab = ABTestController(ABPolicy(v1_weight=settings.AB_SPLIT_V1, sticky=True))
_sim = SimilarityService(_emb_store)


@router.post("/find-similar", response_model=SimilarResponse)
def find_similar(req: SimilarRequest):
    # 1) הפקת embedding לשאילתה
    query_vec = _emb_store.vectorize(req.app.dict())

    # 2) בחירת זרוע A/B
    arm = _ab.pick_arm(req.partner_id, req.app_id)

    # Log and record A/B assignment
    log_ab_assignment(logger, req.partner_id, req.app_id, arm)
    record_ab_assignment("/api/v1/find-similar", arm)

    # 3) שליפת שכנים
    k = req.top_k or settings.DEFAULT_TOP_K
    neighbors = _sim.topk_neighbors(query_vec, k, req.filters, arm)

    logger.info(f"Found {len(neighbors)} neighbors for app_id={req.app_id}")

    return {"neighbors": [n.dict() for n in neighbors], "ab_arm": arm}


@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    t0 = perf_counter()

    logger.info(f"Predicting performance for ab_arm={req.ab_arm}")

    predictor = PerformancePredictor(req.ab_arm)
    pred = predictor.predict(req.app.dict(), req.neighbors)
    latency_ms = int((perf_counter() - t0) * 1000)

    logger.info(f"Prediction complete: score={pred.score}, latency={latency_ms}ms")

    return {"ab_arm": req.ab_arm, "prediction": pred.dict(), "latency_ms": latency_ms}