# MongoDB Setup Guide

Complete guide for setting up MongoDB with your HR Agent.

---

## 🎯 Why MongoDB?

- ✅ **Flexible Schema** - Store varying candidate data easily
- ✅ **Scalable** - Handles millions of candidates
- ✅ **Fast Queries** - Indexed searches for quick lookups
- ✅ **Rich Queries** - Complex filtering and aggregation
- ✅ **Cloud Ready** - MongoDB Atlas for production

---

## 📦 Option 1: Local MongoDB (Development)

### Step 1: Install MongoDB

#### Ubuntu/Debian:
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update and install
sudo apt-get update
sudo apt-get install -y mongodb-org
```

#### macOS:
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
```

#### Windows:
Download installer from: https://www.mongodb.com/try/download/community

### Step 2: Start MongoDB

#### Ubuntu/Debian:
```bash
sudo systemctl start mongod
sudo systemctl enable mongod  # Start on boot
sudo systemctl status mongod  # Check status
```

#### macOS:
```bash
brew services start mongodb-community@7.0
```

#### Windows:
MongoDB runs as a service automatically after installation.

### Step 3: Verify Installation

```bash
# Connect to MongoDB shell
mongosh

# You should see:
# Current Mongosh Log ID: ...
# Connecting to: mongodb://127.0.0.1:27017/
# Using MongoDB: 7.0.x
```

### Step 4: Install Python Driver

```bash
pip install pymongo
```

### Step 5: Configure Environment

```bash
# Default local MongoDB
export MONGODB_URI="mongodb://localhost:27017/"
export MONGODB_DATABASE="hr_agent"
export USE_MONGODB="true"
```

### Step 6: Test Connection

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.hr_agent

# Test
db.test.insert_one({"test": "success"})
print("✅ MongoDB connected!")
```

---

## ☁️ Option 2: MongoDB Atlas (Production/Cloud)

### Step 1: Create Account

1. Go to https://www.mongodb.com/cloud/atlas/register
2. Sign up for free account
3. Verify email

### Step 2: Create Cluster

1. Click "Build a Database"
2. Choose "M0 Free" tier
3. Select cloud provider (AWS/GCP/Azure)
4. Choose region closest to you
5. Click "Create Cluster"
6. Wait 3-5 minutes for cluster creation

### Step 3: Create Database User

1. Go to "Database Access" in left menu
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Username: `hr_agent_user`
5. Password: Generate strong password (save it!)
6. Database User Privileges: "Read and write to any database"
7. Click "Add User"

### Step 4: Configure Network Access

1. Go to "Network Access" in left menu
2. Click "Add IP Address"
3. For development: Click "Allow Access from Anywhere" (0.0.0.0/0)
4. For production: Add your server's IP address
5. Click "Confirm"

### Step 5: Get Connection String

1. Go to "Database" in left menu
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string:
```
mongodb+srv://hr_agent_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```
5. Replace `<password>` with your actual password

### Step 6: Configure Environment

```bash
export MONGODB_URI="mongodb+srv://hr_agent_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
export MONGODB_DATABASE="hr_agent"
export USE_MONGODB="true"
```

### Step 7: Install Python Driver

```bash
pip install pymongo[srv]  # Note: [srv] for Atlas
```

---

## 🐳 Docker Setup

### Update Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY src/ /app

RUN pip install --no-cache-dir \
  fastapi>=0.109.0 \
  uvicorn>=0.27.0 \
  pydantic>=2.6.0 \
  python-dotenv>=1.0.0 \
  requests>=2.31.0 \
  "langchain>=0.2.0,<0.3.0" \
  "langchain-openai>=0.1.0,<0.2.0" \
  click>=8.1.7 \
  pymongo>=4.6.0

ENV PYTHONUNBUFFERED=1

CMD ["python", "__main__.py", "--host", "0.0.0.0", "--port", "5000"]
```

### Update docker-compose.yml

#### Option A: With Local MongoDB Container

```yaml
services:
  mongodb:
    image: mongo:7.0
    container_name: hr-agent-mongodb
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=admin123
      - MONGO_INITDB_DATABASE=hr_agent
    volumes:
      - mongodb_data:/data/db
    networks:
      - agents-net

  hr-agent:
    build: .
    container_name: hr-agent-chaos
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MONGODB_URI=mongodb://admin:admin123@mongodb:27017/
      - MONGODB_DATABASE=hr_agent
      - USE_MONGODB=true
    stdin_open: true
    ports:
      - "5000"
    tty: true
    depends_on:
      - mongodb
    networks:
      - agents-net

volumes:
  mongodb_data:

networks:
  agents-net:
    external: true
