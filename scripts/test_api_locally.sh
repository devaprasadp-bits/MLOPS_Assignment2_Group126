#!/bin/bash
# Script to test the API locally without Docker

echo "🚀 Starting API locally with uvicorn..."
echo ""

# Check if model exists
if [ ! -f "models/cats_dogs_model.h5" ]; then
    echo "❌ Model not found! The pre-trained model should be in models/"
    echo "Or train a new one: python src/train.py --epochs 5 --batch_size 16"
    exit 1
fi

# Start the API
python -m uvicorn src.inference:app --host 0.0.0.0 --port 8000 &
API_PID=$!

echo "⏳ Waiting for API to start (5 seconds)..."
sleep 5

echo ""
echo "✅ Testing API endpoints..."
echo ""

# Test health endpoint
echo "1️⃣ Testing /health endpoint:"
curl -s http://localhost:8000/health | python -m json.tool
echo ""

# Test root endpoint
echo ""
echo "2️⃣ Testing / endpoint:"
curl -s http://localhost:8000/ | python -m json.tool
echo ""

# Download test image if not exists
if [ ! -f "test_cat.jpg" ]; then
    echo ""
    echo "📥 Downloading test image..."
    curl -s -o test_cat.jpg "https://placekitten.com/224/224"
    echo "✅ Test image downloaded"
fi

# Test prediction endpoint
echo ""
echo "3️⃣ Testing /predict endpoint:"
curl -s -X POST "http://localhost:8000/predict" -F "file=@test_cat.jpg" | python -m json.tool
echo ""

echo ""
echo "✅ All tests completed!"
echo ""
echo "API is running on PID: $API_PID"
echo "To stop: kill $API_PID"
echo "Or press Ctrl+C"
echo ""

# Keep script running
wait $API_PID
