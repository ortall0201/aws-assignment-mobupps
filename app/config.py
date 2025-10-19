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

    # CORS settings (can be overridden in .env as CORS_ORIGINS="http://localhost:3000,https://myapp.lovable.app")
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:5173,http://localhost:8080"
    )
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = Field(default=["*"])
    CORS_ALLOW_HEADERS: list[str] = Field(default=["*"])

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string"""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields from .env


settings = Settings()