import random
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "aidevo")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# Interest categories
INTERESTS = [
    "Charity & Volunteering",
    "Clubs & Societies",
    "Sports & Athletics",
    "Cultural Activities",
    "Technical & Coding",
    "Research & Innovation",
    "Entrepreneurship",
    "Arts & Creativity",
    "Leadership & Development",
    "Community Service",
    "Environmental Causes",
    "Education & Tutoring",
    "Professional Development",
    "Social Events",
    "Fundraising"
]

EVENT_CATEGORIES = [
    "Workshop",
    "Seminar",
    "Tournament",
    "Conference",
    "Social",
    "Charity",
    "Competition",
    "Networking",
    "Training",
    "Meetup"
]

DEPARTMENTS = [
    "Computer Science and Engineering",
    "Electrical and Electronic Engineering",
    "Industrial and Production Engineering",
    "Chemical Engineering",
    "Biomedical Engineering",
    "Management",
    "Physics",
    "Chemistry",
    "Mathematics",
    "English"
]

ORG_TYPES = [
    "Club", "Social Service", "Association"
]

def generate_interaction_history():
    """Generate interaction history for a user."""
    interaction_types = ["viewed", "attended", "registered", "shared"]
    interactions = []
    
    for _ in range(random.randint(3, 15)):
        interactions.append({
            "type": random.choice(interaction_types),
            "weight": {
                "viewed": 0.1,
                "registered": 0.3,
                "attended": 1.0,
                "shared": 0.2
            }[random.choice(interaction_types)]
        })
    
    return interactions

def generate_sample_students(count=50):
    """Generate sample student documents."""
    students = []
    sessions = ["2023-2024", "2024-2025", "2025-2026"]
    
    for i in range(count):
        student = {
            "uid": f"student_{i}",
            "email": f"{200142+i}.cse@student.just.edu.bd",
            "name": f"Student {i}",
            "role": "student",
            "photoURL": f"https://ui-avatars.com/api/?name=Student+{i}",
            "createdAt": datetime.utcnow() - timedelta(days=random.randint(30, 365)),
            "student": {
                "studentId": f"{200142+i}",
                "department": random.choice(DEPARTMENTS),
                "session": random.choice(sessions),
                "interests": random.sample(INTERESTS, random.randint(3, 6)),
                "year": random.randint(2, 4),
                "status": "active",
                "verified": True
            }
        }
        students.append(student)
    
    return students

def generate_sample_organizations(count=15):
    """Generate sample organization documents."""
    organizations = []
    campuses = ["Main Campus", "North Campus", "South Campus"]
    
    for i in range(count):
        org = {
            "uid": f"org_{i}",
            "email": f"org{i}@aidevo.com",
            "name": f"Organization {i}",
            "role": "organization",
            "photoURL": f"https://ui-avatars.com/api/?name=Org+{i}",
            "createdAt": datetime.utcnow() - timedelta(days=random.randint(30, 400)),
            "organization": {
                "name": f"Organization {i}",
                "type": random.choice(ORG_TYPES),
                "roleType": f"Role Type {i}",
                "tagline": f"Tagline for organization {i}",
                "founded": datetime.utcnow() - timedelta(days=random.randint(365, 1460)),
                "website": f"https://org{i}.example.com",
                "phone": f"+880{random.randint(1000000000, 9999999999)}",
                "campus": random.choice(campuses),
                "mission": f"Mission statement for organization {i}",
                "membershipCount": random.randint(10, 200),
                "status": "active",
                "verified": True
            }
        }
        organizations.append(org)
    
    return organizations

def generate_sample_events(org_count=15, events_per_org=5):
    """Generate sample event documents."""
    events = []
    event_id = 1
    
    for org_idx in range(org_count):
        for _ in range(events_per_org):
            start_date = datetime.utcnow() + timedelta(days=random.randint(1, 60))
            event = {
                "title": f"Event {event_id}",
                "description": f"Description for event {event_id}. This is a great event with amazing opportunities.",
                "category": random.choice(EVENT_CATEGORIES),
                "tags": random.sample(INTERESTS, random.randint(2, 5)),
                "organizationId": f"org_{org_idx}",
                "createdAt": datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                "startDate": start_date,
                "endDate": start_date + timedelta(hours=random.randint(1, 8)),
                "location": f"Venue {random.randint(1, 10)}",
                "capacity": random.randint(20, 300),
                "attendees": [],
                "registeredUsers": [],
                "viewedUsers": [],
                "status": "active",
                "avgRating": round(random.uniform(3.5, 5.0), 1),
                "ratingCount": random.randint(5, 50)
            }
            events.append(event)
            event_id += 1
    
    return events

