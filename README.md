# MobUpps – AB Similarity & Predict API (Part B)

## Run (local)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

## Run (docker)
docker build -t aws-assignment-mobupps:local .
docker run -p 8000:8000 aws-assignment-mobupps:local

## API
POST /api/v1/find-similar
POST /api/v1/predict
