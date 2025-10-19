# Backend Integration Complete ✅

This UI has been integrated with the MobUpps FastAPI backend.

## What's Been Done

### 1. API Service Layer
- Created `src/lib/api.ts` with all backend endpoints
- Proper TypeScript types matching backend schemas
- Correlation ID tracking in responses
- Error handling and response transformation

### 2. Environment Configuration
- Created `.env` file with API base URL
- Default: `http://localhost:8000`
- Update for production deployment as needed

### 3. Component Updates
- **SearchForm**: Now sends correct payload format to `/api/v1/find-similar`
- **Metrics Page**: Transforms backend metrics to UI format
- **PredictForm**: Updated to match `/api/v1/predict` endpoint

### 4. Response Transformations
- Backend `neighbors` → UI `similar_apps`
- Backend `Neighbor` → UI `SimilarApp` with app_name
- Backend metrics structure → UI metrics structure

## Quick Start

### 1. Start the Backend
```bash
cd C:\Users\user\Desktop\aws-assignment-mobupps
uvicorn app.main:app --reload --port 8000
```

### 2. Install UI Dependencies
```bash
cd C:\Users\user\Desktop\mobdups-lab-suite
npm install
```

### 3. Start the UI
```bash
npm run dev
```

### 4. Open in Browser
```
http://localhost:5173
```

## Testing the Integration

### Search Page (/)
1. Fill in app details (name, category, region, pricing)
2. Select features (optional)
3. Click "Find Similar Apps"
4. Should see results with A/B arm badge (v1 or v2)
5. Check browser DevTools for X-Correlation-ID header

### Metrics Dashboard (/metrics)
1. Should load automatically
2. Shows real-time requests, latency, A/B splits
3. Use refresh dropdown for auto-refresh (5s/10s/30s)
4. Export button downloads metrics as JSON

### Predict Page (/predict)
1. Enter app ID and partner ID
2. Select A/B arm (v1 or v2)
3. Paste neighbor results from search (JSON format)
4. Click "Predict Performance"
5. See predicted score and user segments

## API Endpoints Being Used

- `POST /api/v1/find-similar` - Similarity search
- `POST /api/v1/predict` - Performance prediction
- `GET /metrics` - Operational metrics
- `GET /healthz` - Health check

## Troubleshooting

### CORS Errors
- Backend already configured to allow `localhost:5173`
- Check backend console for CORS logs
- Verify backend is running on port 8000

### Connection Errors
- Ensure backend is running: `http://localhost:8000/docs`
- Check `.env` file has correct `VITE_API_BASE_URL`
- Check browser console for network errors

### 404 Errors
- Verify API endpoint paths match backend
- Check FastAPI Swagger docs: `http://localhost:8000/docs`

## Production Deployment

### Update Environment
```env
# In .env file:
VITE_API_BASE_URL=https://your-production-api.com
```

### Update Backend CORS
```env
# In backend .env file:
CORS_ORIGINS=https://your-lovable-app.lovable.app,http://localhost:5173
```

## Next Steps

1. Test all pages thoroughly
2. Check correlation IDs are working
3. Verify A/B arm assignments
4. Test metrics auto-refresh
5. Deploy to production

## Support

Backend repo: `C:\Users\user\Desktop\aws-assignment-mobupps`
UI repo: `C:\Users\user\Desktop\mobdups-lab-suite`

Integration documentation: `UI_INTEGRATION.md` in backend repo
