# MobUpps – A/B Testing System for Mobile App Similarity & Performance Prediction

**Author:** Ortal Lasry | ML Engineer
**Assignment:** MobUpps Home Assignment - Production ML System

A comprehensive full-stack A/B testing system that finds similar mobile apps using ML embeddings and predicts performance based on historical data.

---

## 📋 Assignment Deliverables

### Part A: AWS Architecture Design
**📄 [Part_A_Technical_Design.pdf](Part_A_Technical_Design.pdf)** - Complete technical design document covering:
- AWS architecture for production ML system (ECS, API Gateway, ElastiCache, DynamoDB, S3, SageMaker)
- A/B testing strategy with statistical rigor
- CI/CD pipeline with blue/green deployments
- Monitoring & alerting (3-tier system)
- Scaling from 100 to 1M+ requests/day
- Cost optimization strategies (43% savings)
- Security, compliance, and disaster recovery

### Part B: Local Implementation (This Repository)
**✅ All requirements implemented** - Production-ready similarity service with:
- ✅ FastAPI backend with A/B testing framework
- ✅ Similarity search with exact cosine similarity (~30ms latency)
- ✅ Performance prediction with caching optimization (3-5ms)
- ✅ Docker containerization
- ✅ Comprehensive error handling & logging
- ✅ Unit & performance tests (all passing, <200ms requirement exceeded)
- ✅ Full-stack React UI with search functionality

---

## 📚 Documentation

**Quick Links:**
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete setup, usage guide, API reference, troubleshooting
- **[architecture-diagram.md](architecture-diagram.md)** - System architecture, sequence diagrams, data flow
- **[Part_A_Technical_Design.pdf](Part_A_Technical_Design.pdf)** - AWS production architecture (Part A solution)
- **[SETUP_GDRIVE.md](SETUP_GDRIVE.md)** - Google Drive configuration for data files

---

## Overview

This system provides:
- **A/B Testing**: Compare two embedding models (v1: 64-dim vs v2: 128-dim) with sticky session assignment
- **Similarity Search**: Find similar apps using cosine similarity on ML-generated embeddings
- **Performance Prediction**: Predict app performance using weighted averages from historical CTR data
- **Full-Stack Application**: FastAPI backend + React TypeScript frontend with modern UI
- **Production Ready**: Structured logging, metrics collection, Docker support, and comprehensive monitoring

## 🚀 Quick Setup (5 minutes)

### Prerequisites
- Python 3.9+ (tested with Python 3.13)
- Node.js 18+ and npm
- Git

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

### 2. Install Backend Dependencies

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### 3. Run Backend (Terminal 1)

```bash
# Start FastAPI backend with auto-reload
python -m uvicorn app.main:app --reload --port 8000
```

**✅ Backend started successfully when you see:**
```
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO: Started reloader process
INFO: Started server process
INFO: Application startup complete.
INFO: Cached performance data for 38 apps
```

**Backend will be available at:** `http://localhost:8000`
**Interactive API docs:** `http://localhost:8000/docs`

### 4. Run Frontend (Terminal 2 - New Terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**✅ Frontend started successfully when you see:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:8080/
➜  Network: use --host to expose
```

**Frontend will be available at:** `http://localhost:8080`

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

**✅ Fully Functional:**
- **Search Page** (`/`): Interactive similarity search with A/B testing, inline performance prediction
  - Complete end-to-end workflow with real backend APIs
  - Find similar apps, view results, predict performance

**⚠️ UI Mockups (Demonstration Only):**
- **Predict Page** (`/predict`): Static demo form (not connected to backend)
- **Metrics Dashboard** (`/metrics`): Static demo dashboard (not connected to backend)

**📖 For Real API Access:**
- Swagger UI: `http://localhost:8000/docs` (interactive API testing)
- ReDoc: `http://localhost:8000/redoc` (beautiful API documentation)
- Metrics API: `http://localhost:8000/metrics` (real operational metrics)

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

## 🧪 Testing

```bash
# Run all tests
pytest -q

# Run specific test suites
pytest tests/test_health.py -v          # Health checks
pytest tests/test_similarity.py -v      # Similarity service
pytest tests/test_performance.py -v     # Performance tests (<200ms requirement)

# Run with coverage report
pytest --cov=app tests/

# Expected results:
# ✅ All tests pass
# ✅ find-similar latency: ~30ms (6.6x faster than 200ms requirement)
# ✅ predict latency: ~3-5ms (with caching optimization)
```

### Performance Test Results
```
tests/test_performance.py::test_find_similar_latency_single_request PASSED
tests/test_performance.py::test_find_similar_latency_average PASSED
tests/test_performance.py::test_find_similar_latency_with_different_k_values PASSED
tests/test_performance.py::test_predict_endpoint_functional PASSED
tests/test_performance.py::test_cold_start_vs_warm PASSED

===================== 5 passed ======================
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
│   │   ├── ab_test.py          # A/B test sticky assignment
│   │   ├── embeddings.py       # Embedding generation (v1: 64-dim, v2: 128-dim)
│   │   ├── similarity.py       # Cosine similarity search
│   │   └── predictor.py        # Performance prediction from historical CTR
│   ├── utils/                  # Utilities
│   │   ├── logging.py          # Structured logging with correlation IDs
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

## 📖 Complete Documentation

### Assignment Deliverables
- **[Part_A_Technical_Design.pdf](Part_A_Technical_Design.pdf)** - AWS architecture design (Part A solution)
  - 10+ pages covering AWS services, A/B testing, CI/CD, monitoring, scaling, cost optimization

### Technical Documentation
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete documentation (setup, usage, API reference, troubleshooting)
  - Backend architecture and components
  - Frontend components and pages
  - Performance optimization (99.9% improvement with caching)
  - Technical deep dive (cosine similarity, weighted CTR prediction)
  - Error handling and production readiness

- **[architecture-diagram.md](architecture-diagram.md)** - Architecture diagrams with Mermaid
  - Sequence diagrams (find-similar, predict flows)
  - Component architecture
  - A/B testing flow
  - Data flow diagrams
  - Exact vs ANN similarity search comparison

### Setup Guides
- **[SETUP_GDRIVE.md](SETUP_GDRIVE.md)** - Google Drive configuration for data files
- **[README.md](README.md)** - This file (quick start guide)

## Key Technologies

- **Backend**: FastAPI, Pydantic, NumPy, Pandas, Uvicorn
- **Frontend**: React 18, TypeScript, Vite, TanStack Query, Tailwind CSS, shadcn/ui
- **Testing**: Pytest
- **Deployment**: Docker, environment-based configuration

## Contributing

This is a technical assignment project. For questions or issues, please refer to [DOCUMENTATION.md](DOCUMENTATION.md) or the inline code documentation.

## License

Proprietary - MobUpps A/B Testing Assignment
