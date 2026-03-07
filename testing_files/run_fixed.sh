#!/bin/bash

echo "================================"
echo "HR Agent - Fixed Startup Script"
echo "================================"
echo ""

# Stop any existing containers
echo "Stopping existing containers..."
docker stop hr-agent-test 2>/dev/null || true
docker rm hr-agent-test 2>/dev/null || true

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ ERROR: .env file not found"
    echo "Please create .env file with:"
    echo "  OPENAI_API_KEY=sk-proj-..."
    echo "  MONGODB_URI=mongodb+srv://..."
    echo "  MONGODB_DATABASE=HR-Database"
    exit 1
fi

echo "✅ Found .env file"
echo ""

# Run with correct configuration
echo "Starting HR Agent with correct configuration..."
docker run -d \
  --name hr-agent-test \
  --env-file .env \
  -p 5000:5000 \
  --dns 8.8.8.8 \
  --dns 8.8.4.4 \
  hr-agent

if [ $? -eq 0 ]; then
    echo "✅ Container started"
    echo ""
    echo "Waiting for startup..."
    sleep 5
    
    echo ""
    echo "Checking logs..."
    docker logs hr-agent-test 2>&1 | tail -20
    
    echo ""
    echo "================================"
    echo "Testing connection..."
    echo "================================"
    
    # Test health endpoint
    echo ""
    echo "1. Health check:"
    curl -s http://localhost:5000/health || echo "❌ Health check failed"
    
    echo ""
    echo ""
    echo "2. Simple test request:"
    curl -s -X POST http://localhost:5000/ \
      -H "Content-Type: application/json" \
      -d '{
        "jsonrpc": "2.0",
        "id": "test-1",
        "method": "message/send",
        "params": {
          "message": {
            "role": "user",
            "parts": [
              {
                "kind": "text",
                "text": "Hello, can you help me?"
              }
            ]
          }
        }
      }' | head -c 200
    
    echo ""
    echo ""
    echo "================================"
    echo "HR Agent is ready!"
    echo "================================"
    echo ""
    echo "View logs: docker logs -f hr-agent-test"
    echo "Run tests: ./test_requests.sh"
    echo ""
else
    echo "❌ Failed to start container"
    exit 1
fi
