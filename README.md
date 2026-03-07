# HR Agent - Agents of Chaos

> Built for Buildathon 2026 by team **Agents of Chaos**

A comprehensive AI-powered HR assistant that helps with scheduling, recruiting, candidate research, interview preparation, and culture fit analysis.

## 🌟 Features

### Core Capabilities

1. **📅 Calendar Management**
   - Schedule interviews and meetings
   - Find available time slots
   - Generate meeting links
   - Manage calendar events

2. **👥 Recruitment & Screening**
   - Screen and evaluate candidates
   - Create candidate shortlists
   - Track recruitment pipeline
   - Provide hiring recommendations
   - Assess candidate-role fit

3. **🔍 Research & Intelligence**
   - Research candidate backgrounds
   - Company information lookup
   - Salary and compensation research
   - Market trend analysis
   - Industry insights

### 🎯 Unique Features

4. **AI Interview Coach** ⭐
   - Generate tailored interview questions
   - Provide interview feedback and coaching
   - Mock interview practice
   - Interview tips and strategies
   - Behavioral question coaching
   - Post-interview analysis

5. **Culture Fit Analyzer** ⭐
   - Assess candidate-company alignment
   - Create culture profiles
   - Analyze team dynamics
   - Values alignment analysis
   - Work style compatibility
   - Long-term success prediction

## 🏗️ Architecture

The agent uses a modular architecture with specialized modules:

```
src/
├── agent.py              # Main agent orchestration
├── tools.py              # LangChain tool definitions
├── core/                 # Modular architecture framework
│   ├── planner.py        # Task planning and breakdown
│   ├── router.py         # Task routing to modules
│   ├── executor.py       # Task execution
│   ├── aggregator.py     # Result aggregation
│   └── base_module.py    # Base module interface
└── modules/              # Specialized HR modules
    ├── calendar_manager.py    # Scheduling
    ├── recruiter.py           # Recruitment
    ├── researcher.py          # Research
    ├── interview_coach.py     # Interview prep (Unique!)
    └── culture_analyzer.py    # Culture fit (Unique!)
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed
- OpenAI API Key
- Git (for GitHub deployment)

### Local Testing

1. **Build the Docker container:**
```bash
cd Nasiko-Agents-of-Chaos
docker build -t hr-agent .
```

2. **Run the agent:**
```bash
export OPENAI_API_KEY=your_openai_api_key_here
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent
```

3. **Test with curl:**
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
          "text": "Schedule a technical interview with Sarah Chen for next week"
        }]
      }
    }
  }'
```

## 💬 Example Interactions

### Scheduling
```
User: "Schedule a technical interview with John Doe for next Tuesday"
Agent: Schedules interview, provides meeting link and details
```

### Candidate Screening
```
User: "Screen candidate Sarah Chen for Senior Software Engineer role. She has 8 years of Python experience and led multiple teams."
Agent: Provides match score, strengths, concerns, and recommendation
```

### Interview Preparation
```
User: "Generate interview questions for a Product Manager position"
Agent: Provides tailored questions with guidance on what to look for
```

### Culture Fit Analysis
```
User: "Analyze culture fit between Michael Rodriguez and our startup environment"
Agent: Provides fit score, alignment areas, potential friction points, and recommendations
```

### Salary Research
```
User: "What's the salary range for a senior data scientist in San Francisco?"
Agent: Provides detailed salary ranges and market insights
```

## 🛠️ Available Tools

The agent exposes these tools:

- `schedule_interview` - Schedule interviews with candidates
- `screen_candidate` - Evaluate and screen candidates
- `research_candidate` - Research candidate backgrounds
- `get_interview_prep` - Generate interview questions and prep materials
- `analyze_culture_fit` - Assess culture compatibility
- `research_salary` - Get salary data and compensation info
- `hr_assistant` - Handle complex multi-step HR tasks

## 📦 Deployment

### Method 1: GitHub (Recommended)

1. Push your code to GitHub
2. Log into Nasiko dashboard
3. Click "Connect GitHub"
4. Select your repository
5. Agent will be automatically deployed

### Method 2: ZIP Upload

1. Create ZIP file:
```bash
cd ..
zip -r hr-agent.zip Nasiko-Agents-of-Chaos/ -x "*.pyc" "*/__pycache__/*" "*/.git/*"
```

2. Upload via Nasiko dashboard
3. Agent will be built and deployed

## 🧪 Testing Scenarios

### Test 1: Multi-step Recruitment
```json
{
  "jsonrpc": "2.0",
  "id": "test-multi",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{
        "kind": "text",
        "text": "I need to hire a senior engineer. Research the market, screen candidate Alex Kim, and schedule an interview if they're a good fit."
      }]
    }
  }
}
```

### Test 2: Interview Coaching
```json
{
  "jsonrpc": "2.0",
  "id": "test-coach",
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
}
```

### Test 3: Culture Analysis
```json
{
  "jsonrpc": "2.0",
  "id": "test-culture",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{
        "kind": "text",
        "text": "Analyze culture fit between candidate Emma Wilson and our fast-paced startup"
      }]
    }
  }
}
```

## 🎨 What Makes This Agent Unique

1. **AI Interview Coach**: Goes beyond basic Q&A to provide comprehensive interview preparation, feedback, and coaching - helping both interviewers and candidates succeed.

2. **Culture Fit Analyzer**: Uses advanced analysis to predict long-term success by assessing values alignment, work style compatibility, and team dynamics.

3. **Modular Architecture**: Clean separation of concerns allows easy extension and maintenance. Each module is independent and can be enhanced separately.

4. **Intelligent Task Planning**: Automatically breaks down complex HR requests into actionable subtasks and routes them to appropriate specialists.

5. **Comprehensive HR Coverage**: Single agent handles the entire recruitment lifecycle from research to scheduling to evaluation.

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key

### Customization

To customize the agent:

1. **Add new modules**: Create a new module in `src/modules/` inheriting from `BaseModule`
2. **Register module**: Add to `agent.py` in the `__init__` method
3. **Create tools**: Add corresponding tools in `tools.py`
4. **Update prompt**: Modify the system prompt in `agent.py` to include new capabilities

## 📊 Performance

- Average response time: 2-5 seconds
- Supports concurrent requests
- Modular design allows parallel task execution
- Efficient LLM usage with targeted prompts

## 🤝 Contributing

Built by team **Agents of Chaos** for Buildathon 2026.

Team members can extend functionality by:
1. Adding new modules in `src/modules/`
2. Creating new tools in `src/tools.py`
3. Enhancing existing module capabilities

## 📝 License

Built for Buildathon 2026.

## 🆘 Troubleshooting

### Agent won't start
- Check that `OPENAI_API_KEY` is set
- Verify Docker is running
- Check port 5000 is available

### Tools not working
- Ensure all modules are properly registered in `agent.py`
- Check that `set_modular_components()` is called
- Verify LLM has access to tool descriptions

### Slow responses
- Consider using `gpt-4o-mini` for faster responses
- Reduce temperature for more deterministic outputs
- Cache frequently accessed data

## 📞 Support

For issues or questions during the hackathon, contact team **Agents of Chaos**.

---

**Built with ❤️ for Buildathon 2026**
