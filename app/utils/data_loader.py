# Module: data_loader.py
# Downloads data files from Google Drive on startup

import os
import gdown
from pathlib import Path


class GoogleDriveDataLoader:
    """Download and cache data files from Google Drive"""

    def __init__(self, cache_dir: str = "data"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def download_file(self, gdrive_url: str, output_filename: str, force: bool = False) -> str:
        """
        Download file from Google Drive if not exists

        Args:
            gdrive_url: Google Drive sharing link or file ID
            output_filename: Local filename to save as
            force: Force re-download even if file exists

        Returns:
            Path to downloaded file
        """
        output_path = self.cache_dir / output_filename

        # Skip if file exists and not forcing
        if output_path.exists() and not force:
            print(f"[OK] Using cached file: {output_path}")
            return str(output_path)

        print(f"[DOWNLOAD] Downloading {output_filename} from Google Drive...")

        # Extract file ID from various Google Drive URL formats
        file_id = self._extract_file_id(gdrive_url)

        # Download using gdown
        gdown.download(
            f"https://drive.google.com/uc?id={file_id}",
            str(output_path),
            quiet=False
        )

        print(f"[OK] Downloaded: {output_path}")
        return str(output_path)

    def _extract_file_id(self, url: str) -> str:
        """Extract file ID from Google Drive URL or return as-is if already an ID"""
        if "drive.google.com" in url:
            # Handle different Google Drive URL formats
            if "/file/d/" in url:
                return url.split("/file/d/")[1].split("/")[0]
            elif "id=" in url:
                return url.split("id=")[1].split("&")[0]
        return url  # Assume it's already a file ID

    def load_all_data_files(self, file_mapping: dict) -> dict:
        """
        Download multiple files from Google Drive

        Args:
            file_mapping: Dict of {output_filename: gdrive_url}

        Returns:
            Dict of {output_filename: local_path}
        """
        paths = {}
        for filename, url in file_mapping.items():
            paths[filename] = self.download_file(url, filename)
        return paths


# Example usage in config
def ensure_data_files():
    """Download all required data files from Google Drive"""
    from app.config import settings

    loader = GoogleDriveDataLoader(cache_dir="data")

    # Map your Google Drive file URLs here
    file_mapping = {
        "mock_embeddings_v1.pkl": settings.GDRIVE_EMB_V1_URL,
        "mock_embeddings_v2.pkl": settings.GDRIVE_EMB_V2_URL,
        "sample_apps.csv": settings.GDRIVE_APPS_URL,
        "historical_performance.csv": settings.GDRIVE_PERF_URL,
    }

    # Remove empty URLs
    file_mapping = {k: v for k, v in file_mapping.items() if v}

    if file_mapping:
        print("[INFO] Loading data files from Google Drive...")
        paths = loader.load_all_data_files(file_mapping)
        print(f"[OK] All data files ready: {len(paths)} files")
        return paths
    else:
        print("[WARNING] No Google Drive URLs configured, using local files")
        return {}
