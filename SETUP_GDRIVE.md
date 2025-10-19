# Google Drive Data Setup Guide

This guide explains how to configure your app to load large data files from Google Drive instead of storing them in the repository.

## Quick Setup

### 1. Get Google Drive Share Links

For each data file in your Google Drive:

1. Right-click the file → **Share**
2. Change access to **Anyone with the link**
3. Copy the share link

You'll get a URL like:
```
https://drive.google.com/file/d/1ABC123xyz_FILE_ID_HERE/view?usp=sharing
```

### 2. Configure Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your Google Drive URLs:

```env
# Google Drive URLs - paste your share links here
GDRIVE_EMB_V1_URL=https://drive.google.com/file/d/YOUR_V1_FILE_ID/view
GDRIVE_EMB_V2_URL=https://drive.google.com/file/d/YOUR_V2_FILE_ID/view
GDRIVE_APPS_URL=https://drive.google.com/file/d/YOUR_APPS_FILE_ID/view
GDRIVE_PERF_URL=https://drive.google.com/file/d/YOUR_PERF_FILE_ID/view
```

Or just use the file IDs:

```env
GDRIVE_EMB_V1_URL=1ABC123xyz_FILE_ID_HERE
GDRIVE_EMB_V2_URL=1DEF456xyz_FILE_ID_HERE
GDRIVE_APPS_URL=1GHI789xyz_FILE_ID_HERE
GDRIVE_PERF_URL=1JKL012xyz_FILE_ID_HERE
```

### 3. Run Your App

The app will automatically download files on startup:

```bash
# Local development
uvicorn app.main:app --reload

# Docker
docker build -t mobupps-ab:local .
docker run -p 8000:8000 --env-file .env mobupps-ab:local
```

## How It Works

1. **On Startup**: The app checks if data files exist in the `data/` directory
2. **Download**: If missing, it downloads them from Google Drive using the URLs in `.env`
3. **Cache**: Downloaded files are cached locally in `data/` directory
4. **Reuse**: On subsequent starts, cached files are used (no re-download)

## File Mapping

| Environment Variable | Local File Path | Description |
|---------------------|-----------------|-------------|
| `GDRIVE_EMB_V1_URL` | `data/mock_embeddings_v1.pkl` | Embeddings version 1 |
| `GDRIVE_EMB_V2_URL` | `data/mock_embeddings_v2.pkl` | Embeddings version 2 |
| `GDRIVE_APPS_URL` | `data/sample_apps.csv` | Sample apps database |
| `GDRIVE_PERF_URL` | `data/historical_performance.csv` | Historical performance data |

## Troubleshooting

### Files not downloading?

Check that your Google Drive links have public access:
- Go to Google Drive
- Right-click file → Share
- Ensure "Anyone with the link" can view

### Want to force re-download?

Delete the cached files and restart:

```bash
rm -rf data/*.pkl data/*.csv
uvicorn app.main:app --reload
```

### Large files timing out?

For very large files (>500MB), consider:
1. Using Google Cloud Storage instead of Drive
2. Mounting a persistent volume with pre-downloaded data
3. Using AWS S3 or Azure Blob Storage

## Production Deployment

### AWS ECS/EC2

Add environment variables to your task definition:

```json
{
  "environment": [
    {"name": "GDRIVE_EMB_V1_URL", "value": "YOUR_FILE_ID"},
    {"name": "GDRIVE_EMB_V2_URL", "value": "YOUR_FILE_ID"}
  ]
}
```

### Kubernetes

Create a ConfigMap or Secret:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: gdrive-config
data:
  GDRIVE_EMB_V1_URL: "YOUR_FILE_ID"
  GDRIVE_EMB_V2_URL: "YOUR_FILE_ID"
```

### Alternative: Pre-download Data

For production, you might want to pre-download data into your container:

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download data at build time
ENV GDRIVE_EMB_V1_URL=YOUR_FILE_ID
RUN python -c "from app.utils.data_loader import ensure_data_files; ensure_data_files()"

# Copy app code
COPY app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Security Notes

- **Public files only**: This method works for public Google Drive files
- **For private files**: Use Google Drive API with service account credentials
- **Sensitive data**: Consider using encrypted storage (S3 + KMS, GCS with encryption)
- **Rate limits**: Google Drive has download limits; cache aggressively in production
