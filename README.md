# Cats vs Dogs Classification - MLOps Pipeline

**Group 126** - MLOps Assignment 2 (S1-25_AIMLCZG523)

## Contributors
- Devaprasad P           (2023aa05069@wilp.bits-pilani.ac.in)
- Devender Kumar         (2024aa05065@wilp.bits-pilani.ac.in)
- Chavali Amrutha Valli  (2024aa05610@wilp.bits-pilani.ac.in)
- Palakolanu Preethi     (2024aa05608@wilp.bits-pilani.ac.in)
- Rohan Tirthankar Behera(2024aa05607@wilp.bits-pilani.ac.in)

**Repository:** https://github.com/devaprasadp-bits/MLOPS_Assignment2_Group126

---

We built a complete MLOps pipeline for binary image classification using the Kaggle Cats vs Dogs dataset. The system includes model training with experiment tracking, REST API deployment, Docker containers, automated CI/CD with GitHub Actions, and Kubernetes orchestration.

## What We Built

**Module 1: Model Development & Experiment Tracking**
- CNN model with 4 convolutional blocks for image classification
- Training pipeline with data augmentation (rotation, flip, zoom)
- MLflow integration to track experiments, metrics, and model artifacts
- DVC setup for dataset versioning

**Module 2: Model Packaging & Containerization**
- FastAPI service with `/health` and `/predict` endpoints
- Docker image with multi-stage builds to keep size around 1.2GB
- docker-compose file to run API + MLflow together

**Module 3: CI Pipeline**
- 25+ unit tests covering preprocessing and model logic
- GitHub Actions workflow that runs tests and builds Docker images
- Automated push to Docker Hub on main branch

**Module 4: CD Pipeline & Deployment**
- Kubernetes manifests (deployment + service + namespace)
- CD workflow that deploys to K8s after successful CI
- Smoke tests to verify deployment health

**Module 5: Monitoring & Logging**
- Structured logging throughout the application
- ModelMonitor class to track prediction metrics
- Health checks with liveness and readiness probes

## Project Structure

```
MLOPS_Assignment2_Group126/
├── src/                        # Source code
│   ├── data_preprocessing.py   # Data loading and preprocessing
│   ├── model.py                # CNN model architecture
│   ├── train.py                # Training script with MLflow
│   ├── inference.py            # FastAPI inference service
│   ├── monitoring.py           # Monitoring utilities
│   └── prepare_dataset.py      # Dataset preparation
├── tests/                      # Unit and smoke tests
│   ├── test_preprocessing.py   # Preprocessing tests (10+ tests)
│   ├── test_model.py           # Model tests (15+ tests)
│   └── smoke_test.py           # Post-deployment tests
├── deployment/                 # Kubernetes manifests
│   └── kubernetes/
│       └── deployment.yaml     # K8s deployment config
├── .github/workflows/          # CI/CD pipelines
│   ├── ci.yml                  # Continuous Integration
│   └── cd.yml                  # Continuous Deployment
├── models/                     # Trained model artifacts
├── logs/                       # Application logs
├── .dvc/                       # DVC configuration
├── data.dvc                    # DVC data tracking
├── Dockerfile                  # Container specification
├── docker-compose.yml          # Local deployment
├── Makefile                    # Common commands
├── setup.cfg                   # Tool configurations
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup and Running

You'll need Python 3.9+, Docker, and optionally kubectl/Minikube for K8s deployment.

### 1. Clone and Install

```bash
git clone https://github.com/devaprasadp-bits/MLOPS_Assignment2_Group126.git
cd MLOPS_Assignment2_Group126

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Get the Dataset

We used the Kaggle Dogs vs Cats dataset (25,000 images). Download it:

```bash
pip install kaggle
kaggle competitions download -c dogs-vs-cats
unzip train.zip

python src/prepare_dataset.py --source train --output data
```

This splits images into train/validation/test folders (80/10/10 split).

### 3. Train the Model

The trained model isn't in the repo, so you need to run training first:

```bash
python src/train.py --epochs 20 --batch_size 32
```

Training takes about 30-60 minutes depending on your hardware. The model gets saved to `models/cats_dogs_model.h5` and all metrics go to MLflow.

View experiments:
```bash
mlflow ui --port 5000
```

### 4. Run the API

Once you have the trained model:

```bash
uvicorn src.inference:app --reload --port 8000
```

Test it:
```bash
curl http://localhost:8000/health

curl -X POST "http://localhost:8000/predict" \
  -F "file=@path/to/image.jpg"
```

### 5. Docker Deployment

Build and run with Docker:
```bash
docker build -t cats-dogs-classifier:latest .
docker run -p 8000:8000 cats-dogs-classifier:latest
```

