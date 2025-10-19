from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uuid
import time
from app.routers.health import router as health_router
from app.routers.api_v1 import router as api_v1_router
from app.utils.data_loader import ensure_data_files
from app.utils.logging import setup_logging, set_correlation_id, get_logger, log_request, log_response
from app.instrumentation.metrics import record_request, get_metrics_summary


app = FastAPI(title="MobUpps – AB Similarity & Predict API", version="1.0.0")
logger = get_logger(__name__)


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    # Setup logging (structured=False for colored console in development)
    setup_logging(level="INFO", structured=False)
    logger.info("Starting MobUpps API...")

    # Download data files from Google Drive on startup
    ensure_data_files()
    logger.info("Data files loaded successfully")


@app.middleware("http")
async def logging_and_metrics_middleware(request: Request, call_next):
    """Middleware for correlation ID tracking, logging, and metrics"""
    # Generate and set correlation ID
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    set_correlation_id(correlation_id)

    # Log incoming request
    log_request(logger, request.method, request.url.path, query_params=str(request.query_params))

    # Track request timing
    start_time = time.perf_counter()

    try:
        # Process request
        response = await call_next(request)

        # Calculate latency
        latency_ms = (time.perf_counter() - start_time) * 1000

        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id

        # Log response
        log_response(logger, response.status_code, latency_ms)

        # Record metrics
        record_request(request.url.path, response.status_code, latency_ms)

        return response

    except Exception as e:
        # Log error
        latency_ms = (time.perf_counter() - start_time) * 1000
        logger.error(f"Request failed: {str(e)}", exc_info=True)

        # Record error metrics
        record_request(request.url.path, 500, latency_ms)

        # Return error response
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "correlation_id": correlation_id},
            headers={"X-Correlation-ID": correlation_id}
        )


@app.get("/metrics")
async def metrics_endpoint():
    """Expose collected metrics"""
    return get_metrics_summary()


app.include_router(health_router)
app.include_router(api_v1_router, prefix="/api/v1")