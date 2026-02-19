#!/bin/bash
# Docker verification and testing script

echo "🔍 Checking Docker status..."
echo ""

# Test 1: Docker daemon
if docker info > /dev/null 2>&1; then
    echo "✅ Docker daemon is running"
    docker version --format 'Client: {{.Client.Version}} | Server: {{.Server.Version}}'
else
    echo "❌ Docker daemon not responding"
    exit 1
fi

echo ""
echo "🐳 Checking containers and images..."
echo ""

# Test 2: List containers
echo "Containers:"
docker ps -a

echo ""
echo "Images:"
docker images | head -10

echo ""
echo "✅ Docker is healthy and ready!"