Or use docker-compose (runs both API and MLflow):
```bash
docker-compose up -d
```

Access at http://localhost:8000 (API) and http://localhost:5000 (MLflow).

### 6. Kubernetes Deployment

We deployed to Minikube for testing:

```bash
minikube start
minikube image load cats-dogs-classifier:latest

kubectl apply -f deployment/kubernetes/deployment.yaml
kubectl get pods -n mlops

# Access the service
minikube service cats-dogs-service --url -n mlops
```

The deployment creates 2 replicas with health checks and rolling updates configured.

## Testing

We wrote 25+ unit tests using pytest:

```bash
pytest tests/ -v --cov=src
```

Tests cover:
- Image preprocessing (loading, resizing, normalization)
- Model architecture (layers, shapes, outputs)
- API endpoints (health check, predictions)

Smoke tests for post-deployment validation:
```bash
export API_URL=http://localhost:8000
python tests/smoke_test.py
```

## CI/CD Setup

**Continuous Integration** (`.github/workflows/ci.yml`):
Runs on every push/PR. Steps are: install dependencies → run tests → build Docker image → push to Docker Hub (on main branch only).

**Continuous Deployment** (`.github/workflows/cd.yml`):
Triggers after CI passes on main branch. Updates Kubernetes deployment with new image, waits for rollout, then runs smoke tests.

GitHub secrets needed:
- `DOCKER_USERNAME` and `DOCKER_PASSWORD` for Docker Hub
- `KUBE_CONFIG` for Kubernetes access
- `API_URL` for smoke tests

## Model Details

We built a simple CNN:
- Input: 224x224 RGB images
- 4 convolutional blocks (32, 64, 128, 128 filters)
- MaxPooling after each block
- Dense layer with 512 units and 0.5 dropout
- Sigmoid output for binary classification

Training config:
- Adam optimizer (lr=0.001)
- Binary crossentropy loss
- Data augmentation: rotation, flip, zoom, shift
- Early stopping on validation loss (patience=5)

Expected accuracy is around 90-92% on test set after 20 epochs.

## API Endpoints

The FastAPI service exposes:

| Endpoint | Method | Input | Output |
|----------|--------|-------|--------|
| `/health` | GET | - | Status and system metrics |
| `/predict` | POST | Image file | class_label, probability, timestamp |
| `/docs` | GET | - | Interactive API docs |

Response example:
```json
{
  "class_label": "cat",
  "probability": 0.9532,
  "prediction_time_ms": 45.23
}
```

## Issues We Ran Into

1. **Docker image was huge** - Our first Docker build was over 3GB because we included all dev dependencies. Fixed it by using multi-stage builds and separating build-time and runtime requirements. Got it down to about 1.2GB.

2. **Kubernetes pods kept restarting** - The health checks were failing because the model takes time to load. Added `initialDelaySeconds: 30` to the readiness probe which solved it.

3. **CI pipeline timeout** - Tests were running too long because we were creating full models in tests. Changed to use smaller architectures and mock models where possible.

4. **Dataset versioning** - Can't commit 1GB of images to git. Set up DVC but ended up just documenting the download process clearly since we all needed to download from Kaggle anyway.

5. **Training time in CI** - Tried to train in the CI pipeline initially but it took forever. Moved training to a separate manual step and just test with a pre-trained model in CI.

## Useful Commands

We added a Makefile to simplify common tasks:

```bash
make install          # Install dependencies
make train            # Train model (20 epochs)
make test             # Run all tests
make docker-build     # Build Docker image
make docker-compose   # Start services
make k8s-deploy       # Deploy to Kubernetes
make mlflow           # Open MLflow UI
make clean            # Clean temporary files
```

## Project Structure

```
MLOPS_Assignment2_Group126/
├── src/                        # Source code
│   ├── train.py                # Training script with MLflow
│   ├── inference.py            # FastAPI service
│   ├── model.py                # CNN architecture
│   ├── data_preprocessing.py   # Data pipeline
│   ├── monitoring.py           # Metrics tracking
│   └── prepare_dataset.py      # Dataset splitting
├── tests/                      # Test suite
│   ├── test_preprocessing.py
│   ├── test_model.py
│   └── smoke_test.py
├── .github/workflows/          # CI/CD pipelines
│   ├── ci.yml
│   └── cd.yml
├── deployment/kubernetes/      # K8s manifests
│   └── deployment.yaml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Makefile
└── README.md
```

## Notes

- You need to train the model first before deploying (it's not in the repo)
- The Kaggle dataset requires a Kaggle account and API token
- CI/CD secrets need to be configured in GitHub for the pipelines to work
- We used Minikube for local K8s testing
- MLflow runs are stored in `mlruns/` directory locally

---

MLOps Assignment 2 - Group 126 - February 2026
