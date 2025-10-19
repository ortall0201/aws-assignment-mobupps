from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Local file paths
    EMB_V1_PATH: str = "data/mock_embeddings_v1.pkl"
    EMB_V2_PATH: str = "data/mock_embeddings_v2.pkl"
    SAMPLE_APPS_PATH: str = "data/sample_apps.csv"
    HIST_PERF_PATH: str = "data/historical_performance.csv"

    # Google Drive URLs (optional - only needed if files don't exist locally)
    GDRIVE_EMB_V1_URL: str = Field(default="")
    GDRIVE_EMB_V2_URL: str = Field(default="")
    GDRIVE_APPS_URL: str = Field(default="")
    GDRIVE_PERF_URL: str = Field(default="")

    # API settings
    DEFAULT_TOP_K: int = 20
    AB_SPLIT_V1: float = 0.5  # 0..1

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields from .env


settings = Settings()