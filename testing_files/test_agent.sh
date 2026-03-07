#!/bin/bash

# Test script for HR Agent
# Usage: ./test_agent.sh [test_number]

BASE_URL="http://localhost:5000"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if jq is available
if command -v jq &> /dev/null; then
    USE_JQ=true
else
    USE_JQ=false
    echo "Note: jq not found. Install with 'sudo apt-get install jq' for prettier output"
fi

echo -e "${BLUE}HR Agent Test Suite${NC}"
echo "================================"

# Test 1: Schedule Interview
test_schedule() {
    echo -e "\n${GREEN}Test 1: Schedule Interview${NC}"
    if [ "$USE_JQ" = true ]; then
        curl -X POST $BASE_URL/ \
          -H "Content-Type: application/json" \
          -d '{
            "jsonrpc": "2.0",
            "id": "test-schedule",
            "method": "message/send",
            "params": {
              "message": {
                "role": "user",
                "parts": [{
                  "kind": "text",
                  "text": "Schedule a technical interview with Sarah Chen for next week"
                }]
              }
            }
          }' | jq '.'
    else
        curl -X POST $BASE_URL/ \
          -H "Content-Type: application/json" \
          -d '{
            "jsonrpc": "2.0",
            "id": "test-schedule",
            "method": "message/send",
            "params": {
              "message": {
                "role": "user",
                "parts": [{
                  "kind": "text",
                  "text": "Schedule a technical interview with Sarah Chen for next week"
                }]
              }
            }
          }'
        echo ""
    fi
}

# Test 2: Screen Candidate
test_screen() {
    echo -e "\n${GREEN}Test 2: Screen Candidate${NC}"
    RESPONSE=$(curl -s -X POST $BASE_URL/ \
      -H "Content-Type: application/json" \
      -d '{
        "jsonrpc": "2.0",
        "id": "test-screen",
        "method": "message/send",
        "params": {
          "message": {
            "role": "user",
            "parts": [{
              "kind": "text",
              "text": "Screen candidate Michael Rodriguez for Senior Software Engineer. He has 10 years of Python experience, led teams of 5-8 engineers, and has strong system design skills."
            }]
          }
        }
      }')
    
    if [ "$USE_JQ" = true ]; then
        echo "$RESPONSE" | jq '.'
    else
        echo "$RESPONSE"
    fi
}

# Test 3: Interview Prep
test_interview_prep() {
    echo -e "\n${GREEN}Test 3: Interview Preparation${NC}"
    RESPONSE=$(curl -s -X POST $BASE_URL/ \
      -H "Content-Type: application/json" \
      -d '{
        "jsonrpc": "2.0",
        "id": "test-prep",
        "method": "message/send",
        "params": {
          "message": {
            "role": "user",
            "parts": [{
              "kind": "text",
              "text": "Generate medium difficulty technical interview questions for a Full Stack Developer position"
            }]
          }
        }
      }')
    
    if [ "$USE_JQ" = true ]; then
        echo "$RESPONSE" | jq '.'
    else
        echo "$RESPONSE"
    fi
}

# Test 4: Culture Fit Analysis
test_culture_fit() {
    echo -e "\n${GREEN}Test 4: Culture Fit Analysis${NC}"
    RESPONSE=$(curl -s -X POST $BASE_URL/ \
      -H "Content-Type: application/json" \
      -d '{
        "jsonrpc": "2.0",
        "id": "test-culture",
        "method": "message/send",
        "params": {
          "message": {
            "role": "user",
            "parts": [{
              "kind": "text",
              "text": "Analyze culture fit between candidate Emma Wilson and our fast-paced startup environment"
            }]
          }
        }
      }')
    
    if [ "$USE_JQ" = true ]; then
        echo "$RESPONSE" | jq '.'
    else
        echo "$RESPONSE"
    fi
}

# Test 5: Salary Research
test_salary() {
    echo -e "\n${GREEN}Test 5: Salary Research${NC}"
    RESPONSE=$(curl -s -X POST $BASE_URL/ \
      -H "Content-Type: application/json" \
      -d '{
        "jsonrpc": "2.0",
        "id": "test-salary",
        "method": "message/send",
        "params": {
          "message": {
            "role": "user",
            "parts": [{
              "kind": "text",
              "text": "What is the salary range for a senior data scientist in San Francisco?"
            }]
          }
        }
      }')
    
    if [ "$USE_JQ" = true ]; then
        echo "$RESPONSE" | jq '.'
    else
        echo "$RESPONSE"
    fi
}

# Test 6: Multi-step Complex Task
test_complex() {
    echo -e "\n${GREEN}Test 6: Complex Multi-step Task${NC}"
    RESPONSE=$(curl -s -X POST $BASE_URL/ \
      -H "Content-Type: application/json" \
      -d '{
        "jsonrpc": "2.0",
        "id": "test-complex",
        "method": "message/send",
        "params": {
          "message": {
            "role": "user",
            "parts": [{
              "kind": "text",
              "text": "I need to hire a senior backend engineer. Research the market salary, screen candidate Alex Kim who has 8 years of Go experience, and if they look good, schedule a technical interview."
            }]
          }
        }
      }')
    
    if [ "$USE_JQ" = true ]; then
        echo "$RESPONSE" | jq '.'
    else
        echo "$RESPONSE"
    fi
}

# Run tests based on argument
case "$1" in
    1) test_schedule ;;
    2) test_screen ;;
    3) test_interview_prep ;;
    4) test_culture_fit ;;
    5) test_salary ;;
    6) test_complex ;;
    *)
        echo "Running all tests..."
        test_schedule
        sleep 2
        test_screen
        sleep 2
        test_interview_prep
        sleep 2
        test_culture_fit
        sleep 2
        test_salary
        sleep 2
        test_complex
        ;;
esac

echo -e "\n${BLUE}Tests complete!${NC}"
