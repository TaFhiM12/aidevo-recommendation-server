import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings from environment variables."""
    
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "aidevo")
    PORT: int = int(os.getenv("PORT", 5000))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    NODE_ENV: str = os.getenv("NODE_ENV", "development")
    DEBUG: bool = NODE_ENV == "development"
    
    # Model paths
    RECOMMENDATION_MODEL_PATH: str = os.getenv("RECOMMENDATION_MODEL_PATH", "./models/recommendation_model.pkl")
    SCALER_PATH: str = os.getenv("SCALER_PATH", "./models/scaler.pkl")
    TFIDF_PATH: str = os.getenv("TFIDF_PATH", "./models/tfidf_vectorizer.pkl")
    
    # Recommendation parameters
    NUM_RECOMMENDATIONS: int = 5
    MIN_SIMILARITY_SCORE: float = 0.3

settings = Settings()
