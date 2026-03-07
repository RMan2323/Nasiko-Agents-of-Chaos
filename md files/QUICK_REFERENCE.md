# HR Agent - Quick Reference Guide

## 🚀 Quick Start

```bash
# Build and run
docker build -t hr-agent Nasiko-Agents-of-Chaos/
docker run -d --name hr-agent-test --env-file Nasiko-Agents-of-Chaos/.env -p 5000:5000 hr-agent

# Check status
curl http://localhost:5000/health
```

---

## 📋 Common Commands

### Candidate Management
```bash
# Add candidate
"Add candidate [Name], email [email], college [college], CPI [score], skills [skills], [X] years experience"

# Search by name
"Give me information about [Name]"

# Search by skills
"Show me all candidates who know [skill]"

# Search by college
"Show me all candidates from [college]"

# Get by email
"Get candidate [email]"
```

### Screening & Interviews
```bash
# Screen candidate
"Screen candidate [email] for [position]"

# Schedule interview
"Schedule a [type] interview with [name] next week"

# Generate questions
"Generate [difficulty] [type] interview questions for [role]"

# Culture fit
"Analyze culture fit between [candidate] and our company"
```

---

## 🔧 Configuration Files

### .env
```bash
OPENAI_API_KEY=your_key
MONGODB_URI=mongodb+srv://...
MONGODB_DATABASE=HR-Database
USE_MONGODB=true
```

---

## 📊 Available Tools

1. **add_candidate_to_database** - Add new candidates
2. **get_candidate_from_database** - Get by email
3. **search_candidates_by_name** - Search by name
4. **search_candidates_by_skills** - Search by skills
5. **search_candidates_advanced** - Advanced filtering
6. **schedule_interview** - Schedule interviews
7. **screen_candidate** - Screen and evaluate
8. **research_candidate** - Research backgrounds
9. **get_interview_prep** - Interview preparation
10. **analyze_culture_fit** - Culture analysis
11. **research_salary** - Salary research
12. **hr_assistant** - General HR tasks

---

## 🐛 Troubleshooting

### Check logs
```bash
docker logs hr-agent-test
```

### Restart agent
```bash
docker stop hr-agent-test
docker rm hr-agent-test
docker run -d --name hr-agent-test --env-file Nasiko-Agents-of-Chaos/.env -p 5000:5000 hr-agent
```

### Test connection
```bash
curl http://localhost:5000/health
```

---

## 📈 Performance Tips

- Database connection is cached (singleton pattern)
- MongoDB uses indexed queries for speed
- LLM has 30-second timeout with retries
- Agent initializes on startup (not per request)

---

## 🔗 Useful Links

- **MongoDB Atlas**: https://cloud.mongodb.com
- **OpenAI API**: https://platform.openai.com
- **FastAPI Docs**: http://localhost:5000/docs (when running)

---

## 📝 Example Queries

```
"Add candidate Sarah Chen, email sarah@example.com, college MIT, CPI 9.2, skills Python and ML, 5 years experience"

"Show me all candidates who know Python"

"Give me information about Bob"

"Screen candidate sarah@example.com for Senior Software Engineer position"

"Schedule a technical interview with Bob Smith next week"

"Generate medium difficulty technical interview questions for Full Stack Developer"

"Show me all candidates from MIT"

"Find candidates with CPI above 8.5"
```

---

## ⚡ Quick Tests

```bash
# Test search
./test_search.sh

# Test general functionality
./test_correct.sh

# Test MongoDB
python test_mongodb.py
```

---

**For detailed documentation, see:**
- FINAL_SUMMARY.md - Complete overview
- OPTIMIZATIONS.md - Performance details
- SEARCH_FEATURES.md - Search capabilities
- MONGODB_COMPLETE.md - Database setup
