#!/bin/bash

echo "================================"
echo "HR Agent - Search Capabilities Test"
echo "================================"

echo ""
echo "Test 1: Search by Name"
echo "--------------------"
curl -s -X POST http://localhost:5000/ -H "Content-Type: application/json" -d '{
  "jsonrpc":"2.0",
  "id":"test-1",
  "method":"message/send",
  "params":{
    "message":{
      "role":"user",
      "parts":[{"kind":"text","text":"Give me information about Bob"}]
    }
  }
}' | python3 -m json.tool | grep -A 20 '"text"'

echo ""
echo "Test 2: Search by Skills (Python)"
echo "--------------------"
curl -s -X POST http://localhost:5000/ -H "Content-Type: application/json" -d '{
  "jsonrpc":"2.0",
  "id":"test-2",
  "method":"message/send",
  "params":{
    "message":{
      "role":"user",
      "parts":[{"kind":"text","text":"Show me all candidates who know Python"}]
    }
  }
}' | python3 -m json.tool | grep -A 20 '"text"'

echo ""
echo "Test 3: Search by Skills (React)"
echo "--------------------"
curl -s -X POST http://localhost:5000/ -H "Content-Type: application/json" -d '{
  "jsonrpc":"2.0",
  "id":"test-3",
  "method":"message/send",
  "params":{
    "message":{
      "role":"user",
      "parts":[{"kind":"text","text":"Find all candidates with React skills"}]
    }
  }
}' | python3 -m json.tool | grep -A 20 '"text"'

echo ""
echo "Test 4: Search by College"
echo "--------------------"
curl -s -X POST http://localhost:5000/ -H "Content-Type: application/json" -d '{
  "jsonrpc":"2.0",
  "id":"test-4",
  "method":"message/send",
  "params":{
    "message":{
      "role":"user",
      "parts":[{"kind":"text","text":"Show me all candidates from MIT"}]
    }
  }
}' | python3 -m json.tool | grep -A 20 '"text"'

echo ""
echo "================================"
echo "Tests complete!"
echo "================================"
