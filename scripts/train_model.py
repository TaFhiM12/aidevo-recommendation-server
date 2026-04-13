import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from pymongo import MongoClient
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "aidevo")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

def train_models():
    """Train recommendation models."""
    print("=" * 60)
    print("Aidevo Recommendation Model Training")
    print("=" * 60)
    
    # Create models directory
    os.makedirs("./models", exist_ok=True)
    
    # Fetch events data
    print("\n[1/3] Fetching event data from MongoDB...")
    events = list(db.events.find())
    print(f"✓ Loaded {len(events)} events")
    
    if len(events) == 0:
        print("\n✗ No events found. Please run: python scripts/generate_dataset.py")
        return
    
    # Prepare event descriptions for TF-IDF
    print("\n[2/3] Training TF-IDF vectorizer on event descriptions...")
    descriptions = [
        f"{e.get('title', '')} {e.get('description', '')} {' '.join(e.get('tags', []))}"
        for e in events
    ]
    
    tfidf_vectorizer = TfidfVectorizer(
        max_features=100,
        stop_words='english',
        ngram_range=(1, 2)
    )
    tfidf_vectorizer.fit(descriptions)
    
    # Save vectorizer
    joblib.dump(tfidf_vectorizer, "./models/tfidf_vectorizer.pkl")
    print(f"✓ TF-IDF vectorizer trained with {len(tfidf_vectorizer.get_feature_names_out())} features")
    
    # Train scaler for numerical features
    print("\n[3/3] Training StandardScaler for numerical features...")
    
    numerical_features = []
    for event in events:
        features = [
            len(event.get('attendees', [])),
            len(event.get('registeredUsers', [])),
            len(event.get('viewedUsers', [])),
            event.get('avgRating', 3.5),
            event.get('ratingCount', 0)
        ]
        numerical_features.append(features)
    
    scaler = StandardScaler()
    scaler.fit(numerical_features)
    
    # Save scaler
    joblib.dump(scaler, "./models/scaler.pkl")
    print(f"✓ StandardScaler trained")
    
    # Save a placeholder model file
    joblib.dump({"vectorizer": tfidf_vectorizer, "scaler": scaler}, "./models/recommendation_model.pkl")
    print(f"✓ Models saved to ./models/")
    
    # Print statistics
    print("\n" + "=" * 60)
    print("Training Statistics")
    print("=" * 60)
    print(f"Events processed: {len(events)}")
    print(f"TF-IDF features: {len(tfidf_vectorizer.get_feature_names_out())}")
    print(f"Average attendees per event: {sum(len(e.get('attendees', [])) for e in events) / len(events):.1f}")
    print(f"Average event rating: {sum(e.get('avgRating', 3.5) for e in events) / len(events):.2f}")
    print("=" * 60)
    print("\n✓ Model training completed successfully!")
    print("\nYou can now run: python -m app.main")

if __name__ == "__main__":
    try:
        train_models()
    except Exception as e:
        print(f"Error during training: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()
