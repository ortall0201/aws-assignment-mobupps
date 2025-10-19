from fastapi import APIRouter, Depends, HTTPException, Request
from time import perf_counter
from app.models.schemas import SimilarRequest, SimilarResponse, PredictRequest, PredictResponse
from app.config import settings
from app.services.ab_test import ABTestController, ABPolicy
from app.services.embeddings import EmbeddingsStore
from app.services.similarity import SimilarityService
from app.services.predictor import PerformancePredictor
from app.utils.logging import get_logger, log_ab_assignment
from app.instrumentation.metrics import record_ab_assignment, record_request_latency


router = APIRouter()
logger = get_logger(__name__)


_emb_store = EmbeddingsStore(settings.EMB_V1_PATH, settings.EMB_V2_PATH)
_ab = ABTestController(ABPolicy(v1_weight=settings.AB_SPLIT_V1, sticky=True))
_sim = SimilarityService(_emb_store)


@router.post("/find-similar", response_model=SimilarResponse)
def find_similar(req: SimilarRequest):
    """
    Find similar apps using embeddings with A/B testing.

    Raises:
        HTTPException: 400 for invalid input, 500 for server errors
    """
    t0 = perf_counter()

    try:
        # 1) בחירת זרוע A/B (first, to determine which model to use)
        arm = _ab.pick_arm(req.partner_id, req.app_id)

        # 2) הפקת embedding לשאילתה (using the selected arm's model)
        query_vec = _emb_store.vectorize(req.app.dict(), arm)

        if not query_vec or len(query_vec) == 0:
            logger.error(f"Failed to generate embedding for app_id={req.app_id}")
            raise HTTPException(status_code=500, detail="Failed to generate embedding vector")

        # Log and record A/B assignment
        log_ab_assignment(logger, req.partner_id, req.app_id, arm)
        record_ab_assignment("/api/v1/find-similar", arm)

        # 3) שליפת שכנים
        k = req.top_k or settings.DEFAULT_TOP_K
        if k <= 0 or k > 100:
            raise HTTPException(status_code=400, detail="top_k must be between 1 and 100")

        neighbors = _sim.topk_neighbors(query_vec, k, req.filters, arm)

        latency_ms = int((perf_counter() - t0) * 1000)
        record_request_latency("/api/v1/find-similar", latency_ms)

        logger.info(f"Found {len(neighbors)} neighbors for app_id={req.app_id}, latency={latency_ms}ms")

        return {"neighbors": [n.dict() for n in neighbors], "ab_arm": arm}

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in find_similar: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in find_similar: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during similarity search")


@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest, request: Request):
    """
    Predict performance based on similar apps using cached performance data.

    Raises:
        HTTPException: 400 for invalid input, 500 for server errors
    """
    t0 = perf_counter()

    try:
        logger.info(f"Predicting performance for ab_arm={req.ab_arm}")

        if not req.neighbors or len(req.neighbors) == 0:
            raise HTTPException(status_code=400, detail="At least one neighbor is required for prediction")

        if req.ab_arm not in ["v1", "v2"]:
            raise HTTPException(status_code=400, detail="ab_arm must be 'v1' or 'v2'")

        # Use cached performance data from app startup
        cached_data = getattr(request.app.state, 'performance_data_cache', None)
        predictor = PerformancePredictor(req.ab_arm, performance_data=cached_data)
        pred = predictor.predict(req.app.dict(), req.neighbors)
        latency_ms = int((perf_counter() - t0) * 1000)

        record_request_latency("/api/v1/predict", latency_ms)

        logger.info(f"Prediction complete: score={pred.score}, latency={latency_ms}ms")

        return {"ab_arm": req.ab_arm, "prediction": pred.dict(), "latency_ms": latency_ms}

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in predict: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in predict: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during performance prediction")