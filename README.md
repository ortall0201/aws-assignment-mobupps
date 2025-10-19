# MobUpps – A/B Testing System for Mobile App Similarity & Performance Prediction

A comprehensive full-stack A/B testing system that finds similar mobile apps using ML embeddings and predicts performance based on historical data.

**📚 Complete Documentation: See [DOCUMENTATION.md](DOCUMENTATION.md) for comprehensive setup, usage, and API reference.**

## Overview

This system provides:
- **A/B Testing**: Compare two embedding models (v1: 64-dim vs v2: 128-dim) with sticky session assignment
- **Similarity Search**: Find similar apps using cosine similarity on ML-generated embeddings
- **Performance Prediction**: Predict app performance using weighted averages from historical CTR data
- **Full-Stack Application**: FastAPI backend + React TypeScript frontend with modern UI
- **Production Ready**: Structured logging, metrics collection, Docker support, and comprehensive monitoring

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

### 3. Run Backend

```bash
# Start FastAPI backend
uvicorn app.main:app --reload --port 8000
```

The backend will automatically download data files from Google Drive on first startup.

Backend API will be available at: `http://localhost:8000`

### 4. Run Frontend

```bash
# From project root, navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Run development server with hot reload
npm run dev
```

Frontend UI will be available at: `http://localhost:8080`

## Quick Start

Once both backend and frontend are running:

1. **Navigate to Search page** (`http://localhost:8080/`)
2. **Fill in the search form** with example values:
   - App Name: `Fitness Tracker Pro`
   - Category: `Health & Fitness`
   - Region: `US`
   - Pricing Model: `freemium`
   - Top K Results: `20`
3. **Click "Find Similar Apps"** - system will use v1 or v2 model (A/B test)
4. **View results** with real app names and similarity scores
5. **Click "Predict Performance"** button below results to see performance predictions

See [DOCUMENTATION.md](DOCUMENTATION.md) for detailed user guide with screenshots and explanations.

## Features

### Frontend UI (`http://localhost:8080`)
- **Search Page** (`/`): Interactive similarity search with A/B testing, inline performance prediction
- **Predict Page** (`/predict`): Standalone performance prediction interface (advanced usage)
- **Metrics Dashboard** (`/metrics`): Real-time operational metrics with auto-refresh
- **API Docs** (`/docs`): Integrated Swagger/OpenAPI documentation

### Backend API (`http://localhost:8000`)
- **A/B Testing**: Sticky session assignment (v1 vs v2 models)
- **Similarity Search**: Cosine similarity with configurable filters
- **Performance Prediction**: Weighted CTR-based predictions from historical data
- **Metrics Collection**: Request counts, latency percentiles, A/B assignments
- **Structured Logging**: Correlation IDs, JSON output, colorized console

## Docker Deployment

```bash
# Build backend image
docker build -t aws-assignment-mobupps:local .

# Run with environment file
docker run -p 8000:8000 --env-file .env aws-assignment-mobupps:local
```

For production deployment, see [DOCUMENTATION.md](DOCUMENTATION.md).

## API Endpoints (Quick Reference)

**Full API documentation with detailed examples: [DOCUMENTATION.md](DOCUMENTATION.md#api-reference)**

### Core Endpoints
- `GET /healthz` - Health check
- `GET /metrics` - Operational metrics (request counts, latency percentiles, A/B assignments)
- `POST /api/v1/find-similar` - Find similar apps with A/B testing
- `POST /api/v1/predict` - Predict performance from neighbor apps

### Example: Find Similar Apps
```bash
curl -X POST http://localhost:8000/api/v1/find-similar \
  -H "Content-Type: application/json" \
  -d '{
    "app": {
      "name": "Fitness Tracker Pro",
      "category": "Health & Fitness",
      "region": "US",
      "pricing": "freemium"
    },
    "top_k": 20,
    "partner_id": "partner-123"
  }'
```

## Testing

```bash
# Run all tests
pytest -q

# Run with coverage
pytest --cov=app tests/
```

## Project Structure

```
aws-assignment-mobupps/
├── app/                        # Backend (FastAPI)
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Settings and configuration
│   ├── models/schemas.py       # Pydantic request/response models
│   ├── routers/api_v1.py       # API endpoint definitions
│   ├── services/               # Core business logic
│   │   ├── ab_testing.py       # A/B test sticky assignment
│   │   ├── embeddings.py       # Embedding generation (v1: 64-dim, v2: 128-dim)
│   │   ├── similarity.py       # Cosine similarity search
│   │   └── predictor.py        # Performance prediction from historical CTR
│   ├── utils/                  # Utilities
│   │   ├── logging_config.py   # Structured logging with correlation IDs
│   │   └── data_loader.py      # Google Drive data loader
│   └── instrumentation/        # Monitoring
│       └── metrics.py          # Request/latency/A/B metrics collection
├── frontend/                   # Frontend (React + TypeScript + Vite)
│   ├── src/
│   │   ├── components/         # Reusable React components
│   │   │   ├── search/         # Search form and results
│   │   │   ├── predict/        # Prediction form and results
│   │   │   └── metrics/        # Metrics dashboard
│   │   ├── pages/              # Main page components
│   │   ├── lib/api.ts          # Backend API client
│   │   └── hooks/              # Custom React hooks
│   ├── public/                 # Static assets
│   └── package.json            # Frontend dependencies
├── data/                       # Data files (auto-downloaded from Google Drive)
│   ├── mock_embeddings_v1.pkl  # v1 model embeddings (64-dim)
│   ├── mock_embeddings_v2.pkl  # v2 model embeddings (128-dim)
│   ├── app_metadata.pkl        # App names and categories
│   ├── sample_apps.csv         # Sample apps for testing
│   └── historical_performance.csv  # Real CTR data for predictions
├── scripts/                    # Data generation scripts
│   └── generate_real_embeddings.py  # Generate embeddings for historical apps
├── tests/                      # Unit tests
├── Dockerfile                  # Backend container image
├── DOCUMENTATION.md            # Comprehensive documentation
├── architecture-diagram.md     # System architecture diagrams
└── README.md                   # This file
```

## Documentation

- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete setup, usage guide, API reference, troubleshooting
- **[architecture-diagram.md](architecture-diagram.md)** - Backend architecture and data flow diagrams
- **[SETUP_GDRIVE.md](SETUP_GDRIVE.md)** - Google Drive configuration for data files

## Key Technologies

- **Backend**: FastAPI, Pydantic, NumPy, Pandas, Uvicorn
- **Frontend**: React 18, TypeScript, Vite, TanStack Query, Tailwind CSS, shadcn/ui
- **Testing**: Pytest
- **Deployment**: Docker, environment-based configuration

## Contributing

This is a technical assignment project. For questions or issues, please refer to [DOCUMENTATION.md](DOCUMENTATION.md) or the inline code documentation.

## License

Proprietary - MobUpps A/B Testing Assignment
