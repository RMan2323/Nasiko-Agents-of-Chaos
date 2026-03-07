#!/bin/bash

echo "================================"
echo "HR Agent - Correct Test Format"
echo "================================"
echo ""

BASE_URL="http://localhost:5000"

# Test 1: Health check
echo "Test 1: Health Check"
echo "--------------------"
curl -s $BASE_URL/health
echo ""
echo ""

# Test 2: Simple greeting (CORRECT FORMAT)
echo "Test 2: Simple Greeting (Correct Format)"
echo "-----------------------------------------"
curl -s -X POST $BASE_URL/ \
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
            "text": "Hello, can you help me with HR tasks?"
          }
        ]
      }
    }
  }'
echo ""
echo ""

# Test 3: Schedule interview (CORRECT FORMAT)
echo "Test 3: Schedule Interview (Correct Format)"
echo "--------------------------------------------"
curl -s -X POST $BASE_URL/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-2",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "Schedule a technical interview with Sarah Chen, email sarah@example.com for next week"
          }
        ]
      }
    }
  }'
echo ""
echo ""

echo "================================"
echo "Tests complete!"
echo "================================"