def generate_user_interactions(students, events):
    """Generate user interactions with events."""
    for student in students:
        # Each student interacts with 5-20 events
        num_interactions = random.randint(5, min(20, len(events)))
        sampled_events = random.sample(events, num_interactions)
        
        for event in sampled_events:
            interaction_type = random.choices(
                ["viewed", "registered", "attended"],
                weights=[0.4, 0.3, 0.3],
                k=1
            )[0]
            
            if interaction_type == "viewed":
                if event["_id"] not in [s for s in event.get("viewedUsers", [])]:
                    event.setdefault("viewedUsers", []).append(student["uid"])
            
            elif interaction_type == "registered":
                if event["_id"] not in [s for s in event.get("registeredUsers", [])]:
                    event.setdefault("registeredUsers", []).append(student["uid"])
                # 70% of registered might attend
                if random.random() < 0.7:
                    if event["_id"] not in [s for s in event.get("attendees", [])]:
                        event.setdefault("attendees", []).append(student["uid"])
            
            elif interaction_type == "attended":
                if event["_id"] not in [s for s in event.get("attendees", [])]:
                    event.setdefault("attendees", []).append(student["uid"])

def generate_dataset():
    """Generate complete dataset and insert into MongoDB."""
    print("=" * 60)
    print("Aidevo Recommendation Dataset Generator")
    print("=" * 60)
    
    # Drop existing collections if they exist
    print("\n[1/5] Cleaning up existing collections...")
    for collection in ["users", "events", "recommendation_logs"]:
        db[collection].drop()
    print("✓ Collections cleaned")
    
    # Generate students
    print("\n[2/5] Generating 50 sample students...")
    students = generate_sample_students(50)
    db.users.insert_many(students)
    print(f"✓ Inserted {len(students)} students")
    
    # Generate organizations
    print("\n[3/5] Generating 15 sample organizations...")
    organizations = generate_sample_organizations(15)
    db.users.insert_many(organizations)
    print(f"✓ Inserted {len(organizations)} organizations")
    
    # Generate events
    print("\n[4/5] Generating 75 sample events (5 per organization)...")
    events = generate_sample_events(org_count=15, events_per_org=5)
    db.events.insert_many(events)
    print(f"✓ Inserted {len(events)} events")
    
    # Generate interactions
    print("\n[5/5] Generating user-event interactions...")
    events_with_ids = list(db.events.find())
    generate_user_interactions(students, events_with_ids)
    
    # Update events with interactions
    for event in events_with_ids:
        db.events.update_one(
            {"_id": event["_id"]},
            {"$set": {
                "attendees": event.get("attendees", []),
                "registeredUsers": event.get("registeredUsers", []),
                "viewedUsers": event.get("viewedUsers", [])
            }}
        )
    print(f"✓ Generated interactions for {len(students)} students")
    
    # Print statistics
    print("\n" + "=" * 60)
    print("Dataset Summary")
    print("=" * 60)
    print(f"Total Students: {db.users.count_documents({'role': 'student'})}")
    print(f"Total Organizations: {db.users.count_documents({'role': 'organization'})}")
    print(f"Total Events: {db.events.count_documents({})}")
    
    # Event statistics
    total_attendees = sum(len(e.get("attendees", [])) for e in events_with_ids)
    total_registrations = sum(len(e.get("registeredUsers", [])) for e in events_with_ids)
    total_views = sum(len(e.get("viewedUsers", [])) for e in events_with_ids)
    
    print(f"Total Event Attendances: {total_attendees}")
    print(f"Total Event Registrations: {total_registrations}")
    print(f"Total Event Views: {total_views}")
    print("=" * 60)
    print("\n✓ Dataset generation completed successfully!")
    print("\nYou can now run: python scripts/train_model.py")

if __name__ == "__main__":
    try:
        generate_dataset()
    except Exception as e:
        print(f"Error generating dataset: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()
