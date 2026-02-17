# MLOps Pipeline - Cats vs Dogs Classification

## Project Overview
This project implements an end-to-end MLOps pipeline for binary image classification (Cats vs Dogs) for a pet adoption platform. The pipeline includes model development, experiment tracking, containerization, CI/CD, and deployment.

## Architecture
```
├── data/                      # Dataset (tracked by DVC)
├── src/                       # Source code
│   ├── data_preprocessing.py  # Data loading and preprocessing
│   ├── model.py              # Model architecture
│   ├── train.py              # Training script
│   └── inference.py          # Inference service (FastAPI)
├── tests/                    # Unit tests
├── models/                   # Trained model artifacts
├── deployment/              # Kubernetes/Docker deployment configs
├── .github/workflows/       # CI/CD pipelines
├── Dockerfile              # Container specification
├── docker-compose.yml      # Local deployment
└── requirements.txt        # Python dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.9+
- Docker
- Git
- DVC

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd MLOPS_Assignment2_Group126

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize DVC
dvc pull
```

### Training the Model
```bash
# Train with MLflow tracking
python src/train.py
```

### Running Tests
```bash
pytest tests/ -v
```

### Local Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Test the API
curl http://localhost:8000/health
```

### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f deployment/kubernetes/

# Check deployment status
kubectl get pods
kubectl get svc
```

## API Endpoints

### Health Check
```bash
GET /health
```

### Prediction
```bash
POST /predict
Content-Type: multipart/form-data
Body: image file

Response: {"class": "cat", "probability": 0.95}
```

## CI/CD Pipeline

The pipeline automatically:
1. Runs unit tests on every push
2. Builds Docker image
3. Pushes image to registry
4. Deploys to Kubernetes cluster
5. Runs smoke tests

## Monitoring

- Request/response logging enabled
- Metrics tracked: request count, latency, accuracy
- Logs available via container logs

## Dataset

**Source**: Kaggle Cats and Dogs Dataset  
**Preprocessing**: 224x224 RGB images  
**Split**: 80% train, 10% validation, 10% test  
**Augmentation**: Random rotation, flip, zoom

## Model

**Architecture**: Convolutional Neural Network (CNN)  
**Framework**: TensorFlow/Keras  
**Input**: 224x224x3 RGB images  
**Output**: Binary classification (cat/dog)

## Experiment Tracking

All experiments tracked using MLflow:
- Parameters (learning rate, batch size, epochs)
- Metrics (accuracy, loss, precision, recall)
- Artifacts (model weights, confusion matrix, training curves)

## Team: Group 126

Course: MLOps (S1-25_AIMLCZG523)  
Assignment: 2
