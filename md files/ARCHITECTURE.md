# HR Agent Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Nasiko Platform                          │
│                   (A2A JSON-RPC 2.0)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Server                             │
│                  (Port 5000)                                 │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         JSON-RPC Request Handler                    │    │
│  │  - Validates A2A protocol                          │    │
│  │  - Extracts message text                           │    │
│  │  - Formats responses                               │    │
│  └──────────────────┬─────────────────────────────────┘    │
└────────────────────┬┴──────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  LangChain Agent                             │
│                  (GPT-4o)                                    │
│                                                              │
│  System Prompt: "You are an expert HR assistant..."         │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Tool Selection                         │    │
│  │  - Analyzes user request                           │    │
│  │  - Selects appropriate tool(s)                     │    │
│  │  - Executes tool calls                             │    │
│  │  - Formats final response                          │    │
│  └──────────────────┬─────────────────────────────────┘    │
└────────────────────┬┴──────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    7 LangChain Tools                         │
│                                                              │
│  1. schedule_interview    5. analyze_culture_fit            │
│  2. screen_candidate      6. research_salary                │
│  3. research_candidate    7. hr_assistant                   │
│  4. get_interview_prep                                      │
│                                                              │
│  Each tool delegates to modular architecture ───────────┐   │
└─────────────────────────────────────────────────────────┼───┘
                                                          │
                     ┌────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Modular Architecture Core                       │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │ Task Planner │──────▶│ Task Router  │                    │
│  │ (GPT-4o-mini)│      │              │                    │
│  └──────────────┘      └──────┬───────┘                    │
│         │                      │                             │
│         │ Breaks down          │ Routes to                  │
│         │ complex tasks        │ modules                    │
│         │                      │                             │
│         ▼                      ▼                             │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │   Executor   │──────▶│  Aggregator  │                    │
│  │              │      │ (GPT-4o-mini)│                    │
│  └──────┬───────┘      └──────────────┘                    │
│         │                      │                             │
│         │ Executes             │ Combines                   │
│         │ tasks                │ results                    │
│         │                      │                             │
└─────────┼──────────────────────┼─────────────────────────────┘
          │                      │
          ▼                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Specialized Modules                         │
│                                                              │
│  ┌────────────────────┐  ┌────────────────────┐            │
│  │ Calendar Manager   │  │    Recruiter       │            │
│  │                    │  │                    │            │
│  │ - Schedule         │  │ - Screen           │            │
│  │ - Find slots       │  │ - Shortlist        │            │
│  │ - Generate links   │  │ - Track pipeline   │            │
│  └────────────────────┘  └────────────────────┘            │
│                                                              │
│  ┌────────────────────┐  ┌────────────────────┐            │
│  │   Researcher       │  │ Interview Coach ⭐  │            │
│  │                    │  │                    │            │
│  │ - Candidate info   │  │ - Generate Q's     │            │
│  │ - Company info     │  │ - Coaching         │            │
│  │ - Salary data      │  │ - Feedback         │            │
│  │ - Market trends    │  │ - Tips             │            │
│  └────────────────────┘  └────────────────────┘            │
│                                                              │
│  ┌────────────────────┐                                     │
│  │ Culture Analyzer ⭐ │                                     │
│  │                    │                                     │
│  │ - Fit scoring      │                                     │
│  │ - Culture profiles │                                     │
│  │ - Team dynamics    │                                     │
│  │ - Values alignment │                                     │
│  └────────────────────┘                                     │
│                                                              │
│  ⭐ = Unique Features                                        │
└─────────────────────────────────────────────────────────────┘
```

## Request Flow

### Simple Request Flow
```
User Request
    │
    ▼
FastAPI Server (validates A2A protocol)
    │
    ▼
LangChain Agent (selects tool)
    │
    ▼
Tool (e.g., schedule_interview)
    │
    ▼
Modular Architecture
    │
    ├─▶ Planner: Creates task
    │
    ├─▶ Router: Routes to Calendar Manager
    │
    ├─▶ Executor: Runs Calendar Manager
    │
    └─▶ Aggregator: Formats response
    │
    ▼
Response to User
```

### Complex Multi-step Flow
```
User: "Research salary, screen candidate, schedule interview"
    │
    ▼
LangChain Agent (selects hr_assistant tool)
    │
    ▼
