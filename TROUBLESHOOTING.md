# Troubleshooting Guide

## Common Issues and Solutions

### 1. API Key Error (401 Unauthorized)

**Error Message**:
```
Error code: 401 - {'error': {'message': 'Incorrect API key provided...
```

**Cause**: Invalid or malformed OpenAI API key

**Solution**:
```bash
# 1. Get your API key from https://platform.openai.com/api-keys
# 2. Make sure it starts with 'sk-proj-' or 'sk-'
# 3. Set it correctly:
export OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE

# 4. Verify it's set:
echo $OPENAI_API_KEY

# 5. Restart the Docker container:
docker stop $(docker ps -q --filter ancestor=hr-agent)
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent
```

**Common Mistakes**:
- ❌ Key starts with `k-proj-` (missing 's')
- ❌ Key has extra spaces or quotes
- ❌ Using old/revoked key
- ❌ Not exporting the variable

**Correct Format**:
```bash
export OPENAI_API_KEY=sk-proj-abcd1234...
```

---

### 2. Missing jq Command

**Error Message**:
```
./test_agent.sh: line 34: jq: command not found
```

**Cause**: `jq` JSON processor not installed

**Solution Option 1** (Install jq):
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y jq

# macOS
brew install jq
```

**Solution Option 2** (Already fixed in updated script):
The test script now works without jq, just with less pretty output.

---

### 3. Port Already in Use

**Error Message**:
```
Error starting userland proxy: listen tcp4 0.0.0.0:5000: bind: address already in use
```

**Solution**:
```bash
# Find process using port 5000
lsof -ti:5000

# Kill the process
lsof -ti:5000 | xargs kill -9

# Or use a different port
docker run -p 5001:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent
# Then update test script: BASE_URL="http://localhost:5001"
```

---

### 4. Docker Build Fails

**Error Message**:
```
ERROR: failed to solve: process "/bin/sh -c pip install..." did not complete successfully
```

**Solution**:
```bash
# Clear Docker cache and rebuild
docker build -t hr-agent . --no-cache

# If still fails, check internet connection
ping pypi.org

# Try with verbose output
docker build -t hr-agent . --progress=plain
```

---

### 5. Module Import Errors

**Error Message**:
```
ModuleNotFoundError: No module named 'tools'
```

**Cause**: Python path issues or missing files

**Solution**:
```bash
# Verify all files are present
ls -la Nasiko-Agents-of-Chaos/src/

# Should see:
# - __init__.py
# - __main__.py
# - agent.py
# - tools.py
# - models.py
# - core/ directory
# - modules/ directory

# Rebuild Docker image
docker build -t hr-agent . --no-cache
```

---

### 6. Agent Returns 500 Error

**Error Message**:
```
INFO: 172.17.0.1:62386 - "POST / HTTP/1.1" 500 Internal Server Error
```

**Causes & Solutions**:

**A. API Key Issue**
```bash
# Check if API key is set in container
docker exec -it $(docker ps -q --filter ancestor=hr-agent) env | grep OPENAI
```

**B. LLM Error**
```bash
# Check Docker logs
docker logs $(docker ps -q --filter ancestor=hr-agent)

# Look for specific error messages
```

**C. Module Initialization Error**
```bash
# Check if all modules loaded
docker logs $(docker ps -q --filter ancestor=hr-agent) | grep "module"
```

---

### 7. Test Script Fails

**Error Message**:
```
curl: (7) Failed to connect to localhost port 5000: Connection refused
```

**Solution**:
```bash
# 1. Check if agent is running
docker ps | grep hr-agent

# 2. If not running, start it
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent

# 3. Wait a few seconds for startup
sleep 5

# 4. Test connection
curl http://localhost:5000/

# 5. Run test again
./test_agent.sh 1
```

---

### 8. Slow Response Times

**Issue**: Agent takes > 30 seconds to respond

**Solutions**:

**A. Use Faster Model**
Edit `src/agent.py`:
```python
# Change from:
self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

# To:
self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
```

**B. Reduce Temperature**
```python
self.llm = ChatOpenAI(model="gpt-4o", temperature=0)  # More deterministic
```

**C. Check OpenAI Status**
```bash
# Visit https://status.openai.com/
```

---

### 9. JSON Parse Errors

**Error Message**:
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solution**:
```bash
# Test with proper JSON format
curl -X POST http://localhost:5000/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "Hello"}]
      }
    }
  }'

# Make sure JSON is valid (use https://jsonlint.com/)
```

---

### 10. Docker Container Exits Immediately

**Issue**: Container starts then stops

**Solution**:
```bash
# Check logs
docker logs $(docker ps -aq --filter ancestor=hr-agent | head -1)

# Run in interactive mode to see errors
docker run -it -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent

# Check if port is specified correctly in Dockerfile
grep CMD Dockerfile
# Should be: CMD ["python", "__main__.py", "--host", "0.0.0.0", "--port", "5000"]
```

---

## Quick Diagnostic Commands

### Check Everything
```bash
# 1. API Key
echo "API Key: ${OPENAI_API_KEY:0:10}..." # Shows first 10 chars

# 2. Docker
docker --version
docker ps

# 3. Port
lsof -ti:5000

# 4. Agent Status
curl -s http://localhost:5000/ | head -20

# 5. Test Connection
curl -X POST http://localhost:5000/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"message/send","params":{"message":{"role":"user","parts":[{"kind":"text","text":"test"}]}}}'
```

---

## Getting Help

### 1. Check Logs
```bash
# Docker logs
docker logs $(docker ps -q --filter ancestor=hr-agent)

# Last 50 lines
docker logs --tail 50 $(docker ps -q --filter ancestor=hr-agent)

# Follow logs in real-time
docker logs -f $(docker ps -q --filter ancestor=hr-agent)
```

### 2. Verify Configuration
```bash
# Check all config files
cat AgentCard.json
cat docker-compose.yml
cat Dockerfile
```

### 3. Test Individual Components
```bash
# Test just the server
docker run -it -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent

# Test with simple curl
curl http://localhost:5000/
```

---

## Still Having Issues?

1. **Read the documentation**:
   - [QUICKSTART.md](QUICKSTART.md)
   - [README.md](README.md)
   - [DEPLOYMENT.md](DEPLOYMENT.md)

2. **Check the code**:
   - Review `src/agent.py`
   - Check `src/tools.py`
   - Verify module files

3. **Start fresh**:
   ```bash
   # Remove all containers
   docker rm -f $(docker ps -aq --filter ancestor=hr-agent)
   
   # Remove image
   docker rmi hr-agent
   
   # Rebuild
   docker build -t hr-agent .
   
   # Run again
   docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent
   ```

---

## Prevention Checklist

Before running, verify:
- [ ] OpenAI API key is valid and starts with `sk-`
- [ ] API key is exported: `export OPENAI_API_KEY=...`
- [ ] Docker is running
- [ ] Port 5000 is available
- [ ] All source files are present
- [ ] Docker image is built: `docker images | grep hr-agent`

---

**Most Common Issue**: Invalid API key (90% of problems)

**Quick Fix**:
```bash
export OPENAI_API_KEY=sk-proj-YOUR_REAL_KEY
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent
```

Good luck! 🚀
