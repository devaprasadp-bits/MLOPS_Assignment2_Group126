#!/bin/bash
set -e

echo "=== Building Docker image with Python 3.11 ==="
docker build -t mlops_assignment2_group126-cats-dogs-api:latest .

echo ""
echo "=== Starting service ==="
docker-compose up -d cats-dogs-api

echo ""
echo "=== Waiting for service to start (15 seconds) ==="
sleep 15

echo ""
echo "=== Testing health endpoint ==="
curl -s http://localhost:8000/health | jq

echo ""
echo "=== Testing root endpoint ==="
curl -s http://localhost:8000/ | jq

echo ""
echo "✓ All tests passed!"
echo "API is running at http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
echo ""
echo "To stop: docker-compose down"
