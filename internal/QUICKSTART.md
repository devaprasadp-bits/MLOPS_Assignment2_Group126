# Quick Start Guide - Cats vs Dogs Classifier

⏱️ **Get running in 5 minutes!**

## Prerequisites
- Docker installed and running
- 4GB free disk space
- Port 8000 available

## Option 1: Docker (Simplest)

```bash
# Build the image (~4-5 minutes first time)
docker build -t cats-dogs-classifier:latest .

# Run the container
docker run -d --name cats-dogs-api -p 8000:8000 cats-dogs-classifier:latest

# Test it!
open http://localhost:8000/docs
```

**In the browser:**
1. Go to http://localhost:8000/docs
2. Click on `POST /predict` → "Try it out"
3. Upload any cat or dog image
4. Click "Execute"
5. See the prediction!

**Stop the container:**
```bash
docker stop cats-dogs-api
docker rm cats-dogs-api
```

## Option 2: Run Tests

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Expected: 25 tests pass
```

## Option 3: Kubernetes (Advanced)

```bash
# Start Minikube
minikube start

# Load the Docker image
minikube image load cats-dogs-classifier:latest

# Deploy
kubectl apply -f deployment/kubernetes/deployment.yaml

# Check deployment
kubectl get pods -n mlops
kubectl get svc -n mlops

# Get service URL
minikube service cats-dogs-service -n mlops --url

# Test (replace URL with output from above)
curl http://<MINIKUBE-IP>:<PORT>/health
```

## Troubleshooting

**Port 8000 already in use:**
```bash
docker stop $(docker ps -q --filter "publish=8000")
```

**Docker build fails:**
```bash
docker system prune -a
docker build -t cats-dogs-classifier:latest . --no-cache
```

**Model predictions are random (~50%):**
This is expected! We're using an untrained model for infrastructure testing. The MLOps pipeline is what matters, not the model accuracy.

## What's Included

✅ FastAPI REST API with Swagger UI  
✅ Docker containerization  
✅ Kubernetes deployment manifests  
✅ 25 unit tests (pytest)  
✅ Health monitoring endpoints  
✅ Structured logging  

## Next Steps

- **See Full Documentation:** [README.md](README.md)
- **View Test Results:** [TESTING_SUMMARY.md](TESTING_SUMMARY.md)
- **CI/CD Setup:** `.github/workflows/`

---

**Group 126** | MLOps Assignment 2