Modular Architecture
    │
    ├─▶ Planner: Breaks into 3 tasks
    │   ├─ Task 1: Research salary
    │   ├─ Task 2: Screen candidate
    │   └─ Task 3: Schedule interview
    │
    ├─▶ Router: Routes each task
    │   ├─ Task 1 → Researcher
    │   ├─ Task 2 → Recruiter
    │   └─ Task 3 → Calendar Manager
    │
    ├─▶ Executor: Runs all modules
    │   ├─ Researcher.execute()
    │   ├─ Recruiter.execute()
    │   └─ CalendarManager.execute()
    │
    └─▶ Aggregator: Combines all results
    │
    ▼
Comprehensive Response to User
```

## Module Architecture

### Base Module Interface
```python
class BaseModule(ABC):
    def can_handle(task) -> bool
    def execute(task) -> result
    def get_capabilities() -> list
```

### Module Implementation Example
```
CalendarManager (extends BaseModule)
    │
    ├─▶ can_handle()
    │   └─ Checks for scheduling keywords
    │
    ├─▶ execute()
    │   ├─ Extract parameters
    │   ├─ Find available slot
    │   ├─ Create event
    │   └─ Generate meeting link
    │
    └─▶ get_capabilities()
        └─ Returns list of features
```

## Data Flow

### Input Processing
```
A2A JSON-RPC Request
    │
    ▼
{
  "jsonrpc": "2.0",
  "id": "...",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{"kind": "text", "text": "..."}]
    }
  }
}
    │
    ▼
Extract text from parts
    │
    ▼
Pass to LangChain Agent
```

### Output Processing
```
Module Result
    │
    ▼
Aggregator combines results
    │
    ▼
LangChain Agent formats
    │
    ▼
{
  "jsonrpc": "2.0",
  "id": "...",
  "result": {
    "id": "task-id",
    "kind": "task",
    "status": {"state": "completed", ...},
    "artifacts": [{
      "parts": [{"kind": "text", "text": "..."}]
    }]
  }
}
```

## Technology Stack

### Core Technologies
```
┌─────────────────────────────────────┐
│         Python 3.11                  │
├─────────────────────────────────────┤
│ FastAPI      - Web framework         │
│ Uvicorn      - ASGI server          │
│ Pydantic     - Data validation      │
│ LangChain    - Agent framework      │
│ OpenAI       - LLM provider         │
│ Click        - CLI interface        │
└─────────────────────────────────────┘
```

### LLM Usage Strategy
```
┌─────────────────────────────────────┐
│ GPT-4o (Main Agent)                  │
│ - Tool selection                     │
│ - Complex reasoning                  │
│ - Module execution                   │
│ Temperature: 0.2                     │
├─────────────────────────────────────┤
│ GPT-4o-mini (Planning/Aggregation)   │
│ - Task planning                      │
│ - Result aggregation                 │
│ Temperature: 0-0.3                   │
└─────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────┐
│      Nasiko Platform                 │
│                                      │
│  ┌────────────────────────────┐    │
│  │   Agent Registry           │    │
│  │   - Stores AgentCard       │    │
│  │   - Routes requests        │    │
│  └────────┬───────────────────┘    │
│           │                         │
│           ▼                         │
│  ┌────────────────────────────┐    │
│  │   Docker Container         │    │
│  │   - HR Agent               │    │
│  │   - Port 5000              │    │
│  │   - External network       │    │
│  └────────────────────────────┘    │
└─────────────────────────────────────┘
```

## Security & Configuration

### Environment Variables
```
OPENAI_API_KEY
    │
    ├─▶ Set in docker-compose.yml
    ├─▶ Passed to container
    └─▶ Used by LangChain
```

### Network Configuration
```
agents-net (external network)
    │
    ├─▶ Allows inter-agent communication
    └─▶ Managed by Nasiko platform
```

## Scalability Considerations

### Horizontal Scaling
```
Load Balancer
    │
    ├─▶ HR Agent Instance 1
    ├─▶ HR Agent Instance 2
    └─▶ HR Agent Instance N
```

### Module Independence
```
Each module is independent:
- Can be scaled separately
- Can be replaced/upgraded
- Can be tested in isolation
```

## Extension Points

### Adding New Modules
```
1. Create new module in src/modules/
2. Extend BaseModule
3. Implement can_handle() and execute()
4. Register in agent.py router
5. Create corresponding tool in tools.py
6. Update agent prompt
```

### Adding New Tools
```
1. Define @tool in tools.py
2. Add to agent.tools list
3. Update system prompt
4. Test with curl/test script
```

---

**Architecture designed for:**
- ✅ Modularity
- ✅ Extensibility
- ✅ Testability
- ✅ Scalability
- ✅ Maintainability

**Built by team Agents of Chaos for Buildathon 2026** 🚀
