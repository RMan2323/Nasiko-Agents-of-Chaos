#!/bin/bash

# Quick test requests for HR Agent
# Usage: ./test_requests.sh

BASE_URL="http://localhost:5000"

echo "================================"
echo "HR Agent - Quick Test Requests"
echo "================================"
echo ""

# Test 1: Simple greeting
echo "Test 1: Simple Greeting"
echo "------------------------"
curl -X POST $BASE_URL/ \
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
  }'
echo ""
echo ""

# Test 2: Schedule interview
echo "Test 2: Schedule Interview"
echo "------------------------"
curl -X POST $BASE_URL/ \
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

# Test 3: Add candidate to database
echo "Test 3: Add Candidate to Database"
echo "------------------------"
curl -X POST $BASE_URL/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-3",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "Add candidate Michael Rodriguez, email michael@example.com, college MIT, CPI 9.0, skills Python and AWS, 5 years experience"
          }
        ]
      }
    }
  }'
echo ""
echo ""

# Test 4: Screen candidate
echo "Test 4: Screen Candidate"
echo "------------------------"
curl -X POST $BASE_URL/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-4",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "Screen candidate Michael Rodriguez for Senior Software Engineer position"
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