```

#### Option B: With MongoDB Atlas

```yaml
services:
  hr-agent:
    build: .
    container_name: hr-agent-chaos
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MONGODB_URI=${MONGODB_URI}
      - MONGODB_DATABASE=hr_agent
      - USE_MONGODB=true
    stdin_open: true
    ports:
      - "5000"
    tty: true
    networks:
      - agents-net

networks:
  agents-net:
    external: true
```

---

## 📊 Database Schema

### Candidates Collection

```javascript
{
  "_id": ObjectId("..."),
  "email": "sarah@example.com",  // Unique index
  "name": "Sarah Chen",
  "phone": "+1234567890",
  
  // Education
  "college": "MIT",
  "degree": "B.Tech Computer Science",
  "cpi": 9.2,
  "graduation_year": "2020",
  
  // Professional
  "skills": ["Python", "React", "AWS"],
  "experience_years": 5,
  "current_company": "Tech Corp",
  "current_position": "Senior Engineer",
  
  // Links
  "resume_url": "https://...",
  "linkedin_url": "https://linkedin.com/in/...",
  "github_url": "https://github.com/...",
  "portfolio_url": "https://...",
  
  // Application
  "applied_position": "Senior Software Engineer",
  "status": "screened",  // applied, screened, interviewing, offered, hired, rejected
  "source": "linkedin",  // direct, linkedin, referral, job_board
  
  // Scores
  "screening_score": 92,
  "culture_fit_score": 85,
  "technical_score": 88,
  
  // Metadata
  "notes": "Strong candidate, excellent communication",
  "tags": ["python", "senior", "remote"],
  "created_at": ISODate("2026-03-07T10:00:00Z"),
  "updated_at": ISODate("2026-03-07T15:30:00Z"),
  
  // References
  "interview_ids": [ObjectId("..."), ObjectId("...")]
}
```

### Interviews Collection

```javascript
{
  "_id": ObjectId("..."),
  "candidate_email": "sarah@example.com",  // Index
  "type": "technical",  // technical, behavioral, cultural, final
  "scheduled_at": ISODate("2026-03-09T10:00:00Z"),  // Index
  "duration": 60,
  "meeting_link": "https://meet.google.com/...",
  "calendar_event_id": "evt_123",
  "status": "scheduled",  // scheduled, completed, cancelled, no_show
  "interviewer": "John Smith",
  "interviewer_email": "john@company.com",
  "notes": "Focus on system design",
  "feedback": "Excellent problem-solving skills",
  "score": 9,
  "created_at": ISODate("2026-03-07T10:00:00Z"),
  "updated_at": ISODate("2026-03-07T10:00:00Z")
}
```

### Jobs Collection

```javascript
{
  "_id": ObjectId("..."),
  "title": "Senior Software Engineer",
  "department": "Engineering",
  "location": "Remote",
  "type": "full-time",  // full-time, part-time, contract
  "experience_level": "senior",  // entry, mid, senior, lead
  "salary_min": 130000,
  "salary_max": 180000,
  "description": "We are looking for...",
  "requirements": ["5+ years Python", "System design experience"],
  "skills": ["Python", "AWS", "Docker"],
  "status": "open",  // open, closed, on_hold
  "posted_at": ISODate("2026-03-01T00:00:00Z"),
  "created_at": ISODate("2026-03-01T00:00:00Z"),
  "updated_at": ISODate("2026-03-01T00:00:00Z")
}
```

---

## 🔍 Indexes Created

The system automatically creates these indexes for performance:

### Candidates
- `email` (unique)
- `status`
- `screening_score`
- `culture_fit_score`
- `name` (ascending)
- `created_at` (descending)

### Interviews
- `candidate_email`
- `scheduled_at`
- `status`

### Jobs
- `title`
- `status`

---

## 🧪 Testing MongoDB Connection

### Test Script

Create `test_mongodb.py`:

```python
from utils.mongodb_database import MongoDBDatabase

# Test connection
db = MongoDBDatabase()

if db.is_connected():
    print("✅ MongoDB connected!")
    
    # Add test candidate
    candidate_id = db.add_candidate({
        "name": "Test Candidate",
        "email": "test@example.com",
        "college": "Test University",
        "cpi": 8.5,
        "skills": ["Python", "Testing"]
    })
    
    print(f"✅ Candidate added: {candidate_id}")
    
    # Retrieve candidate
    candidate = db.get_candidate("test@example.com")
    print(f"✅ Candidate retrieved: {candidate['name']}")
    
    # Get stats
    stats = db.get_pipeline_stats()
    print(f"✅ Pipeline stats: {stats}")
    
    # Cleanup
    db.delete_candidate("test@example.com")
    print("✅ Test candidate deleted")
    
else:
    print("❌ MongoDB not connected")
```

Run:
```bash
python test_mongodb.py
```

---

## 🚀 Running with MongoDB

### Local Development

```bash
# Start MongoDB
sudo systemctl start mongod

