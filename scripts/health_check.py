from pymongo import MongoClient
from app.config import settings

# MongoDB connection for testing
def test_mongodb_connection():
    """Test MongoDB connection."""
    try:
        client = MongoClient(settings.MONGODB_URI)
        client.admin.command('ping')
        print("✓ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False

def test_collections_exist():
    """Verify required collections exist."""
    try:
        client = MongoClient(settings.MONGODB_URI)
        db = client[settings.DB_NAME]
        
        required_collections = ['users', 'events']
        existing = db.list_collection_names()
        
        missing = [c for c in required_collections if c not in existing]
        
        if missing:
            print(f"✗ Missing collections: {missing}")
            return False
        
        print(f"✓ All required collections exist: {required_collections}")
        return True
    except Exception as e:
        print(f"✗ Error checking collections: {e}")
        return False

def test_data_volume():
    """Check data volume in collections."""
    try:
        client = MongoClient(settings.MONGODB_URI)
        db = client[settings.DB_NAME]
        
        users_count = db.users.count_documents({})
        events_count = db.events.count_documents({})
        
        print(f"✓ Users: {users_count}")
        print(f"✓ Events: {events_count}")
        
        if users_count == 0 or events_count == 0:
            print("⚠ Warning: Low data volume. Run: python scripts/generate_dataset.py")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error checking data: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Recommendation Service Health Check")
    print("=" * 50)
    
    checks = [
        ("MongoDB Connection", test_mongodb_connection),
        ("Collections", test_collections_exist),
        ("Data Volume", test_data_volume)
    ]
    
    results = []
    for name, test_func in checks:
        print(f"\n[{name}]")
        results.append(test_func())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ All checks passed! Service is ready.")
    else:
        print("✗ Some checks failed. See above for details.")
    print("=" * 50)
