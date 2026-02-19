# Quick Start Guide for Reviewers

## Important: Python Version Requirement

**This project requires Python 3.9, 3.10, or 3.11**  
TensorFlow 2.13.0 does NOT support Python 3.12 or 3.13.

If you see `ModuleNotFoundError: No module named 'tensorflow'`, you're likely using an incompatible Python version.

### Check Your Python Version

```bash
python3 --version
```

If you have Python 3.12 or 3.13, you need to install Python 3.11:

**macOS (with Homebrew):**
```bash
brew install python@3.11
```

**Ubuntu/Debian:**
```bash
sudo apt-get install python3.11 python3.11-venv
```

## Step-by-Step Setup (5 minutes)

### 1. Create Virtual Environment

```bash
# Use Python 3.11 (or 3.10 or 3.9)
python3.11 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This takes 5-10 minutes due to TensorFlow being large (~450MB).

### 3. Verify Setup

```bash
python internal/verify_setup.py
```

You should see: ✓ All checks passed! (21/21)

### 4. Run Tests (Without Dataset)

```bash
pytest tests/ -v
```

Note: Some tests need a trained model, so they'll be skipped. This is expected.

## Quick Test Run (Without Full Dataset)

If you want to test quickly without downloading the full 1GB dataset:

### Option 1: Run Tests Only
```bash
pytest tests/ -v --tb=short
```

### Option 2: Quick Training Test
```bash
# Create minimal test data
mkdir -p data/train/{cats,dogs} data/validation/{cats,dogs} data/test/{cats,dogs}

# This will fail gracefully if no images, but tests code paths
python src/train.py --epochs 1 || echo "Expected: needs actual images"
```

### Option 3: Test API with Dummy Model
```bash
# Create a minimal dummy model file
python -c "import tensorflow as tf; model=tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(150,150,3))]); model.save('models/cats_dogs_model.h5')"

# Start API
uvicorn src.inference:app --reload --port 8000 &

# Test endpoints
sleep 3
curl http://localhost:8000/health

# Kill API
pkill -f uvicorn
```

## Full Workflow (With Dataset - 60+ minutes)

### 1. Get Kaggle Dataset

```bash
# Install Kaggle CLI
pip install kaggle

# Set up Kaggle credentials (~/.kaggle/kaggle.json)
# Get from: https://www.kaggle.com/account

# Download dataset
kaggle competitions download -c dogs-vs-cats
unzip train.zip
```

### 2. Prepare Dataset

```bash
python src/prepare_dataset.py --source train --output data
```

This creates:
- data/train/{cats,dogs} - 20,000 images
- data/validation/{cats,dogs} - 2,500 images
- data/test/{cats,dogs} - 2,500 images

### 3. Train Model

```bash
# Full training (20 epochs, ~45-60 minutes on CPU)
python src/train.py --epochs 20 --batch_size 32

# Quick test (5 epochs, ~10-15 minutes)
python src/train.py --epochs 5 --batch_size 32
```

### 4. View Experiments

```bash
mlflow ui --port 5000
```

Open: http://localhost:5000

### 5. Test API

```bash
# Start API
uvicorn src.inference:app --reload --port 8000

# In another terminal
curl http://localhost:8000/health

curl -X POST "http://localhost:8000/predict" \
  -F "file=@data/test/cats/cat.1.jpg"
```

### 6. Run All Tests

```bash
pytest tests/ -v --cov=src
```

### 7. Docker Build & Run

```bash
docker build -t cats-dogs-classifier:latest .
docker run -p 8000:8000 cats-dogs-classifier:latest
```

Test: `curl http://localhost:8000/health`

### 8. Kubernetes Deployment

```bash
# Start Minikube
minikube start

# Load image
minikube image load cats-dogs-classifier:latest

# Deploy
kubectl apply -f deployment/kubernetes/deployment.yaml

# Check status
kubectl get pods -n mlops
kubectl get svc -n mlops

# Access service
minikube service cats-dogs-service --url -n mlops

# Test
curl $(minikube service cats-dogs-service --url -n mlops)/health
```

