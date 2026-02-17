# Cats vs Dogs Classification - MLOps Pipeline

**GitHub Repository:** https://github.com/devaprasadp-bits/MLOPS_Assignment2_Group126

**Group 126** - MLOps Assignment 2 (S1-25_AIMLCZG523)

## Contributors:
- Devaprasad P           (2023aa05069@wilp.bits-pilani.ac.in)
- Devender Kumar         (2024aa05065@wilp.bits-pilani.ac.in)
- Chavali Amrutha Valli  (2024aa05610@wilp.bits-pilani.ac.in)
- Palakolanu Preethi     (2024aa05608@wilp.bits-pilani.ac.in)
- Rohan Tirthankar Behera(2024aa05607@wilp.bits-pilani.ac.in)

This project implements an end-to-end MLOps pipeline for binary image classification (Cats vs Dogs) for a pet adoption platform. The pipeline covers model development, experiment tracking with MLflow, containerization, automated CI/CD, Kubernetes deployment, and monitoring.

## What's Included

- Baseline CNN model for binary classification
- MLflow experiment tracking with automated metrics logging
- FastAPI REST API with health and prediction endpoints
- Docker containerization with multi-stage builds
- GitHub Actions CI/CD pipeline (automated testing, building, deployment)
- Kubernetes deployment manifests with auto-scaling
- Comprehensive unit tests (25+ tests with pytest)
- DVC for data version control
- Monitoring and logging infrastructure

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

## Prerequisites

- Python 3.9 or 3.10
- Docker and Docker Compose
- Git
- (Optional) kubectl and Minikube for Kubernetes deployment
- (Optional) DVC for data versioning

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/devaprasadp-bits/MLOPS_Assignment2_Group126.git
cd MLOPS_Assignment2_Group126

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
make install
# Or: pip install -r requirements.txt
```

### 2. Prepare Dataset

Download the Cats vs Dogs dataset from Kaggle:

```bash
# Install Kaggle CLI
pip install kaggle

# Download dataset (requires Kaggle API token in ~/.kaggle/)
kaggle competitions download -c dogs-vs-cats
unzip train.zip

# Organize dataset into train/validation/test splits
python src/prepare_dataset.py --source train --output data
```

**Dataset structure after preparation:**
```
data/
├── train/
│   ├── cats/      # 80% of cat images
│   └── dogs/      # 80% of dog images
├── validation/
│   ├── cats/      # 10% of cat images
│   └── dogs/      # 10% of dog images
└── test/
    ├── cats/      # 10% of cat images
    └── dogs/      # 10% of dog images
```

### 3. Train Model (Required)

**Note:** Model is not included in the repository. You must train before running the API.

```bash
# Train model with MLflow tracking
make train
# Or: python src/train.py --epochs 20 --batch_size 32

# For quick testing (5 epochs)
make train-quick
```

This will:
- Load and preprocess images (224x224 RGB)
- Train a CNN model with data augmentation
- Log experiments to MLflow (metrics, parameters, artifacts)
- Save the best model to `models/cats_dogs_model.h5`

### 4. View MLflow Experiments

```bash
make mlflow
# Or: mlflow ui --port 5000
```
Then open http://localhost:5000 to view training metrics, plots, and model artifacts.

## Running the Project

After completing the Quick Start setup above, you can explore different deployment options:

### 5. Run API Locally

**Prerequisites:** Complete step 3 (Train Model) first to create `models/cats_dogs_model.h5`.

```bash
# Start the API
make api
# Or: uvicorn src.inference:app --reload --port 8000
```

Test the API:
```bash
# Health check
curl http://localhost:8000/health

# Make prediction
curl -X POST "http://localhost:8000/predict" \
  -F "file=@path/to/cat_image.jpg"

# View interactive docs
open http://localhost:8000/docs
```

### 6. Docker

**Prerequisites:** Complete step 3 (Train Model) first.

Build and run with Docker:
```bash
make docker-build
make docker-run
```

Or use docker-compose (runs API + MLflow):
```bash
make docker-compose
# Or: docker-compose up -d
```

Access:
- API: http://localhost:8000
- MLflow: http://localhost:5000
- API Docs: http://localhost:8000/docs

Stop services:
```bash
make docker-stop
```

### 7. Kubernetes

**Prerequisites:** Complete step 3 (Train Model) and step 6 (Docker build) first.

Deploy to Kubernetes (Minikube):
```bash
# Start Minikube
minikube start

# Load Docker image into Minikube
minikube image load cats-dogs-classifier:latest

# Deploy application
make k8s-deploy
# Or: kubectl apply -f deployment/kubernetes/deployment.yaml

# Check status
make k8s-status
# Or: kubectl get pods -n mlops
```

Access the service:
```bash
# Get service URL
minikube service cats-dogs-service --url -n mlops

# Or port forward
kubectl port-forward -n mlops svc/cats-dogs-service 8000:80
```

Test scaling:
```bash
# Scale to 5 replicas
kubectl scale deployment cats-dogs-deployment --replicas=5 -n mlops

