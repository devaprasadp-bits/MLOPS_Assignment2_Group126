# Assignment 2 - Reviewer Checklist

## Module 1: Model Development & Experiment Tracking (10M)

### ✅ Data & Code Versioning
- [x] Git for source code versioning
  - Files: `.git/`, `.gitignore`, commit history
  - Verify: `git log --oneline`
- [x] DVC for dataset versioning
  - Files: `.dvc/`, `data.dvc`
  - Verify: `dvc status`

### ✅ Model Building
- [x] Baseline CNN model implemented
  - File: `src/model.py` (build_baseline_cnn function)
  - Architecture: 4 conv blocks with pooling
- [x] Model saved in standard format (.h5)
  - Location: `models/cats_dogs_model.h5` (after training)
  - Verify: Run `python src/train.py --epochs 5`

### ✅ Experiment Tracking
- [x] MLflow integration
  - File: `src/train.py` (mlflow.start_run, mlflow.log_param, mlflow.log_metric)
  - Logs: parameters, metrics, artifacts
- [x] Tracks confusion matrix and loss curves
  - Verify: Run training, check `mlflow ui`

---

## Module 2: Model Packaging & Containerization (10M)

### ✅ Inference Service
- [x] REST API with FastAPI
  - File: `src/inference.py`
- [x] Health check endpoint
  - Endpoint: `GET /health`
  - Returns: status, model_loaded, timestamp
- [x] Prediction endpoint
  - Endpoint: `POST /predict`
  - Input: image file
  - Output: class_label, probability, timestamp
  - Verify: `curl -X POST http://localhost:8000/predict -F "file=@image.jpg"`

### ✅ Environment Specification
- [x] requirements.txt with pinned versions
  - File: `requirements.txt`
  - Check: All key libraries have version numbers

### ✅ Containerization
- [x] Dockerfile created
  - File: `Dockerfile`
  - Multi-stage build: builder + runtime
  - Non-root user execution
- [x] Docker image builds successfully
  - Verify: `docker build -t cats-dogs-classifier:latest .`
- [x] Container runs and serves predictions
  - Verify: `docker run -p 8000:8000 cats-dogs-classifier:latest`
  - Test: `curl http://localhost:8000/health`

---

## Module 3: CI Pipeline (10M)

### ✅ Automated Testing
- [x] Unit tests for data preprocessing
  - File: `tests/test_preprocessing.py`
  - Functions: test_load_and_preprocess_image, test_preprocess_image_bytes, etc.
- [x] Unit tests for model utilities/inference
  - File: `tests/test_model.py`
  - Functions: test_model_architecture, test_model_predictions, etc.
- [x] Tests run via pytest
  - Verify: `pytest tests/ -v`

### ✅ CI Setup (GitHub Actions)
- [x] CI workflow defined
  - File: `.github/workflows/ci.yml`
  - Triggers: push, pull_request to main/develop
- [x] Pipeline checks out repository
  - Step: actions/checkout@v3
- [x] Pipeline installs dependencies
  - Step: pip install -r requirements.txt
- [x] Pipeline runs unit tests
  - Step: pytest tests/
- [x] Pipeline builds Docker image
  - Step: docker/build-push-action@v4

### ✅ Artifact Publishing
- [x] Docker image pushed to registry (Docker Hub)
  - Registry: devaprasadp/cats-dogs-classifier
  - Condition: Only on main branch
  - Verify: Check Docker Hub after push to main

---

## Module 4: CD Pipeline & Deployment (10M)

### ✅ Deployment Target
- [x] Kubernetes chosen as deployment target
  - Local cluster: Minikube/kind/microk8s
- [x] Infrastructure manifests defined
  - File: `deployment/kubernetes/deployment.yaml`
  - Includes: Namespace, Deployment, Service

### ✅ Deployment Manifest Details
- [x] Namespace: cats-dogs or mlops
- [x] Deployment with replicas (2)
- [x] Service type: LoadBalancer
- [x] Health probes configured
  - Liveness probe: /health endpoint
  - Readiness probe: /health endpoint with initial delay
- [x] Resource limits defined
  - Memory: 1Gi, CPU: 1000m

### ✅ CD / GitOps Flow
- [x] CD workflow defined
  - File: `.github/workflows/cd.yml`
  - Triggers: After CI success on main
- [x] Pulls new image from registry
  - Step: kubectl set image
- [x] Deploys/updates service automatically
  - Step: kubectl rollout status
- [x] Only on main branch changes
  - Condition: github.ref == 'refs/heads/main'

### ✅ Smoke Tests / Health Check
- [x] Post-deploy smoke test implemented
  - File: `tests/smoke_test.py`
  - Tests: /health endpoint returns 200
  - Tests: /predict endpoint works with sample image
- [x] Pipeline fails if smoke tests fail
  - Verify: Check CD workflow exit codes

---

## Module 5: Monitoring, Logs & Submission (10M)

### ✅ Basic Monitoring & Logging
- [x] Request/response logging enabled
  - File: `src/inference.py` (logging.info statements)
  - Format: Structured with timestamps
- [x] Excludes sensitive data
  - Check: No passwords, tokens, or PII in logs
- [x] Tracks request count and latency
  - File: `src/monitoring.py` (ModelMonitor class)
  - Metrics: total_predictions, avg_confidence, processing_time

### ✅ Model Performance Tracking
- [x] Monitoring class for post-deployment tracking
  - File: `src/monitoring.py`
  - Tracks: predictions, confidence scores, class distribution
