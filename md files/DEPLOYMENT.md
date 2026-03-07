# Deployment Checklist - HR Agent

## Pre-Deployment Checklist

### ✅ Required Files
- [x] `Dockerfile` - Present and configured for port 5000
- [x] `docker-compose.yml` - Present with correct service name
- [x] `AgentCard.json` - Present with updated skills and description
- [x] `README.md` - Comprehensive documentation
- [x] `src/agent.py` - Main agent logic
- [x] `src/tools.py` - Tool definitions
- [x] `src/__main__.py` - Entry point
- [x] `src/models.py` - Data models
- [x] All module files in `src/modules/`
- [x] All core files in `src/core/`

### ✅ Configuration Check
- [x] Port 5000 in Dockerfile CMD
- [x] Port 5000 in docker-compose.yml
- [x] Port 5000 in AgentCard.json URL
- [x] Port 5000 in __main__.py default
- [x] OPENAI_API_KEY in docker-compose.yml environment
- [x] External network `agents-net` configured

### ✅ Code Quality
- [x] No syntax errors (verified with getDiagnostics)
- [x] All imports present
- [x] Modular components properly initialized
- [x] Tools properly registered
- [x] Modules properly registered with router

### ✅ Documentation
- [x] README.md with full documentation
- [x] QUICKSTART.md for easy onboarding
- [x] FEATURES.md detailing capabilities
- [x] Test script (test_agent.sh)
- [x] Example interactions documented

---

## Local Testing Steps

### 1. Build Test
```bash
cd Nasiko-Agents-of-Chaos
docker build -t hr-agent-test .
```

**Expected**: Build completes without errors

### 2. Run Test
```bash
export OPENAI_API_KEY=your_key_here
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent-test
```

**Expected**: Server starts on port 5000

### 3. Basic Functionality Test
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
        "parts": [{"kind": "text", "text": "Hello, can you help me?"}]
      }
    }
  }'
```

**Expected**: JSON response with task result

### 4. Tool Test - Schedule
```bash
./test_agent.sh 1
```

**Expected**: Scheduling response with meeting details

### 5. Tool Test - Screen
```bash
./test_agent.sh 2
```

**Expected**: Candidate screening with match score

### 6. Tool Test - Interview Prep
```bash
./test_agent.sh 3
```

**Expected**: Interview questions and guidance

### 7. Tool Test - Culture Fit
```bash
./test_agent.sh 4
```

**Expected**: Culture fit analysis with score

### 8. Tool Test - Salary Research
```bash
./test_agent.sh 5
```

**Expected**: Salary ranges and market data

### 9. Complex Multi-step Test
```bash
./test_agent.sh 6
```

**Expected**: Multiple tasks executed and aggregated

---

## Deployment Methods

### Method 1: GitHub Deployment (Recommended)

#### Prerequisites
- GitHub account
- Repository created
- Code pushed to main branch

#### Steps
1. **Prepare Repository**
```bash
cd Nasiko-Agents-of-Chaos
git init
git add .
git commit -m "Initial HR Agent implementation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

2. **Deploy via Nasiko Dashboard**
- Log into Nasiko dashboard
- Navigate to "Add Agent"
- Click "Connect GitHub"
- Authenticate with GitHub
- Select your repository
- Wait for automatic deployment

3. **Verify Deployment**
- Check deployment status in dashboard
- Verify agent appears in registry
- Test agent through Nasiko platform

#### Updates
```bash
# Make changes
git add .
git commit -m "Update: description of changes"
git push origin main

# In Nasiko dashboard
# Navigate to "Your Agents"
# Click "Re-upload Agent"
```

---

### Method 2: ZIP Upload

#### Prerequisites
- Agent tested locally
- All files present

#### Steps
1. **Create ZIP Package**
```bash
cd ..
zip -r hr-agent-chaos.zip Nasiko-Agents-of-Chaos/ \
  -x "*.pyc" \
  -x "*/__pycache__/*" \
  -x "*/.git/*" \
  -x "*/test_agent.sh" \
  -x "*/.DS_Store"
```

2. **Verify ZIP Contents**
```bash
unzip -l hr-agent-chaos.zip
```

**Should include**:
- Dockerfile
- docker-compose.yml
- AgentCard.json
- README.md
- src/ directory with all files

3. **Upload via Dashboard**
- Log into Nasiko dashboard
- Navigate to "Add Agent"
- Click "Upload ZIP"
- Select `hr-agent-chaos.zip`
- Click upload
- Wait for build and deployment

4. **Monitor Deployment**
- Watch deployment logs
- Check for build errors
- Verify agent status

#### Updates
```bash
# Create new version
zip -r hr-agent-chaos-v1.1.zip Nasiko-Agents-of-Chaos/ \
  -x "*.pyc" "*/__pycache__/*" "*/.git/*"

# Upload via dashboard
# Navigate to "Your Agents"
# Click "Re-upload Agent"
# Select new ZIP file
```

---

## Post-Deployment Verification

### 1. Agent Status Check
- [ ] Agent shows as "Running" in dashboard
- [ ] No error messages in logs
- [ ] Agent appears in registry

### 2. Functionality Test
Test each capability through the platform:
- [ ] Schedule interview
- [ ] Screen candidate
- [ ] Research candidate
- [ ] Interview preparation
- [ ] Culture fit analysis
- [ ] Salary research
- [ ] Complex multi-step task

### 3. Performance Check
- [ ] Response time < 10 seconds
- [ ] No timeout errors
- [ ] Proper error handling
- [ ] Consistent output format

---

## Troubleshooting

### Build Fails
**Issue**: Docker build fails during deployment

**Solutions**:
1. Check Dockerfile syntax
2. Verify all dependencies in pip install
3. Test build locally first
4. Check for missing files

### Agent Crashes
**Issue**: Agent shows "Crashed" status

**Solutions**:
1. Check deployment logs for errors
2. Verify OPENAI_API_KEY is set
3. Check port configuration (5000)
4. Verify all imports are correct

### Tools Not Working
**Issue**: Agent responds but tools aren't called

**Solutions**:
1. Check tool registration in agent.py
2. Verify set_modular_components() is called
3. Check module registration with router
4. Review tool descriptions for clarity

### Slow Responses
**Issue**: Agent takes too long to respond

**Solutions**:
1. Consider using gpt-4o-mini for faster responses
2. Reduce temperature for deterministic outputs
3. Optimize prompts for conciseness
4. Check for unnecessary API calls

---

## Rollback Plan

If deployment fails:

1. **GitHub Method**:
```bash
git revert HEAD
git push origin main
# Re-upload in dashboard
```

2. **ZIP Method**:
- Keep previous working ZIP file
- Upload previous version through dashboard

---

## Success Criteria

Agent is successfully deployed when:
- ✅ Shows "Running" status in dashboard
- ✅ Responds to test queries
- ✅ All 7 tools work correctly
- ✅ Response time < 10 seconds
- ✅ No errors in logs
- ✅ Proper JSON-RPC format responses

---

## Final Checklist

Before submitting for hackathon:
- [ ] All tests pass locally
- [ ] Agent deployed successfully
- [ ] Documentation complete
- [ ] Unique features working (Interview Coach, Culture Fit)
- [ ] Demo scenarios prepared
- [ ] Team members can access and test
- [ ] GitHub repository public (if using GitHub method)
- [ ] README.md has team information

---

## Support

For deployment issues during hackathon:
1. Check deployment logs in dashboard
2. Review this checklist
3. Test locally first
4. Contact team Agents of Chaos

---

**Ready to deploy! 🚀**

Good luck with Buildathon 2026!