# Check pods
kubectl get pods -n mlops
```

## Testing

Run all tests:
```bash
make test
# Or: pytest tests/ -v --cov=src
```

Run smoke tests (post-deployment):
```bash
export API_URL=http://localhost:8000
make test-smoke
# Or: python tests/smoke_test.py
```

Test results: 25+ unit tests covering preprocessing, model architecture, and inference.

## CI/CD Pipeline

The project includes automated GitHub Actions workflows:

### Continuous Integration (CI)
**Trigger:** Push or PR to main/develop branch

Pipeline steps:
1. Checkout code
2. Set up Python 3.9
3. Install dependencies
4. Run unit tests with coverage
5. Build Docker image
6. Push image to Docker Hub (on main branch)

### Continuous Deployment (CD)
**Trigger:** After successful CI on main branch

Pipeline steps:
1. Pull latest Docker image
2. Update Kubernetes deployment
3. Wait for rollout completion
4. Run smoke tests
5. Rollback on failure

**Required GitHub Secrets:**
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub access token
- `KUBE_CONFIG` - Base64-encoded Kubernetes config
- `API_URL` - Deployed API URL for smoke tests

## Model Architecture

**CNN Baseline Model:**
- Input: 224x224x3 RGB images
- Conv2D layers: 32, 64, 128, 128 filters
- MaxPooling after each conv block
- Flatten + Dense(512) + Dropout(0.5)
- Output: Dense(1) with sigmoid activation

**Training Configuration:**
- Optimizer: Adam (lr=0.001)
- Loss: Binary crossentropy
- Metrics: Accuracy, Precision, Recall
- Data Augmentation: Rotation, flip, zoom, shift
- EarlyStopping: patience=5 on val_loss
- ReduceLROnPlateau: factor=0.5, patience=3

## Expected Results

**Model Performance:**
- Training Accuracy: ~94%
- Validation Accuracy: ~92%
- Test Accuracy: ~90-91%
- Model Size: ~50MB
- Inference Time: ~45ms per image

**System Performance:**
- API Latency: <100ms (average)
- Throughput: ~20 requests/second (single instance)
- Container Size: ~1.2GB (optimized multi-stage build)

## API Endpoints

| Endpoint | Method | Description | Request | Response |
|----------|--------|-------------|---------|----------|
| `/` | GET | Root endpoint | - | API information |
| `/health` | GET | Health check | - | Status, metrics |
| `/predict` | POST | Classify image | image file | class, probability |
| `/docs` | GET | API documentation | - | Swagger UI |

**Example Response:**
```json
{
  "class_label": "cat",
  "probability": 0.9532,
  "prediction_time_ms": 45.23,
  "timestamp": "2026-02-18T10:30:45.123456"
}
```

## Monitoring and Logging

The application includes:
- Structured JSON logging for all requests
- Request/response tracking with timestamps  
- Performance metrics (latency, throughput)
- Health check endpoint with system metrics
- Post-deployment performance tracking

Logs are stored in `logs/` directory and excluded from git.

## Makefile Commands

Quick reference for common tasks:

```bash
make help              # Show all available commands
make install           # Install dependencies
make train             # Train model (20 epochs)
make train-quick       # Quick training (5 epochs)
make test              # Run unit tests
make test-smoke        # Run smoke tests
make docker-build      # Build Docker image
make docker-compose    # Start all services
make k8s-deploy        # Deploy to Kubernetes
make mlflow            # Start MLflow UI
make api               # Run API locally
make clean             # Clean cache files
make lint              # Run code linters
make format            # Format code
```

## Problems We Faced

1. **TensorFlow GPU compatibility**: Initial model training was slow on CPU. Optimized by reducing batch size and using data generators efficiently.

2. **Docker image size**: First build was >3GB. Fixed by using multi-stage builds and cleaning up unnecessary files, reduced to ~1.2GB.

3. **Kubernetes health checks**: Pods were restarting due to slow model loading. Added `initialDelaySeconds: 30` to probes.

4. **CI pipeline timeout**: Tests were timing out due to model creation. Reduced test epochs and used smaller test images.

5. **Data versioning**: Large dataset (~1GB) couldn't be in git. Implemented DVC for data tracking and documented download process.

## Dataset Information

**Source:** Kaggle - Dogs vs. Cats Dataset  
**Total Images:** 25,000 labeled images  
**Split:** 80% train (20,000), 10% validation (2,500), 10% test (2,500)  
**Format:** JPEG images (variable sizes, resized to 224x224)  
**Classes:** Binary (cats=0, dogs=1)  
**Preprocessing:** RGB conversion, resizing, normalization [0,1]  
**Augmentation:** Random rotation, flips, zoom (training only)

## Notes

- Model training must be completed before API deployment
- DVC is configured but requires remote storage setup
- CI/CD pipeline requires GitHub secrets for Docker Hub and Kubernetes
- Use `internal/` folder for development notes (gitignored)
- MLflow runs are stored in `mlruns/` directory
- Docker image needs to be pushed to registry for Kubernetes deployment

---

MLOps Assignment 2 - February 2026
