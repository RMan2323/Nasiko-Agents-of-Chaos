# Quick Start Guide - HR Agent

Get your HR Agent up and running in 5 minutes!

## Prerequisites

- Docker Desktop installed and running
- OpenAI API Key
- Terminal/Command Line access

## Step 1: Set Your API Key

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

## Step 2: Build the Agent

```bash
cd Nasiko-Agents-of-Chaos
docker build -t hr-agent .
```

This will take 2-3 minutes the first time.

## Step 3: Run the Agent

```bash
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5000
```

## Step 4: Test the Agent

Open a new terminal and run:

```bash
# Make test script executable (first time only)
chmod +x test_agent.sh

# Run a quick test
./test_agent.sh 1
```

Or test manually:

```bash
curl -X POST http://localhost:5000/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{
          "kind": "text",
          "text": "Schedule a technical interview with Sarah Chen"
        }]
      }
    }
  }'
```

## What to Try

### 1. Schedule an Interview
```
"Schedule a technical interview with John Doe for next Tuesday"
```

### 2. Screen a Candidate
```
"Screen candidate Sarah Chen for Senior Engineer role. She has 8 years Python experience."
```

### 3. Get Interview Questions
```
"Generate interview questions for a Product Manager position"
```

### 4. Analyze Culture Fit
```
"Analyze culture fit between Michael Rodriguez and our startup"
```

### 5. Research Salaries
```
"What's the salary range for a senior data scientist in San Francisco?"
```

### 6. Complex Multi-step Task
```
"I need to hire a backend engineer. Research market salary, screen candidate Alex Kim with 8 years Go experience, and schedule an interview if they're good."
```

## Run All Tests

```bash
./test_agent.sh
```

This runs all 6 test scenarios automatically.

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### API Key Not Set
```bash
# Check if set
echo $OPENAI_API_KEY

# Set it again
export OPENAI_API_KEY=your_key_here
```

### Docker Issues
```bash
# Restart Docker Desktop
# Then rebuild
docker build -t hr-agent . --no-cache
```

## Next Steps

1. Deploy to Nasiko platform (see README.md)
2. Customize modules in `src/modules/`
3. Add new tools in `src/tools.py`
4. Enhance prompts in `src/agent.py`

## Need Help?

Check the full README.md for detailed documentation and architecture details.

---

**Happy Building! 🚀**
