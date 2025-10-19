.PHONY: run test docker-build docker-run

run:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -q

docker-build:
	docker build -t aws-assignment-mobupps:local .

docker-run:
	docker run -it --rm -p 8000:8000 aws-assignment-mobupps:local
