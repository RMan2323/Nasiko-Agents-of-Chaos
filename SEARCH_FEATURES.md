# Database Search Features

## Overview
The HR Agent now has powerful search capabilities to find candidates by various criteria without needing email addresses.

## Available Search Tools

### 1. Search by Name (`search_candidates_by_name`)
Find candidates by their name (supports partial matching).

**Examples:**
- "Give me information about Bob"
- "Tell me about Sarah"
- "Find candidate Smith"

**Features:**
- Case-insensitive search
- Partial name matching (e.g., "Bob" finds "Bob Smith")
- Returns full candidate details

### 2. Search by Skills (`search_candidates_by_skills`)
Find all candidates who have specific skills.

**Examples:**
- "Show me all candidates who know Python"
- "Find candidates with React skills"
- "Who knows AWS and Docker?"

**Features:**
- Case-insensitive search
- Multiple skills support (comma-separated)
- Shows matching skills highlighted
- Returns candidates with ANY of the specified skills

### 3. Advanced Search (`search_candidates_advanced`)
Search by multiple criteria simultaneously.

**Examples:**
- "Show me all candidates from MIT"
- "Find candidates with CPI above 8.5"
- "Show candidates with 5+ years experience"
- "Find screened candidates from Stanford"

**Criteria:**
- College/University (partial match)
- Minimum CPI/GPA
- Minimum years of experience
- Status (applied, screened, interviewed, etc.)

### 4. Search by Email (`get_candidate_from_database`)
Direct lookup by email address (exact match).

**Examples:**
- "Get candidate bob@example.com"
- "Show me sarah@example.com details"

## How It Works

The agent automatically selects the appropriate search tool based on your query:

1. **Name mentioned** → Uses `search_candidates_by_name`
2. **Skills mentioned** → Uses `search_candidates_by_skills`
3. **College/CPI/Experience mentioned** → Uses `search_candidates_advanced`
4. **Email mentioned** → Uses `get_candidate_from_database`

## Database Integration

All search tools query MongoDB directly:
- ✅ Real-time data from MongoDB Atlas
- ✅ Efficient indexed searches
- ✅ Supports regex for partial matching
- ✅ Returns complete candidate profiles

## Example Queries

```bash
# Search by name
curl -X POST http://localhost:5000/ -H "Content-Type: application/json" -d '{
  "jsonrpc":"2.0",
  "id":"1",
  "method":"message/send",
  "params":{
    "message":{
      "role":"user",
      "parts":[{"kind":"text","text":"Give me information about Bob"}]
    }
  }
}'

# Search by skills
curl -X POST http://localhost:5000/ -H "Content-Type: application/json" -d '{
  "jsonrpc":"2.0",
  "id":"2",
  "method":"message/send",
  "params":{
    "message":{
      "role":"user",
      "parts":[{"kind":"text","text":"Show me all candidates who know Python"}]
    }
  }
}'

# Search by college
curl -X POST http://localhost:5000/ -H "Content-Type: application/json" -d '{
  "jsonrpc":"2.0",
  "id":"3",
  "method":"message/send",
  "params":{
    "message":{
      "role":"user",
      "parts":[{"kind":"text","text":"Show me all candidates from MIT"}]
    }
  }
}'
```

## Test Script

Run the comprehensive test script:
```bash
./test_search.sh
```

## Current Database

The system currently has these candidates in MongoDB:
- **Sarah Chen** - MIT, Python/ML/AWS, 5 years experience
- **Bob Smith** - Berkeley, React/Node.js, 4 years experience
- **John Doe** - MIT, Python/AWS, 5 years experience
- **Alice Johnson** - Stanford, Java/Docker, 3 years experience

## Technical Details

### MongoDB Queries
- Name search: `{"name": {"$regex": "Bob", "$options": "i"}}`
- Skills search: `{"skills": {"$regex": "Python|AWS", "$options": "i"}}`
- Advanced: `{"college": {"$regex": "MIT", "$options": "i"}, "cpi": {"$gte": 8.5}}`

### Response Format
All search tools return formatted text with:
- Candidate name and email
- College and degree
- CPI/GPA
- Skills list
- Years of experience
- Current status
- Screening scores (if available)

## Benefits

1. **No email required** - Search by any attribute
2. **Flexible queries** - Natural language understanding
3. **Fast results** - Indexed MongoDB queries
4. **Complete profiles** - All candidate information returned
5. **Smart routing** - Agent picks the right tool automatically