- [x] Can collect requests and true labels
  - Methods: log_prediction, track_batch_performance

---

## Deliverables

### ✅ Deliverable 1: Zip File Contents
Repository should contain:
- [x] Source code (`src/` directory)
- [x] Configuration files
  - [x] DVC config (`.dvc/`, `data.dvc`)
  - [x] CI/CD workflows (`.github/workflows/`)
  - [x] Docker (`Dockerfile`, `docker-compose.yml`)
  - [x] Kubernetes (`deployment/kubernetes/`)
- [x] Trained model artifacts
  - Note: Model created after running `python src/train.py`
  - Location: `models/cats_dogs_model.h5`

### ✅ Deliverable 2: Screen Recording
- [ ] Video < 5 minutes
- [ ] Demonstrates complete workflow:
  - [ ] Code change
  - [ ] Git push
  - [ ] CI pipeline triggered
  - [ ] Tests run and pass
  - [ ] Docker image built
  - [ ] Image pushed to registry
  - [ ] CD pipeline triggered
  - [ ] Deployment updated
  - [ ] Live prediction from deployed model

---

## Testing Instructions for Reviewer

### Step 1: Environment Setup (5 minutes)
```bash
# Clone repository
git clone https://github.com/devaprasadp-bits/MLOPS_Assignment2_Group126.git
cd MLOPS_Assignment2_Group126

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get Dataset (10 minutes)
```bash
# Install Kaggle CLI
pip install kaggle

# Download (requires Kaggle API token)
kaggle competitions download -c dogs-vs-cats
unzip train.zip

# Prepare dataset
python src/prepare_dataset.py --source train --output data
```

### Step 3: Train Model (30-60 minutes)
```bash
# Quick training (5 epochs for testing)
python src/train.py --epochs 5 --batch_size 32

# View MLflow UI
mlflow ui --port 5000
# Open http://localhost:5000
```

### Step 4: Test API Locally (2 minutes)
```bash
# Start API
uvicorn src.inference:app --reload --port 8000

# In another terminal, test endpoints
curl http://localhost:8000/health
curl -X POST "http://localhost:8000/predict" -F "file=@data/test/cats/cat.0.jpg"
```

### Step 5: Run Tests (2 minutes)
```bash
pytest tests/ -v --cov=src
```

### Step 6: Docker Testing (5 minutes)
```bash
# Build image
docker build -t cats-dogs-classifier:latest .

# Run container
docker run -p 8000:8000 cats-dogs-classifier:latest

# Test
curl http://localhost:8000/health
```

### Step 7: Kubernetes Deployment (10 minutes)
```bash
# Start Minikube
minikube start

# Load image
minikube image load cats-dogs-classifier:latest

# Deploy
kubectl apply -f deployment/kubernetes/deployment.yaml

# Check status
kubectl get pods -n cats-dogs
kubectl get svc -n cats-dogs

# Access service
minikube service cats-dogs-service --url -n cats-dogs
```

### Step 8: Smoke Tests (2 minutes)
```bash
export API_URL=http://localhost:8000
python tests/smoke_test.py
```

---

## Scoring Summary

| Module | Max Marks | Checklist Items | Status |
|--------|-----------|-----------------|--------|
| M1: Model Development & Experiment Tracking | 10 | 6 requirements | ✅ All met |
| M2: Model Packaging & Containerization | 10 | 6 requirements | ✅ All met |
| M3: CI Pipeline | 10 | 7 requirements | ✅ All met |
| M4: CD Pipeline & Deployment | 10 | 9 requirements | ✅ All met |
| M5: Monitoring & Logging | 10 | 5 requirements | ✅ All met |
| **Total** | **50** | **33 items** | **✅ 32/33** |

**Missing:** Video recording (will be created after deployment)

---

## Common Issues & Solutions

### Issue 1: Import errors when running code
**Solution:** Install dependencies first: `pip install -r requirements.txt`

### Issue 2: Model not found error
**Solution:** Train model first: `python src/train.py --epochs 5`

### Issue 3: Kaggle dataset download fails
**Solution:** 
1. Create Kaggle account
2. Get API token from kaggle.com/account
3. Place in `~/.kaggle/kaggle.json`
4. Run: `chmod 600 ~/.kaggle/kaggle.json`

### Issue 4: Docker build fails
**Solution:** Ensure model is trained first (needs `models/cats_dogs_model.h5`)

### Issue 5: Kubernetes pods not starting
**Solution:** 
1. Check image is loaded: `minikube image ls | grep cats-dogs`
2. Load if missing: `minikube image load cats-dogs-classifier:latest`
3. Check logs: `kubectl logs -n cats-dogs <pod-name>`

### Issue 6: CI/CD not running
**Solution:** 
1. Check GitHub Actions is enabled in repo settings
2. Configure required secrets:
   - DOCKER_USERNAME
   - DOCKER_PASSWORD
   - KUBE_CONFIG
   - API_URL

---

## Verification Commands

Quick commands to verify each module:

```bash
# M1: Check experiment tracking
mlflow ui --port 5000

# M2: Check API
curl http://localhost:8000/docs

# M3: Run tests
pytest tests/ -v

# M4: Check K8s deployment
kubectl get all -n cats-dogs

# M5: Check logs
kubectl logs -n cats-dogs deployment/cats-dogs-api --tail=50
```
