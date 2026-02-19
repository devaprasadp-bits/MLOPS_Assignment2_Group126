# API Testing Examples

## Using cURL

### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

Expected Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_path": "models/cats_dogs_model.h5",
  "requests_served": 0,
  "average_latency_ms": 0
}
```

### Prediction
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@path/to/cat_image.jpg"
```

Expected Response:
```json
{
  "class_label": "cat",
  "probability": 0.9532,
  "prediction_time_ms": 45.23,
  "timestamp": "2026-02-18T10:30:45.123456"
}
```

## Using Python

### Health Check
```python
import requests

response = requests.get("http://localhost:8000/health")
print(response.json())
```

### Prediction
```python
import requests

# Single prediction
with open("test_image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/predict", files=files)
    print(response.json())
```

### Batch Predictions
```python
import requests
from pathlib import Path

def predict_image(image_path):
    """Make prediction for a single image."""
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post("http://localhost:8000/predict", files=files)
        return response.json()

# Predict multiple images
image_dir = Path("data/test/cats")
for image_path in image_dir.glob("*.jpg"):
    result = predict_image(image_path)
    print(f"{image_path.name}: {result['class_label']} ({result['probability']:.4f})")
```

## Using Postman

1. **Health Check**
   - Method: GET
   - URL: http://localhost:8000/health
   - Click Send

2. **Prediction**
   - Method: POST
   - URL: http://localhost:8000/predict
   - Body: form-data
   - Key: file (type: File)
   - Value: Select an image file
   - Click Send

## Using HTTPie

### Install HTTPie
```bash
pip install httpie
```

### Health Check
```bash
http GET http://localhost:8000/health
```

### Prediction
```bash
http -f POST http://localhost:8000/predict file@cat_image.jpg
```

## Performance Testing

### Using Apache Bench (ab)
```bash
# Install (macOS)
brew install apache-bench

# Load test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health
```

### Using Python script
```python
import requests
import time
from concurrent.futures import ThreadPoolExecutor

def make_request():
    """Make a health check request."""
    start = time.time()
    response = requests.get("http://localhost:8000/health")
    latency = (time.time() - start) * 1000
    return response.status_code, latency

# Run 100 concurrent requests
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(lambda _: make_request(), range(100)))

# Calculate statistics
statuses = [r[0] for r in results]
latencies = [r[1] for r in results]

print(f"Total requests: {len(results)}")
print(f"Successful: {sum(1 for s in statuses if s == 200)}")
print(f"Average latency: {sum(latencies)/len(latencies):.2f}ms")
print(f"Min latency: {min(latencies):.2f}ms")
print(f"Max latency: {max(latencies):.2f}ms")
```

## Error Handling

### Invalid File Type
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@document.txt"
```

Response:
```json
{
  "detail": "File must be an image"
}
```

### No Model Loaded
Response:
```json
{
  "detail": "Model not loaded"
}
```

## Integration Test Script

```python
#!/usr/bin/env python3
"""Integration test for API endpoints."""

import requests
import sys
from io import BytesIO
from PIL import Image

API_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint."""
    response = requests.get(f"{API_URL}/")
    assert response.status_code == 200
    print("✓ Root endpoint working")

def test_health():
    """Test health endpoint."""
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data
    print("✓ Health endpoint working")

def test_prediction():
    """Test prediction endpoint."""
    # Create test image
    img = Image.new('RGB', (224, 224), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    # Make prediction
    files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
    response = requests.post(f"{API_URL}/predict", files=files)
    assert response.status_code == 200
    
    data = response.json()
    assert "class_label" in data
    assert "probability" in data
    assert data["class_label"] in ["cat", "dog"]
    print("✓ Prediction endpoint working")

if __name__ == "__main__":
    try:
        test_root()
        test_health()
        test_prediction()
        print("\n✓ All tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
```