# Set environment
export MONGODB_URI="mongodb://localhost:27017/"
export MONGODB_DATABASE="hr_agent"
export USE_MONGODB="true"
export OPENAI_API_KEY="sk-proj-..."

# Run agent
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e MONGODB_URI=$MONGODB_URI \
  -e MONGODB_DATABASE=$MONGODB_DATABASE \
  -e USE_MONGODB=$USE_MONGODB \
  hr-agent
```

### With Docker Compose

```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-proj-...
MONGODB_URI=mongodb://admin:admin123@mongodb:27017/
MONGODB_DATABASE=hr_agent
USE_MONGODB=true
EOF

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f hr-agent
```

### With MongoDB Atlas

```bash
export MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
export MONGODB_DATABASE="hr_agent"
export USE_MONGODB="true"
export OPENAI_API_KEY="sk-proj-..."

docker run -p 5000:5000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e MONGODB_URI=$MONGODB_URI \
  -e MONGODB_DATABASE=$MONGODB_DATABASE \
  -e USE_MONGODB=$USE_MONGODB \
  hr-agent
```

---

## 📊 MongoDB Compass (GUI)

### Install MongoDB Compass

Download from: https://www.mongodb.com/try/download/compass

### Connect

1. Open MongoDB Compass
2. Enter connection string:
   - Local: `mongodb://localhost:27017/`
   - Atlas: `mongodb+srv://user:pass@cluster.mongodb.net/`
3. Click "Connect"
4. Browse databases and collections
5. Run queries visually

---

## 🔧 Useful MongoDB Commands

### MongoDB Shell (mongosh)

```bash
# Connect
mongosh

# Or connect to specific database
mongosh "mongodb://localhost:27017/hr_agent"

# Show databases
show dbs

# Use database
use hr_agent

# Show collections
show collections

# Count candidates
db.candidates.countDocuments()

# Find all candidates
db.candidates.find().pretty()

# Find by email
db.candidates.findOne({email: "sarah@example.com"})

# Find candidates with high scores
db.candidates.find({screening_score: {$gte: 85}})

# Update candidate
db.candidates.updateOne(
  {email: "sarah@example.com"},
  {$set: {status: "hired"}}
)

# Delete candidate
db.candidates.deleteOne({email: "test@example.com"})

# Get pipeline stats
db.candidates.aggregate([
  {$group: {_id: "$status", count: {$sum: 1}}}
])

# Drop collection (careful!)
db.candidates.drop()

# Drop database (very careful!)
db.dropDatabase()
```

---

## 🔒 Security Best Practices

### 1. Authentication

```bash
# Create admin user
mongosh
use admin
db.createUser({
  user: "admin",
  pwd: "strong_password",
  roles: ["root"]
})

# Create app user
use hr_agent
db.createUser({
  user: "hr_agent_app",
  pwd: "app_password",
  roles: [{role: "readWrite", db: "hr_agent"}]
})
```

### 2. Connection String with Auth

```bash
export MONGODB_URI="mongodb://hr_agent_app:app_password@localhost:27017/hr_agent?authSource=hr_agent"
```

### 3. Network Security

- Use firewall to restrict MongoDB port (27017)
- For production, use VPN or private network
- MongoDB Atlas handles this automatically

### 4. Encryption

- Enable encryption at rest (Atlas does this)
- Use TLS/SSL for connections
- Never commit credentials to git

---

## 📈 Monitoring

### Check Database Size

```javascript
db.stats()
```

### Check Collection Stats

```javascript
db.candidates.stats()
```

### Monitor Queries

```javascript
db.setProfilingLevel(2)  // Log all queries
db.system.profile.find().pretty()
```

---

## 🆘 Troubleshooting

### Connection Refused

```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Check port
sudo netstat -tulpn | grep 27017

# Check logs
sudo tail -f /var/log/mongodb/mongod.log
```

### Authentication Failed

```bash
# Verify credentials
mongosh "mongodb://user:pass@localhost:27017/hr_agent"

# Check user exists
use hr_agent
db.getUsers()
```

### Slow Queries

```bash
# Check indexes
db.candidates.getIndexes()

# Explain query
db.candidates.find({email: "test@example.com"}).explain("executionStats")
```

---

## ✅ Verification Checklist

- [ ] MongoDB installed and running
- [ ] Python driver installed (`pip install pymongo`)
- [ ] Environment variables set
- [ ] Connection successful
- [ ] Indexes created
- [ ] Test candidate added and retrieved
- [ ] Agent starts without errors
- [ ] Logs show "✅ Connected to MongoDB"

---

## 🎉 You're Ready!

Your HR agent now has a production-grade MongoDB database!

**Next steps:**
1. Test with real candidate data
2. Monitor performance
3. Set up backups (Atlas does this automatically)
4. Scale as needed

---

**Need help?** Check the logs or MongoDB documentation: https://docs.mongodb.com/
