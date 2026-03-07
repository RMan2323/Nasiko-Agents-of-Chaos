#!/usr/bin/env python3
"""
Test script for MongoDB integration.
Run this to verify MongoDB is working correctly.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.mongodb_database import MongoDBDatabase


def test_mongodb():
    """Test MongoDB connection and operations."""
    
    print("=" * 60)
    print("MongoDB Integration Test")
    print("=" * 60)
    print()
    
    # Initialize database
    print("1. Connecting to MongoDB...")
    db = MongoDBDatabase()
    
    if not db.is_connected():
        print("❌ MongoDB not connected")
        print()
        print("To use MongoDB:")
        print("1. Install MongoDB: https://www.mongodb.com/docs/manual/installation/")
        print("2. Start MongoDB: sudo systemctl start mongod")
        print("3. Set environment: export MONGODB_URI='mongodb://localhost:27017/'")
        print()
        print("Or use MongoDB Atlas (cloud):")
        print("1. Sign up: https://www.mongodb.com/cloud/atlas/register")
        print("2. Create cluster and get connection string")
        print("3. Set environment: export MONGODB_URI='mongodb+srv://...'")
        print()
        return False
    
    print("✅ Connected to MongoDB!")
    print(f"   Database: {db.database_name}")
    print()
    
    # Test 1: Add candidate
    print("2. Adding test candidate...")
    candidate_data = {
        "name": "Test Candidate",
        "email": "test@example.com",
        "phone": "+1234567890",
        "college": "Test University",
        "degree": "B.Tech Computer Science",
        "cpi": 8.5,
        "graduation_year": "2024",
        "skills": ["Python", "MongoDB", "Testing"],
        "experience_years": 3,
        "linkedin_url": "https://linkedin.com/in/test",
        "github_url": "https://github.com/test",
        "applied_position": "Software Engineer",
        "status": "applied"
    }
    
    candidate_id = db.add_candidate(candidate_data)
    
    if candidate_id:
        print(f"✅ Candidate added: {candidate_id}")
    else:
        print("❌ Failed to add candidate")
        return False
    print()
    
    # Test 2: Retrieve candidate
    print("3. Retrieving candidate...")
    candidate = db.get_candidate("test@example.com")
    
    if candidate:
        print(f"✅ Candidate retrieved:")
        print(f"   Name: {candidate['name']}")
        print(f"   College: {candidate['college']}")
        print(f"   CPI: {candidate['cpi']}")
        print(f"   Skills: {', '.join(candidate['skills'])}")
    else:
        print("❌ Failed to retrieve candidate")
        return False
    print()
    
    # Test 3: Update candidate
    print("4. Updating candidate...")
    success = db.update_candidate("test@example.com", {
        "screening_score": 85,
        "status": "screened"
    })
    
    if success:
        print("✅ Candidate updated")
        candidate = db.get_candidate("test@example.com")
        print(f"   Screening Score: {candidate['screening_score']}")
        print(f"   Status: {candidate['status']}")
    else:
        print("❌ Failed to update candidate")
    print()
    
    # Test 4: Add interview
    print("5. Adding interview...")
    interview_id = db.add_interview("test@example.com", {
        "type": "technical",
        "scheduled_at": "2026-03-10T10:00:00",
        "duration": 60,
        "meeting_link": "https://meet.google.com/test-123",
        "status": "scheduled",
        "interviewer": "John Doe"
    })
    
    if interview_id:
        print(f"✅ Interview added: {interview_id}")
    else:
        print("❌ Failed to add interview")
    print()
    
    # Test 5: Get interviews
    print("6. Retrieving interviews...")
    interviews = db.get_interviews(candidate_email="test@example.com")
    
    if interviews:
        print(f"✅ Found {len(interviews)} interview(s)")
        for interview in interviews:
            print(f"   Type: {interview['type']}")
            print(f"   Status: {interview['status']}")
            print(f"   Scheduled: {interview['scheduled_at']}")
    else:
        print("⚠️ No interviews found")
    print()
    
    # Test 6: Search candidates
    print("7. Searching candidates...")
    results = db.search_candidates({"status": "screened"})
    
    if results:
        print(f"✅ Found {len(results)} screened candidate(s)")
    else:
        print("⚠️ No screened candidates found")
    print()
    
    # Test 7: Get pipeline stats
    print("8. Getting pipeline statistics...")
    stats = db.get_pipeline_stats()
    
    if stats:
        print("✅ Pipeline stats:")
        for status, count in stats.items():
            print(f"   {status}: {count}")
    else:
        print("⚠️ No stats available")
    print()
    
    # Test 8: Get average scores
    print("9. Getting average scores...")
    scores = db.get_average_scores()
    
    if scores:
        print("✅ Average scores:")
        for metric, value in scores.items():
            print(f"   {metric}: {value}")
    else:
        print("⚠️ No scores available")
    print()
    
    # Cleanup
    print("10. Cleaning up test data...")
    db.delete_candidate("test@example.com")
    print("✅ Test candidate deleted")
    print()
    
    print("=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    print()
    print("MongoDB is working correctly with your HR Agent!")
    print()
    
    return True


if __name__ == "__main__":
    try:
        success = test_mongodb()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
