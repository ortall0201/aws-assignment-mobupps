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

## Web UI Dashboard

A modern React dashboard is available for this API at:
**Repository**: `https://github.com/ortall0201/mobdups-lab-suite`

### Quick Setup
```bash
# Clone UI repository
git clone https://github.com/ortall0201/mobdups-lab-suite
cd mobdups-lab-suite

# Install and run
npm install
npm run dev
```

The UI will be available at `http://localhost:5173` and includes:
- **Search Page**: Interactive similarity search with A/B testing
- **Predict Page**: Performance prediction interface
- **Metrics Dashboard**: Real-time operational metrics with auto-refresh
- **API Docs**: Integrated API documentation

See `UI_INTEGRATION.md` for detailed integration documentation.

## API Endpoints

### Health Check
```
GET /healthz
```

### Metrics
```
GET /metrics
```
Returns operational metrics including:
- Request counts (total, by endpoint, by status code)
- Latency statistics (avg, min, max, p50, p95, p99)
- A/B test assignments by arm and endpoint
- Error counts by type

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

## Logging & Monitoring

### Structured Logging
The API includes structured logging with:
- Correlation ID tracking across requests
- Request/response logging with timing
- A/B test assignment logging
- Colorized console output for development
- JSON output for production (set `structured=True` in `main.py`)

All logs include correlation IDs for tracing requests across services.

### Metrics Collection
Real-time metrics are collected for:
- **Request Metrics**: Total requests, requests per endpoint, status code distribution
- **Latency Metrics**: Average, min, max, and percentiles (p50, p95, p99) per endpoint
- **A/B Test Metrics**: Assignment counts by arm and endpoint
- **Error Metrics**: Total errors and errors by type

Access metrics via `GET /metrics` endpoint.

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
