# API Integration Guide

## 🔄 Current vs Enhanced Architecture

### ❌ Before (Mock/Simulated)
- **Calendar**: Fake meeting links
- **Email**: Console output only
- **Database**: No persistence
- **Research**: LLM-generated fictional data

### ✅ After (Real APIs)
- **Calendar**: Google Calendar API with real Google Meet links
- **Email**: Gmail API sending actual emails
- **Database**: File-based storage (upgradeable to PostgreSQL/MongoDB)
- **Research**: Database lookups + LLM analysis

---

## 📊 What Changed

### 1. Database Integration ✅

**File**: `src/utils/database.py`

**What it does**:
- Stores candidate information persistently
- Tracks interviews, screening scores, culture fit scores
- Supports search and updates

**Data stored**:
```python
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "college": "MIT",
    "degree": "B.Tech Computer Science",
    "cpi": 8.5,
    "graduation_year": "2020",
    "skills": ["Python", "React", "AWS"],
    "experience_years": 5,
    "resume_url": "https://...",
    "linkedin_url": "https://linkedin.com/in/...",
    "github_url": "https://github.com/...",
    "screening_score": 85,
    "culture_fit_score": 78,
    "interviews": [...]
}
```

**Usage**:
```python
from utils.database import get_database

db = get_database()

# Add candidate
db.add_candidate({
    "name": "Sarah Chen",
    "email": "sarah@example.com",
    "college": "Stanford",
    "cpi": 9.2,
    "skills": ["Python", "ML", "TensorFlow"]
})

# Get candidate
candidate = db.get_candidate("sarah@example.com")

# Update
db.update_candidate("sarah@example.com", {
    "screening_score": 92
})
```

---

### 2. Google Calendar Integration ✅

**File**: `src/utils/google_calendar.py`

**What it does**:
- Creates real calendar events
- Generates Google Meet links automatically
- Sends calendar invites to attendees
- Finds available time slots

**Setup Required**:

#### Step 1: Enable Google Calendar API
```bash
1. Go to https://console.cloud.google.com/
2. Create new project or select existing
3. Enable "Google Calendar API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Download credentials.json
```

#### Step 2: Set Environment Variable
```bash
export GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json
```

#### Step 3: First Run (OAuth Flow)
```bash
# First time you run, it will open browser for authorization
# After authorization, token is saved for future use
```

**Features**:
- ✅ Real Google Calendar events
- ✅ Automatic Google Meet link generation
- ✅ Email invitations to attendees
- ✅ Calendar reminders
- ⚠️ Falls back to mock if not configured

---

### 3. Gmail Integration ✅

**File**: `src/utils/gmail.py`

**What it does**:
- Sends real emails to candidates
- Interview invitations
- Status updates
- Offer letters

**Setup Required**:

#### Step 1: Enable Gmail API
```bash
1. Go to https://console.cloud.google.com/
2. Same project as Calendar API
3. Enable "Gmail API"
4. Use same OAuth credentials
```

#### Step 2: Set Environment Variable
```bash
export GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json
# (Same as Calendar API)
```

**Email Templates**:

1. **Interview Invitation**:
```
Subject: Interview Invitation - Technical Interview

Dear Sarah Chen,

We are pleased to invite you for a technical interview.

Interview Details:
- Date: March 9, 2026
- Time: 10:00 AM
- Duration: 60 minutes
- Meeting Link: https://meet.google.com/abc-defg-hij

Please confirm your availability...
```

2. **Screening Update**:
```
Subject: Application Update - Screened

Dear Michael Rodriguez,

Thank you for your application. We wanted to update you...

Status: Screened
Next Steps: Technical interview scheduled

...
```

**Features**:
- ✅ Real email sending
- ✅ Professional templates
- ✅ CC support
- ✅ HTML email support
- ⚠️ Falls back to console output if not configured

---

### 4. Updated Modules

#### Calendar Manager (`src/modules/calendar_manager.py`)
**Changes**:
- ✅ Uses Google Calendar API
- ✅ Stores events in database
- ✅ Sends email invitations
- ✅ Real Google Meet links

**Before**:
```python
meeting_link = f"https://meet.company.com/{random_id}"
```

**After**:
```python
event = calendar_api.create_event(
    summary="Technical Interview - Sarah Chen",
    start_time=datetime(...),
    duration_minutes=60,
    attendees=["sarah@example.com", "hr@company.com"]
)
# Returns real Google Meet link
```

#### Recruiter (`src/modules/recruiter.py`)
**Changes**:
- ✅ Stores candidates in database
- ✅ Retrieves candidate data from database
- ✅ Updates screening scores
- ✅ Sends email notifications

**Before**:
```python
# No persistence, LLM-only analysis
```

**After**:
```python
# Get from database
candidate = db.get_candidate(email)

# Use real data in LLM prompt
prompt = f"""
Database Information:
- College: {candidate['college']}
- CPI: {candidate['cpi']}
- Skills: {candidate['skills']}
...
"""

# Update database
db.update_candidate(email, {"screening_score": 85})
```

