
---

# HR AI Agent System

An **Agentic HR Assistant** built with modular architecture.
The system plans tasks using an LLM, routes them to specialized modules, executes them, and aggregates results.

The agent can assist with:

* Candidate screening
* Interview scheduling
* Candidate research
* Culture fit analysis
* Sending emails
* Managing recruitment pipelines

---

# Setup

## Build Docker Image

```bash
docker build -t my-agent .
```

## Run Container

```bash
docker run -p 5000:5000 --env-file .env my-agent
```

---

## Windows Request Example

```bash
curl.exe -X POST http://localhost:5000/ \
-H "Content-Type: application/json" \
-d "@curlPOST.json"
```

---

## Configuration

Before running the system, ensure the following APIs and credentials are configured:

- Google Calendar API
- Gmail API
- OpenAI API
- MongoDB Database

Create a `.env` file in the project root with the following variables:

```env
OPENAI_API_KEY=
GOOGLE_API_KEY=
GOOGLE_CREDENTIALS_PATH=
MONGODB_URI=
MONGODB_DATABASE=HR-Database
USE_MONGODB=true
```

# System Architecture

The system follows a **modular agent pipeline**.

```
User Request
      │
      ▼
Agent (agent.py)
      │
      ▼
Tools Layer
      │
      ▼
Planner → Executor → Router → Modules
      │
      ▼
Aggregator
      │
      ▼
Final Response
```

### Responsibilities

| Component  | Responsibility                |
| ---------- | ----------------------------- |
| Planner    | Convert user query into tasks |
| Executor   | Execute tasks sequentially    |
| Router     | Select appropriate module     |
| Modules    | Perform domain specific work  |
| Aggregator | Combine outputs               |

---

# Execution Flow

1️⃣ `__main__.py` starts the FastAPI server.

2️⃣ Requests are forwarded to **agent.py**.

3️⃣ `agent.py` initializes:

* planner
* executor
* router
* aggregator

4️⃣ Agent forwards queries to **tools.py**.

5️⃣ `tools.py` orchestrates:

```
Planner → Executor → Aggregator
```

6️⃣ Executor routes tasks to modules.

7️⃣ Modules perform the actual work.

8️⃣ Aggregator combines results using LLM enhancement.

---

# Project Structure

```
src/
│
├── __main__.py
├── agent.py
├── models.py
├── tools.py
│
├── core/
│   ├── planner.py
│   ├── executor.py
│   ├── router.py
│   ├── aggregator.py
│   └── base_module.py
│
├── modules/
│   ├── calendar_manager.py
│   ├── culture_analyzer.py
│   ├── interview_coach.py
│   ├── recruiter.py
│   └── researcher.py
│
└── utils/
    ├── database.py
    ├── gmail.py
    ├── google_calendar.py
    └── mongodb_database.py
```

---

# Core Components

## Agent (`agent.py`)

Central orchestrator of the system.

Responsibilities:

* Register modules
* Create prompts
* Manage tool usage
* Process incoming messages

Main method:

```
process_message(message_text)
```

---

# Core Agent System

## Planner (`planner.py`)

Responsible for **task planning using LLM reasoning**.

Example output:

```json
[
  {
    "module": "recruiter",
    "task": "screen_candidate",
    "parameters": {
      "candidate_email": "abc@email.com"
    }
  }
]
```

---

## Executor (`executor.py`)

Executes tasks sequentially.

Flow:

```
task → router → module.execute() → result
```

Returns:

```
list[str]
```

---

## Router (`router.py`)

Routes tasks to the correct module.

Example mapping:

```
calendar → CalendarManager
recruiter → Recruiter
research → Researcher
```

---

## Aggregator (`aggregator.py`)

Combines outputs from modules.

Example:

```
["result1", "result2"]
      ↓
"Final combined response"
```

LLM may enhance responses before returning.

---

## Base Module (`base_module.py`)

Defines the **standard interface** for all modules.

Every module must implement:

```
can_handle(task)
execute(task)
get_capabilities()
```

This enables **plug-and-play modules**.

---

# Modules

Modules contain domain-specific logic.

---

## Calendar Manager

Handles:

* interview scheduling
* calendar event creation
* slot finding
* event cancellation

Uses **Google Calendar API**.

---

## Recruiter

Handles:

* candidate addition
* screening
* shortlisting
* pipeline tracking
* recruitment insights

---

## Researcher

Handles:

* candidate research
* company research
* salary research
* market trend analysis

---

## Culture Analyzer

Analyzes:

* candidate-company cultural fit
* team compatibility
* value alignment

Produces a **fit score**.

---

## Interview Coach

Provides:

* interview questions
* feedback
* preparation tips
* interview difficulty analysis

---

# Utilities

Utility layer provides integrations and shared services.

---

## Database (`database.py`)

Local candidate database.

Supports:

* add candidate
* update candidate
* search candidates
* interview tracking

---

## MongoDB Database (`mongodb_database.py`)

Production-ready candidate database.

Supports:

* candidate management
* interview pipeline
* job postings
* analytics

---

## Gmail (`gmail.py`)

Handles email communication:

* interview invitations
* screening updates
* offer letters

---

## Google Calendar (`google_calendar.py`)

Handles:

* event creation
* slot search
* event retrieval
* event cancellation

---


---

# My new point / idea / suggestion

Add a **Task Validator Layer** between Planner and Executor.

```
Planner
   ↓
Validator
   ↓
Executor
```

Validator checks:

* invalid modules
* missing parameters
* malformed JSON

This prevents **LLM-generated errors from breaking execution**.

---