from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class AppMeta(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    region: Optional[str] = None
    pricing: Optional[str] = None
    features: Optional[List[str]] = None


class SimilarRequest(BaseModel):
    app: AppMeta
    filters: Optional[Dict[str, List[str]]] = None
    top_k: Optional[int] = Field(default=None, ge=1, le=100)
    partner_id: Optional[str] = None
    app_id: Optional[str] = None


class Neighbor(BaseModel):
    app_id: str
    similarity: float
    app_name: Optional[str] = None
    category: Optional[str] = None


class SimilarResponse(BaseModel):
    neighbors: List[Neighbor]
    ab_arm: str


class PredictRequest(BaseModel):
    app: AppMeta
    neighbors: List[Neighbor]
    ab_arm: str


class Prediction(BaseModel):
    score: float
    segments: List[str]


class PredictResponse(BaseModel):
    ab_arm: str
    prediction: Prediction
    latency_ms: int