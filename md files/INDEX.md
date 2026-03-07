# HR Agent - Documentation Index

**Team**: Agents of Chaos  
**Event**: Buildathon 2026  
**Status**: ✅ Ready for Deployment

---

## 📚 Documentation Guide

### For Quick Start
1. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
   - Prerequisites
   - Build & run commands
   - Quick tests
   - Troubleshooting

### For Understanding the Project
2. **[README.md](README.md)** - Comprehensive overview
   - Features and capabilities
   - Architecture overview
   - Installation guide
   - Example interactions
   - Testing instructions

3. **[SUMMARY.md](SUMMARY.md)** - Project summary
   - What we built
   - Technical stack
   - Files created
   - Testing status
   - Quick commands

### For Technical Details
4. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
   - Visual diagrams
   - Request flow
   - Module architecture
   - Data flow
   - Technology stack

5. **[FEATURES.md](FEATURES.md)** - Detailed features
   - Core capabilities
   - Unique features
   - Use cases
   - Innovation highlights

### For Deployment
6. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guide
   - Pre-deployment checklist
   - Local testing steps
   - GitHub deployment
   - ZIP deployment
   - Troubleshooting

### For Presentation
7. **[PITCH.md](PITCH.md)** - Hackathon pitch
   - Problem statement
   - Solution overview
   - Demo scenarios
   - Business impact
   - Why we should win

---

## 🗂️ File Structure

```
Nasiko-Agents-of-Chaos/
│
├── Documentation (You are here!)
│   ├── INDEX.md              ← Start here
│   ├── QUICKSTART.md         ← 5-minute setup
│   ├── README.md             ← Main documentation
│   ├── SUMMARY.md            ← Project summary
│   ├── ARCHITECTURE.md       ← Technical details
│   ├── FEATURES.md           ← Feature descriptions
│   ├── DEPLOYMENT.md         ← Deployment guide
│   └── PITCH.md              ← Hackathon pitch
│
├── Configuration
│   ├── AgentCard.json        ← Agent metadata
│   ├── docker-compose.yml    ← Docker compose config
│   ├── Dockerfile            ← Docker build config
│   └── .gitignore            ← Git ignore rules
│
├── Testing
│   └── test_agent.sh         ← Automated test script
│
└── Source Code
    └── src/
        ├── __main__.py       ← Entry point
        ├── agent.py          ← Main agent logic
        ├── tools.py          ← LangChain tools
        ├── models.py         ← Data models
        │
        ├── core/             ← Modular architecture
        │   ├── base_module.py
        │   ├── planner.py
        │   ├── router.py
        │   ├── executor.py
        │   └── aggregator.py
        │
        └── modules/          ← Specialized modules
            ├── calendar_manager.py
            ├── recruiter.py
            ├── researcher.py
            ├── interview_coach.py    ⭐ Unique
            └── culture_analyzer.py   ⭐ Unique
```

---

## 🎯 Quick Navigation

### I want to...

**...get started quickly**
→ Read [QUICKSTART.md](QUICKSTART.md)

**...understand what this agent does**
→ Read [README.md](README.md) or [FEATURES.md](FEATURES.md)

**...see the technical architecture**
→ Read [ARCHITECTURE.md](ARCHITECTURE.md)

**...deploy the agent**
→ Read [DEPLOYMENT.md](DEPLOYMENT.md)

**...prepare a demo/pitch**
→ Read [PITCH.md](PITCH.md)

**...get a quick overview**
→ Read [SUMMARY.md](SUMMARY.md)

**...test the agent**
→ Run `./test_agent.sh` (see [QUICKSTART.md](QUICKSTART.md))

