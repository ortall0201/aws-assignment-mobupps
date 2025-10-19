# UI Integration Guide

## Backend Setup (Completed ✅)

The FastAPI backend is now configured with:
- **CORS enabled** for cross-origin requests from the UI
- **Allowed origins**: `http://localhost:3000`, `http://localhost:5173`, `http://localhost:8080`
- **Correlation ID tracking** in all responses via `X-Correlation-ID` header
- **Metrics endpoint** at `/metrics` for dashboard data

### To add Lovable deployment URL:
Edit `.env` file and add:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://your-app.lovable.app
```

## Frontend Setup (Lovable UI)

### 1. Clone the UI Repository
```bash
cd C:\Users\user\Desktop
git clone https://github.com/ortall0201/mobdups-lab-suite
cd mobdups-lab-suite
```

### 2. Configure API Base URL

Look for the API configuration file (usually one of these):
- `src/config.ts`
- `src/lib/config.ts`
- `.env` or `.env.local`
- `vite.config.ts` or `next.config.js`

Add/update the API URL:
```typescript
// In config file:
export const API_BASE_URL = process.env.VITE_API_URL || "http://localhost:8000";

// Or in .env file:
VITE_API_URL=http://localhost:8000
```

### 3. Install and Run
```bash
npm install
npm run dev
```

The UI should now be accessible at `http://localhost:5173` (or port shown in console).

## API Endpoints Reference

### Health Check
```http
GET http://localhost:8000/healthz
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-19T14:45:00Z"
}
```

### Get Metrics
```http
GET http://localhost:8000/metrics
```

**Response:**
```json
{
  "uptime_seconds": 123.45,
  "requests": {
    "total": 42,
    "by_endpoint": {
      "/api/v1/find-similar": 20,
      "/api/v1/predict": 15
    },
    "by_status": {
      "200": 40,
      "400": 2
    }
  },
  "latencies": {
    "/api/v1/find-similar": {
      "count": 20,
      "avg_ms": 45.2,
      "min_ms": 12.5,
      "max_ms": 102.3,
      "p50_ms": 42.0,
      "p95_ms": 89.5,
      "p99_ms": 98.1
    }
  },
  "ab_tests": {
    "total_assignments": 20,
    "by_arm": {
      "v1": 12,
      "v2": 8
    },
    "by_endpoint": {
      "/api/v1/find-similar": {
        "v1": 12,
        "v2": 8
      }
    }
  },
  "errors": {
    "total": 2,
    "by_type": {}
  }
}
```

### Find Similar Apps
```http
POST http://localhost:8000/api/v1/find-similar
Content-Type: application/json
```

**Request Body:**
```json
{
  "app": {
    "name": "FitNow",
    "category": "Health & Fitness",
    "region": "US",
    "pricing": "freemium",
    "features": ["sharing", "tracking"]
  },
  "filters": {
    "region": ["US"],
    "category": ["Health & Fitness"]
  },
  "top_k": 20,
  "partner_id": "partner-123",
  "app_id": "fitnow-001"
}
```

**Response:**
```json
{
  "neighbors": [
    {
      "app_id": "app_42",
      "similarity": 0.93
    },
    {
      "app_id": "app_17",
      "similarity": 0.89
    }
  ],
  "ab_arm": "v2"
}
```

**Response Headers:**
- `X-Correlation-ID`: Unique request identifier for tracing

### Predict Performance
```http
POST http://localhost:8000/api/v1/predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "app": {
    "name": "FitNow",
    "category": "Health & Fitness",
    "region": "US",
    "pricing": "freemium",
    "features": ["sharing", "tracking"]
  },
  "neighbors": [
    {
      "app_id": "app_42",
      "similarity": 0.93
    },
    {
      "app_id": "app_7",
      "similarity": 0.90
    }
  ],
  "ab_arm": "v2"
}
```

**Response:**
```json
{
  "ab_arm": "v2",
  "prediction": {
    "score": 0.85,
    "segments": ["tech-savvy", "fitness-enthusiasts", "premium-users"]
  },
  "latency_ms": 42
}
```

