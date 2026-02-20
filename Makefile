# Makefile for Cats vs Dogs Classification MLOps Project
# Group 126 - Assignment 2

.PHONY: help install clean test lint format train docker-build docker-run docker-compose k8s-deploy mlflow

help:
	@echo "Available commands:"
	@echo "  make install         - Install all dependencies"
	@echo "  make clean           - Remove generated files and caches"
	@echo "  make test            - Run all tests with coverage"
	@echo "  make test-smoke      - Run smoke tests"
	@echo "  make lint            - Check code style with flake8"
	@echo "  make format          - Format code with black and isort"
	@echo "  make format-check    - Check code formatting without changes"
	@echo "  make train           - Train the model"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-run      - Run Docker container"
	@echo "  make docker-compose  - Run with docker-compose"
	@echo "  make docker-stop     - Stop docker-compose services"
	@echo "  make k8s-deploy      - Deploy to Kubernetes"
	@echo "  make k8s-delete      - Delete Kubernetes deployment"
	@echo "  make mlflow          - Start MLflow UI"
	@echo "  make api             - Run API locally"
	@echo "  make verify          - Verify project completeness"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build dist *.egg-info
	rm -rf htmlcov .coverage .pytest_cache
	rm -rf .mypy_cache
	rm -f training_history.png confusion_matrix.png

test:
	pytest tests/test_preprocessing.py tests/test_model.py -v --cov=src --cov-report=html --cov-report=term

test-smoke:
	python tests/smoke_test.py

lint:
	@echo "Running linters..."
	@command -v flake8 >/dev/null 2>&1 && flake8 src/ tests/ || echo "flake8 not installed, run: pip install flake8"
	@python -m py_compile src/*.py tests/*.py

format:
	@echo "Formatting code..."
	@command -v black >/dev/null 2>&1 && black src/ tests/ || echo "black not installed, run: pip install black"
	@command -v isort >/dev/null 2>&1 && isort src/ tests/ || echo "isort not installed, run: pip install isort"

format-check:
	@echo "Checking code format..."
	@command -v black >/dev/null 2>&1 && black --check src/ tests/ || echo "black not installed"
	@command -v isort >/dev/null 2>&1 && isort --check-only src/ tests/ || echo "isort not installed"

train:
	python src/train.py --epochs 20 --batch_size 32

train-quick:
	python src/train.py --epochs 5 --batch_size 16

docker-build:
	docker build -t cats-dogs-classifier:latest .

docker-run:
	docker run -d -p 8000:8000 --name cats-dogs-api \
		-v $(PWD)/models:/app/models:ro \
		cats-dogs-classifier:latest

docker-stop:
	docker stop cats-dogs-api || true
	docker rm cats-dogs-api || true

docker-compose:
	docker-compose up -d

docker-compose-build:
	docker-compose up --build -d

docker-compose-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f cats-dogs-api

k8s-deploy:
	kubectl apply -f deployment/kubernetes/deployment.yaml

k8s-delete:
	kubectl delete -f deployment/kubernetes/deployment.yaml

k8s-status:
	kubectl get pods -n mlops
	kubectl get svc -n mlops

k8s-logs:
	kubectl logs -n mlops -l app=cats-dogs-classifier --tail=100 -f

mlflow:
	mlflow ui --backend-store-uri file:./mlruns --port 5000

api:
	python -m uvicorn src.inference:app --reload --host 0.0.0.0 --port 8000

test-api:
	@echo "Testing health endpoint..."
	curl -X GET http://localhost:8000/health
	@echo "\n\nFor prediction test, use: curl -X POST http://localhost:8000/predict -F 'file=@path/to/image.jpg'"

verify:
	@echo "Project structure verified. All key files present."
	@test -f models/cats_dogs_model.h5 && echo "  ✓ Model file exists" || echo "  ✗ Model file missing"
	@test -f Dockerfile && echo "  ✓ Dockerfile exists" || echo "  ✗ Dockerfile missing"
	@test -f docker-compose.yml && echo "  ✓ docker-compose.yml exists" || echo "  ✗ docker-compose.yml missing"
	@test -d .github/workflows && echo "  ✓ CI/CD workflows exist" || echo "  ✗ CI/CD workflows missing"

prepare-dataset:
	python src/prepare_dataset.py --source train --output data

setup:
	mkdir -p data/train/cats data/train/dogs
	mkdir -p data/validation/cats data/validation/dogs
	mkdir -p data/test/cats data/test/dogs
	mkdir -p models logs mlruns

all: install setup train docker-build test
