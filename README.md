# MobUpps – AB Similarity & Predict API (Part B)

A/B testing system for similarity search and performance prediction using embeddings.

## Setup

### 1. Configure Data Files (Google Drive)

Since data files are too large for Git, they're loaded from Google Drive on startup.

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Add your Google Drive share links to `.env`:
   ```env
   GDRIVE_EMB_V1_URL=https://drive.google.com/file/d/YOUR_FILE_ID/view
   GDRIVE_EMB_V2_URL=https://drive.google.com/file/d/YOUR_FILE_ID/view
   GDRIVE_APPS_URL=https://drive.google.com/file/d/YOUR_FILE_ID/view
   GDRIVE_PERF_URL=https://drive.google.com/file/d/YOUR_FILE_ID/view
   ```

📖 See [SETUP_GDRIVE.md](SETUP_GDRIVE.md) for detailed instructions.

### 2. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run Locally

```bash
uvicorn app.main:app --reload --port 8000
```

The app will automatically download data files from Google Drive on first startup.

## Run with Docker

```bash
# Build
docker build -t aws-assignment-mobupps:local .

# Run with environment file
docker run -p 8000:8000 --env-file .env aws-assignment-mobupps:local
```

## API Endpoints

### Health Check
```
GET /healthz
```

### Find Similar Apps
```
POST /api/v1/find-similar
Content-Type: application/json

{
  "app": {
    "name": "FitNow",
    "category": "Health & Fitness",
    "region": "US",
    "pricing": "freemium",
    "features": ["sharing", "tracking"]
  },
  "filters": {"region": ["US"], "category": ["Health & Fitness"]},
  "top_k": 20,
  "partner_id": "partner-123",
  "app_id": "fitnow-001"
}
```

### Predict Performance
```
POST /api/v1/predict
Content-Type: application/json

{
  "app": {
    "name": "FitNow",
    "category": "Health & Fitness",
    "region": "US",
    "pricing": "freemium",
    "features": ["sharing", "tracking"]
  },
  "neighbors": [
    {"app_id": "app_42", "similarity": 0.93},
    {"app_id": "app_7", "similarity": 0.90}
  ],
  "ab_arm": "v2"
}
```

## Testing

```bash
pytest -q
```

## Project Structure

```
aws-assignment-mobupps/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── models/schemas.py    # Pydantic models
│   ├── routers/             # API routes
│   ├── services/            # Business logic (A/B, embeddings, similarity, prediction)
│   └── utils/               # Utilities (logging, data loader)
├── data/                    # Data files (downloaded from Google Drive)
├── tests/                   # Unit tests
└── Dockerfile
```

## Architecture

See [architecture-diagram.md](architecture-diagram.md) for detailed flow diagrams.