---

## 🚀 How to Use

### Option 1: With Google APIs (Production)

#### 1. Setup Google Cloud Project
```bash
# Follow setup instructions above for Calendar and Gmail APIs
```

#### 2. Set Environment Variables
```bash
export GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json
export OPENAI_API_KEY=sk-proj-...
```

#### 3. Build and Run
```bash
docker build -t hr-agent .
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e GOOGLE_CREDENTIALS_PATH=/credentials.json \
  -v /path/to/credentials.json:/credentials.json \
  hr-agent
```

#### 4. First Run Authorization
```bash
# Browser will open for Google OAuth
# Authorize the application
# Token saved for future use
```

---

### Option 2: Without Google APIs (Mock Mode)

#### 1. Just Run
```bash
export OPENAI_API_KEY=sk-proj-...
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY hr-agent
```

#### 2. What Happens
- ✅ Everything works
- ⚠️ Calendar events are mocked
- ⚠️ Emails printed to console
- ✅ Database still works (file-based)
- ✅ All LLM features work

**Mock Output Example**:
```
MOCK EMAIL (Gmail API not configured)
============================================================
To: sarah@example.com
Subject: Interview Invitation - Technical Interview
Body:
Dear Sarah Chen,
We are pleased to invite you...
============================================================
```

---

## 📦 Required Dependencies

### For Google APIs
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Update Dockerfile
```dockerfile
RUN pip install --no-cache-dir \
  fastapi>=0.109.0 \
  uvicorn>=0.27.0 \
  pydantic>=2.6.0 \
  python-dotenv>=1.0.0 \
  requests>=2.31.0 \
  "langchain>=0.2.0,<0.3.0" \
  "langchain-openai>=0.1.0,<0.2.0" \
  click>=8.1.7 \
  google-auth>=2.0.0 \
  google-auth-oauthlib>=1.0.0 \
  google-auth-httplib2>=0.1.0 \
  google-api-python-client>=2.0.0
```

---

## 🔧 Testing

### Test Database
```bash
curl -X POST http://localhost:5000/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-db",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{
          "kind": "text",
          "text": "Add candidate Sarah Chen, email sarah@example.com, college MIT, CPI 9.2, skills Python and ML"
        }]
      }
    }
  }'
```

### Test Calendar (with API)
```bash
curl -X POST http://localhost:5000/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-cal",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{
          "kind": "text",
          "text": "Schedule technical interview with sarah@example.com for next Tuesday"
        }]
      }
    }
  }'
```

**Expected**: Real Google Calendar event created + email sent

---

## 🎯 Production Deployment

### 1. Database Upgrade (Recommended)

Replace file-based database with PostgreSQL:

```python
# src/utils/database.py
import psycopg2

class CandidateDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
```

### 2. Service Account (Recommended)

For production, use service account instead of OAuth:

```python
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    '/path/to/service-account-key.json',
    scopes=['https://www.googleapis.com/auth/calendar']
)
```

### 3. Environment Variables
```bash
# Required
OPENAI_API_KEY=sk-proj-...

# Optional (for Google APIs)
GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json
GOOGLE_CALENDAR_ID=primary

# Optional (for PostgreSQL)
DB_HOST=localhost
DB_NAME=hr_agent
DB_USER=postgres
DB_PASSWORD=...
```

---

## 📊 Feature Comparison

| Feature | Mock Mode | With APIs |
|---------|-----------|-----------|
| Candidate Storage | ✅ File-based | ✅ File-based (upgradeable) |
| Calendar Events | ⚠️ Fake links | ✅ Real Google Calendar |
| Meeting Links | ⚠️ Mock URLs | ✅ Real Google Meet |
| Email Sending | ⚠️ Console only | ✅ Real Gmail |
| Interview Scheduling | ✅ Works | ✅ Works + Real invites |
| Candidate Screening | ✅ Works | ✅ Works + DB storage |
| Culture Fit Analysis | ✅ Works | ✅ Works + DB storage |
| Interview Coach | ✅ Works | ✅ Works |

---

## 🎉 Summary

### What's Real Now:
1. ✅ **Database** - Persistent candidate storage
2. ✅ **Google Calendar** - Real events and Meet links
3. ✅ **Gmail** - Actual email sending
4. ✅ **Graceful Fallback** - Works without APIs (mock mode)

### What's Still LLM-Based (Good!):
1. ✅ **Interview Coach** - Generates questions (should be LLM)
2. ✅ **Culture Fit Analysis** - Analyzes compatibility (should be LLM)
3. ✅ **Researcher** - Market insights (should be LLM)

### Next Steps:
1. Set up Google Cloud Project
2. Enable Calendar and Gmail APIs
3. Download credentials
4. Update Dockerfile with dependencies
5. Test with real APIs
6. Deploy to production

---

**Your agent now has REAL integrations!** 🚀

Mock mode still works perfectly for development and demos.