**...modify the code**
→ Check `src/` directory and [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🚀 Quick Commands

### Build
```bash
docker build -t hr-agent .
```

### Run
```bash
export OPENAI_API_KEY=your_key
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent
```

### Test
```bash
./test_agent.sh
```

### Deploy (GitHub)
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
# Then connect in Nasiko dashboard
```

---

## 📊 Key Statistics

- **7 Tools**: Complete HR lifecycle coverage
- **5 Modules**: Specialized capabilities
- **2 Unique Features**: Interview Coach + Culture Fit
- **~2000 Lines**: Clean, modular code
- **< 10 seconds**: Average response time
- **6 Test Scenarios**: Comprehensive testing
- **7 Documentation Files**: Thorough documentation

---

## 🌟 Unique Features

### 1. AI Interview Coach ⭐
- Generate tailored interview questions
- Provide coaching and feedback
- Interview tips and strategies
- Post-interview analysis

**See**: [FEATURES.md](FEATURES.md#4-ai-interview-coach-module)

### 2. Culture Fit Analyzer ⭐
- Assess candidate-company alignment
- Culture fit scoring (0-100)
- Team dynamics analysis
- Long-term success prediction

**See**: [FEATURES.md](FEATURES.md#5-culture-fit-analyzer-module)

---

## 🎬 Demo Scenarios

### Quick Tests
```bash
./test_agent.sh 1  # Schedule interview
./test_agent.sh 2  # Screen candidate
./test_agent.sh 3  # Interview prep
./test_agent.sh 4  # Culture fit
./test_agent.sh 5  # Salary research
./test_agent.sh 6  # Complex multi-step
```

**See**: [PITCH.md](PITCH.md#-demo-scenarios) for detailed scenarios

---

## 🔧 Development

### Adding New Modules
1. Create module in `src/modules/`
2. Extend `BaseModule`
3. Register in `agent.py`
4. Create tool in `tools.py`
5. Update documentation

**See**: [ARCHITECTURE.md](ARCHITECTURE.md#extension-points)

### Adding New Tools
1. Define `@tool` in `tools.py`
2. Add to `agent.tools` list
3. Update system prompt
4. Test functionality

**See**: [ARCHITECTURE.md](ARCHITECTURE.md#adding-new-tools)

---

## 🆘 Troubleshooting

### Common Issues

**Port already in use**
```bash
lsof -ti:5000 | xargs kill -9
```

**API key not set**
```bash
export OPENAI_API_KEY=your_key_here
```

**Docker build fails**
```bash
docker build -t hr-agent . --no-cache
```

**See**: [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting) for more

---

## 📞 Support

### During Hackathon
- Check documentation files
- Review test scripts
- Contact team Agents of Chaos

### After Hackathon
- GitHub Issues: https://github.com/RMan2323/Nasiko-Agents-of-Chaos
- Documentation: This repository

---

## ✅ Checklist for Team

### Before Demo
- [ ] Read [PITCH.md](PITCH.md)
- [ ] Test all scenarios with `./test_agent.sh`
- [ ] Review [FEATURES.md](FEATURES.md) for talking points
- [ ] Prepare to highlight unique features

### Before Deployment
- [ ] Complete [DEPLOYMENT.md](DEPLOYMENT.md) checklist
- [ ] Test locally
- [ ] Verify all files present
- [ ] Check configuration

### During Presentation
- [ ] Emphasize unique features (Interview Coach, Culture Fit)
- [ ] Show live demos
- [ ] Highlight business impact
- [ ] Discuss technical excellence

---

## 🏆 Success Criteria

Agent is ready when:
- ✅ All documentation complete
- ✅ All tests passing
- ✅ Deployed successfully
- ✅ Demo scenarios prepared
- ✅ Team familiar with features

---

## 📈 Next Steps

1. **Review** all documentation
2. **Test** locally with `./test_agent.sh`
3. **Deploy** using [DEPLOYMENT.md](DEPLOYMENT.md)
4. **Prepare** demo using [PITCH.md](PITCH.md)
5. **Win** the hackathon! 🚀

---

**Built with ❤️ by team Agents of Chaos for Buildathon 2026**

**Status**: ✅ Ready for Deployment  
**Last Updated**: March 7, 2026

---

## Quick Links

- [GitHub Repository](https://github.com/RMan2323/Nasiko-Agents-of-Chaos)
- [Nasiko Platform](https://nasiko.ai)
- [A2A Protocol](https://github.com/ashishsharma/nasiko)

---

**Happy Building! 🚀**
