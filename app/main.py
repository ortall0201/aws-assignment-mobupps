from fastapi import FastAPI, Request
from app.routers.health import router as health_router
from app.routers.api_v1 import router as api_v1_router
from app.utils.data_loader import ensure_data_files


app = FastAPI(title="MobUpps – AB Similarity & Predict API", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    """Download data files from Google Drive on startup"""
    ensure_data_files()


@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    # midware קצר ל-correlation id
    response = await call_next(request)
    return response


app.include_router(health_router)
app.include_router(api_v1_router, prefix="/api/v1")