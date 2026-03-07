#!/bin/bash

# Simple test script that doesn't require jq
# Usage: ./test_simple.sh

echo "================================"
echo "HR Agent - Simple Test"
echo "================================"
echo ""

# Check if API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ ERROR: OPENAI_API_KEY is not set"
    echo ""
    echo "Please set your API key:"
    echo "  export OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE"
    echo ""
    echo "Get your key from: https://platform.openai.com/api-keys"
    exit 1
fi

# Validate API key format
if [[ ! $OPENAI_API_KEY =~ ^sk- ]]; then
    echo "⚠️  WARNING: API key should start with 'sk-' or 'sk-proj-'"
    echo "Current key starts with: ${OPENAI_API_KEY:0:10}..."
    echo ""
    echo "Please verify your key at: https://platform.openai.com/api-keys"
    echo ""
fi

# Check if agent is running
echo "Checking if agent is running on port 5000..."
if ! curl -s http://localhost:5000/ > /dev/null 2>&1; then
    echo "❌ ERROR: Agent is not running on port 5000"
    echo ""
    echo "Start the agent with:"
    echo "  docker run -p 5000:5000 -e OPENAI_API_KEY=\$OPENAI_API_KEY hr-agent"
    echo ""
    exit 1
fi

echo "✅ Agent is running"
echo ""

# Test 1: Simple greeting
echo "Test 1: Simple Greeting"
echo "------------------------"
RESPONSE=$(curl -s -X POST http://localhost:5000/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "Hello, can you help me?"}]
      }
    }
  }')

# Check if response contains error
if echo "$RESPONSE" | grep -q '"error"'; then
    echo "❌ ERROR in response:"
    echo "$RESPONSE"
    echo ""
    
    # Check for specific errors
    if echo "$RESPONSE" | grep -q "401"; then
        echo "This is an API key error. Please check:"
        echo "1. Your API key is correct"
        echo "2. It starts with 'sk-' or 'sk-proj-'"
        echo "3. It's not expired or revoked"
        echo ""
        echo "Get a new key at: https://platform.openai.com/api-keys"
    fi
    exit 1
else
    echo "✅ Response received successfully"
    echo ""
    # Extract just the text response
    if command -v python3 &> /dev/null; then
        echo "Agent says:"
        echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('result', {}).get('artifacts', [{}])[0].get('parts', [{}])[0].get('text', 'No text found'))" 2>/dev/null || echo "$RESPONSE"
    else
        echo "$RESPONSE"
    fi
fi

echo ""
echo "================================"
echo "✅ Basic test passed!"
echo "================================"
echo ""
echo "Run full test suite with: ./test_agent.sh"
echo ""