## Common Issues

### Issue: ImportError: No module named 'tensorflow'
**Cause:** Wrong Python version (3.12 or 3.13)  
**Fix:** Use Python 3.9, 3.10, or 3.11

### Issue: Model file not found
**Cause:** Haven't trained model yet  
**Fix:** Run `python src/train.py --epochs 5` first

### Issue: No images found during training
**Cause:** Dataset not prepared  
**Fix:** Run `python src/prepare_dataset.py` first

### Issue: Kaggle 401 Unauthorized
**Cause:** Kaggle API credentials not set up  
**Fix:** 
1. Go to https://www.kaggle.com/account
2. Create API token
3. Save to ~/.kaggle/kaggle.json
4. Run: `chmod 600 ~/.kaggle/kaggle.json`

### Issue: Docker build fails - COPY models/
**Cause:** Models directory is empty  
**Fix:** Train model first, or the CI creates a dummy file for build testing

### Issue: K8s pods CrashLoopBackOff
**Cause:** Image not loaded in Minikube  
**Fix:** `minikube image load cats-dogs-classifier:latest`

## Scoring Checklist

Use this to quickly verify all requirements are met:

- [ ] **M1: Model Development** - src/model.py, src/train.py exist
- [ ] **M1: Experiment Tracking** - MLflow integration in train.py
- [ ] **M1: Data Versioning** - data.dvc file exists
- [ ] **M2: REST API** - src/inference.py with /health and /predict
- [ ] **M2: Containerization** - Dockerfile and docker-compose.yml exist
- [ ] **M2: Dependencies** - requirements.txt with pinned versions
- [ ] **M3: Unit Tests** - tests/test_*.py files (2+)
- [ ] **M3: CI Pipeline** - .github/workflows/ci.yml runs tests and builds
- [ ] **M3: Docker Publish** - CI pushes to Docker Hub on main branch
- [ ] **M4: K8s Manifests** - deployment/kubernetes/deployment.yaml
- [ ] **M4: CD Pipeline** - .github/workflows/cd.yml deploys after CI
- [ ] **M4: Smoke Tests** - tests/smoke_test.py runs post-deploy
- [ ] **M5: Logging** - Structured logging in src/inference.py
- [ ] **M5: Monitoring** - src/monitoring.py tracks metrics

Run: `python internal/verify_setup.py` to auto-check all items.

## Time Estimates

- **Setup environment:** 5-10 minutes
- **Download dataset:** 10-15 minutes (depends on internet speed)
- **Prepare dataset:** 2-3 minutes
- **Train model (5 epochs):** 10-15 minutes on modern laptop
- **Train model (20 epochs):** 45-60 minutes on modern laptop
- **Run tests:** 30-60 seconds
- **Docker build:** 3-5 minutes
- **K8s deployment:** 2-3 minutes
- **Total (quick verification):** ~20-30 minutes without training
- **Total (full workflow):** ~90-120 minutes with training

## Binary Submission Checklist

What should be in the zip file:

✓ Source code (src/)
✓ Tests (tests/)
✓ CI/CD workflows (.github/workflows/)
✓ Docker files (Dockerfile, docker-compose.yml)
✓ K8s manifests (deployment/kubernetes/)
✓ Configuration (requirements.txt, setup.cfg, Makefile)
✓ Documentation (README.md)
✓ DVC files (.dvc/, data.dvc)
✓ Git repository (.git/)

✗ Not needed: venv/, __pycache__/, .pytest_cache/, mlruns/, logs/, internal/
✗ Not included: Trained model (too large, created during training)
✗ Not included: Dataset (1GB, downloaded from Kaggle)

## Contact

If you encounter issues not covered here, check:
1. Python version (must be 3.9-3.11)
2. Virtual environment is activated
3. All dependencies installed
4. README.md for detailed instructions