## Frontend Integration Code Examples

### TypeScript Types
```typescript
// types.ts
export interface AppMeta {
  name?: string;
  category?: string;
  region?: string;
  pricing?: string;
  features?: string[];
}

export interface Neighbor {
  app_id: string;
  similarity: number;
}

export interface SimilarRequest {
  app: AppMeta;
  filters?: Record<string, string[]>;
  top_k?: number;
  partner_id?: string;
  app_id?: string;
}

export interface SimilarResponse {
  neighbors: Neighbor[];
  ab_arm: string;
}

export interface PredictRequest {
  app: AppMeta;
  neighbors: Neighbor[];
  ab_arm: string;
}

export interface Prediction {
  score: number;
  segments: string[];
}

export interface PredictResponse {
  ab_arm: string;
  prediction: Prediction;
  latency_ms: number;
}

export interface MetricsResponse {
  uptime_seconds: number;
  requests: {
    total: number;
    by_endpoint: Record<string, number>;
    by_status: Record<string, number>;
  };
  latencies: Record<string, {
    count: number;
    avg_ms: number;
    min_ms: number;
    max_ms: number;
    p50_ms: number;
    p95_ms: number;
    p99_ms: number;
  }>;
  ab_tests: {
    total_assignments: number;
    by_arm: Record<string, number>;
    by_endpoint: Record<string, Record<string, number>>;
  };
  errors: {
    total: number;
    by_type: Record<string, number>;
  };
}
```

### API Service
```typescript
// api.ts
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function findSimilarApps(request: SimilarRequest): Promise<SimilarResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/find-similar`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export async function predictPerformance(request: PredictRequest): Promise<PredictResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export async function getMetrics(): Promise<MetricsResponse> {
  const response = await fetch(`${API_BASE_URL}/metrics`);

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export async function healthCheck(): Promise<{ status: string; timestamp: string }> {
  const response = await fetch(`${API_BASE_URL}/healthz`);

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}
```

### React Hook Example
```typescript
// useSimilarity.ts
import { useState } from 'react';
import { findSimilarApps } from './api';
import type { SimilarRequest, SimilarResponse } from './types';

export function useSimilarity() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<SimilarResponse | null>(null);

  const search = async (request: SimilarRequest) => {
    setLoading(true);
    setError(null);

    try {
      const result = await findSimilarApps(request);
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return { search, loading, error, data };
}
```

## Testing the Integration

### 1. Start the Backend
```bash
cd C:\Users\user\Desktop\aws-assignment-mobupps
uvicorn app.main:app --reload --port 8000
```

### 2. Start the Frontend
```bash
cd C:\Users\user\Desktop\mobdups-lab-suite
npm run dev
```

### 3. Test with cURL
```bash
# Health check
curl http://localhost:8000/healthz

# Find similar apps
curl -X POST http://localhost:8000/api/v1/find-similar \
  -H "Content-Type: application/json" \
  -d '{
    "app": {
      "name": "TestApp",
      "category": "Games",
      "region": "US",
      "pricing": "free",
      "features": ["social"]
    },
    "top_k": 5,
    "partner_id": "test-partner",
    "app_id": "test-app"
  }'

# Get metrics
curl http://localhost:8000/metrics
```

## Troubleshooting

### CORS Errors
If you see CORS errors in the browser console:
1. Check that your UI URL is in the CORS_ORIGINS list
2. Update `.env` file with your Lovable app URL
3. Restart the FastAPI server

### API Not Found (404)
- Verify the API is running: `http://localhost:8000/docs`
- Check the API_BASE_URL in your frontend config
- Ensure no trailing slashes in the base URL

### Connection Refused
- Ensure FastAPI is running on port 8000
- Check firewall settings
- Verify the port is not in use by another application

## Next Steps

Once the UI is connected:
1. Test all endpoints through the UI
2. Verify metrics dashboard displays real-time data
3. Test A/B arm assignments (should show v1 or v2)
4. Check correlation IDs in browser DevTools Network tab
5. Deploy frontend to Lovable and update CORS_ORIGINS
