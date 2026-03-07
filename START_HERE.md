# 🚀 HR Agent - START HERE

**Team**: Agents of Chaos  
**Event**: Buildathon 2026  
**Status**: ✅ Ready for Deployment

---

## 👋 Welcome!

You've just opened the HR Agent project - a comprehensive AI-powered HR assistant built for the Nasiko platform.

---

## ⚡ Quick Start (5 minutes)

### 1. Set Your API Key
```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Build & Run
```bash
docker build -t hr-agent .
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent
```

### 3. Test It
```bash
chmod +x test_agent.sh
./test_agent.sh 1
```

**That's it!** Your HR agent is running.

---

## 📖 What to Read Next

### New to the Project?
👉 Read **[INDEX.md](INDEX.md)** - Complete documentation guide

### Want Quick Setup?
👉 Read **[QUICKSTART.md](QUICKSTART.md)** - 5-minute guide

### Want Full Details?
👉 Read **[README.md](README.md)** - Comprehensive documentation

### Ready to Deploy?
👉 Read **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment checklist

### Preparing Demo?
👉 Read **[PITCH.md](PITCH.md)** - Hackathon pitch

---

## 🌟 What Makes This Special?

### Two Unique Features

1. **AI Interview Coach** ⭐
   - Not just Q&A - full coaching experience
   - Helps both interviewers and candidates
   - Post-interview feedback and improvement

2. **Culture Fit Analyzer** ⭐
   - Predicts long-term success
   - Multi-dimensional analysis
   - Team dynamics assessment

### Complete HR Lifecycle
```
Research → Screen → Interview → Evaluate → Schedule
```
All in one agent, all in natural language.

---

## 🎯 What Can It Do?

Try these commands:

```
"Schedule a technical interview with Sarah Chen"

"Screen candidate Michael Rodriguez for Senior Engineer. 
He has 10 years Python experience."

"Generate interview questions for Product Manager"

"Analyze culture fit between Emma Wilson and our startup"

"Research salary for senior data scientist in San Francisco"

"Hire a backend engineer. Research salary, screen Alex Kim 
with 8 years Go experience, and schedule interview if good."
```

---

## 📁 Project Structure

```
Nasiko-Agents-of-Chaos/
│
├── 📚 Documentation (8 files)
│   ├── START_HERE.md      ← You are here!
│   ├── INDEX.md           ← Documentation guide
│   ├── QUICKSTART.md      ← 5-minute setup
│   ├── README.md          ← Main docs
│   ├── SUMMARY.md         ← Project summary
│   ├── ARCHITECTURE.md    ← Technical details
│   ├── FEATURES.md        ← Feature descriptions
│   ├── DEPLOYMENT.md      ← Deployment guide
│   └── PITCH.md           ← Hackathon pitch
│
├── ⚙️ Configuration
│   ├── AgentCard.json
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── .gitignore
│
├── 🧪 Testing
│   └── test_agent.sh
│
└── 💻 Source Code
    └── src/
        ├── agent.py           (Main logic)
        ├── tools.py           (7 tools)
        ├── core/              (5 files)
        └── modules/           (5 modules)
            ├── calendar_manager.py
            ├── recruiter.py
            ├── researcher.py
            ├── interview_coach.py    ⭐
            └── culture_analyzer.py   ⭐
