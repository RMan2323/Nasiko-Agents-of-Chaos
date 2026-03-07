#!/bin/bash

# Run HR Agent with all environment variables
# Usage: ./run_agent.sh

echo "Starting HR Agent..."
echo ""

# Load .env file if it exists
if [ -f .env ]; then
    echo "Loading environment from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment loaded from .env"
else
    echo "ℹ️  No .env file found, using environment variables"
fi

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ ERROR: OPENAI_API_KEY is not set"
    echo "Please either:"
    echo "  1. Create a .env file with OPENAI_API_KEY=sk-proj-..."
    echo "  2. Or export OPENAI_API_KEY=sk-proj-..."
    exit 1
fi

echo "✅ OPENAI_API_KEY is set"

# Set MongoDB defaults if not set
if [ -z "$MONGODB_URI" ]; then
    export MONGODB_URI="mongodb://localhost:27017/"
    echo "ℹ️  Using default MONGODB_URI: $MONGODB_URI"
fi

if [ -z "$MONGODB_DATABASE" ]; then
    export MONGODB_DATABASE="hr_agent"
    echo "ℹ️  Using default MONGODB_DATABASE: $MONGODB_DATABASE"
fi

echo ""
echo "Configuration:"
echo "  OPENAI_API_KEY: ${OPENAI_API_KEY:0:20}..."
echo "  MONGODB_URI: ${MONGODB_URI:0:50}..."
echo "  MONGODB_DATABASE: $MONGODB_DATABASE"
echo ""

# Stop any existing container
docker rm -f hr-agent-test 2>/dev/null || true

# Run the agent
echo "Starting container..."
docker run -d \
  -p 5000:5000 \
  --name hr-agent-test \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  -e MONGODB_URI="$MONGODB_URI" \
  -e MONGODB_DATABASE="$MONGODB_DATABASE" \
  hr-agent

if [ $? -eq 0 ]; then
    echo "✅ Container started successfully!"
    echo ""
    echo "Waiting for agent to start..."
    sleep 3
    
    echo ""
    echo "Checking logs..."
    docker logs hr-agent-test
    
    echo ""
    echo "================================"
    echo "HR Agent is running!"
    echo "================================"
    echo ""
    echo "Test with:"
    echo "  curl http://localhost:5000/health"
    echo ""
    echo "Or run tests:"
    echo "  ./test_requests.sh"
    echo ""
    echo "View logs:"
    echo "  docker logs -f hr-agent-test"
    echo ""
else
    echo "❌ Failed to start container"
    exit 1
fi