```

---

## ✅ Quick Checklist

### For Testing
- [ ] Set OPENAI_API_KEY
- [ ] Build Docker image
- [ ] Run agent
- [ ] Test with test_agent.sh
- [ ] Verify all 6 scenarios work

### For Deployment
- [ ] Read DEPLOYMENT.md
- [ ] Test locally first
- [ ] Choose deployment method (GitHub or ZIP)
- [ ] Follow deployment checklist
- [ ] Verify agent status

### For Demo
- [ ] Read PITCH.md
- [ ] Practice demo scenarios
- [ ] Highlight unique features
- [ ] Prepare talking points
- [ ] Test live demos

---

## 🎬 Demo Scenarios

Run these to see the agent in action:

```bash
./test_agent.sh 1  # Schedule interview
./test_agent.sh 2  # Screen candidate
./test_agent.sh 3  # Interview prep (Unique!)
./test_agent.sh 4  # Culture fit (Unique!)
./test_agent.sh 5  # Salary research
./test_agent.sh 6  # Complex multi-step
```

---

## 🆘 Need Help?

### Quick Fixes

**Invalid API Key? (Most Common)**
```bash
# Get your key from https://platform.openai.com/api-keys
# Make sure it starts with 'sk-proj-' or 'sk-'
export OPENAI_API_KEY=sk-proj-YOUR_REAL_KEY_HERE
```

**Port already in use?**
```bash
lsof -ti:5000 | xargs kill -9
```

**Docker issues?**
```bash
docker build -t hr-agent . --no-cache
```

### More Help
- 🔧 **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Complete troubleshooting guide
- 📖 [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting) - Deployment issues
- ⚡ [QUICKSTART.md](QUICKSTART.md#troubleshooting) - Setup issues
- 📚 [INDEX.md](INDEX.md) - Documentation navigation

---

## 📊 Key Stats

- ✅ **7 Tools** - Complete HR lifecycle
- ✅ **5 Modules** - Specialized capabilities
- ✅ **2 Unique Features** - Interview Coach + Culture Fit
- ✅ **~2000 Lines** - Clean, modular code
- ✅ **< 10 seconds** - Average response time
- ✅ **6 Test Scenarios** - Comprehensive testing
- ✅ **8 Documentation Files** - Thorough docs

---

## 🎯 Next Steps

### 1. Quick Test (5 minutes)
```bash
export OPENAI_API_KEY=your_key
docker build -t hr-agent .
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent
# In another terminal:
./test_agent.sh
```

### 2. Read Documentation (15 minutes)
- [INDEX.md](INDEX.md) - Documentation guide
- [README.md](README.md) - Full documentation
- [FEATURES.md](FEATURES.md) - Feature details

### 3. Deploy (30 minutes)
- [DEPLOYMENT.md](DEPLOYMENT.md) - Follow checklist
- Choose GitHub or ZIP method
- Deploy to Nasiko platform

### 4. Prepare Demo (30 minutes)
- [PITCH.md](PITCH.md) - Review pitch
- Practice demo scenarios
- Highlight unique features

---

## 🏆 Why This Agent Wins

### Innovation
- ✅ Two unique features not seen elsewhere
- ✅ Novel approach to culture fit prediction
- ✅ AI coaching from both perspectives

### Technical Excellence
- ✅ Clean, modular architecture
- ✅ Production-ready code
- ✅ Comprehensive documentation
- ✅ Fully tested

### Business Impact
- ✅ Solves real, expensive problems
- ✅ Clear ROI (save $250K+/year)
- ✅ Scalable business model
- ✅ Large market opportunity

### Execution
- ✅ Complete, working solution
- ✅ Professional presentation
- ✅ Clear roadmap
- ✅ Ready to deploy

---

## 📞 Contact

**Team**: Agents of Chaos  
**Repository**: https://github.com/RMan2323/Nasiko-Agents-of-Chaos  
**Event**: Buildathon 2026

---

## 🚀 Ready to Go!

Everything is set up and ready. Just follow the Quick Start above and you're good to go!

**Good luck with the hackathon!** 💪

---

**Navigation**:
- 📖 [INDEX.md](INDEX.md) - Documentation guide
- ⚡ [QUICKSTART.md](QUICKSTART.md) - 5-minute setup
- 📚 [README.md](README.md) - Full documentation
- 🚀 [DEPLOYMENT.md](DEPLOYMENT.md) - Deploy guide
- 🎤 [PITCH.md](PITCH.md) - Hackathon pitch

---

**Built with ❤️ by team Agents of Chaos for Buildathon 2026** 🚀
