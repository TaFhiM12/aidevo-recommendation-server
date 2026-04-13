from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
from app.database import db
from app.recommendation import recommendation_engine
from app.config import settings
from app.models import RecommendationRequest, RecommendationResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown."""
    # Startup
    logger.info("Starting Aidevo Recommendation Service...")
    db.connect()
    recommendation_engine.load_models()
    logger.info("Services initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Recommendation Service...")
    db.disconnect()

# Create FastAPI app
app = FastAPI(
    title="Aidevo Recommendation Service",
    description="AI-powered event recommendation microservice",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Aidevo Recommendation Service",
        "timestamp": datetime.utcnow().isoformat()
    }

# Recommendation endpoint
@app.post("/api/recommendations")
async def get_recommendations(request: RecommendationRequest):
    """Get personalized event recommendations for a user.
    
    Args:
        request: RecommendationRequest containing user_id and preferences
    
    Returns:
        RecommendationResponse with recommended events
    """
    try:
        # Fetch user profile from MongoDB
        users_collection = db.get_collection("users")
        user_doc = users_collection.find_one({"uid": request.user_id})
        
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Build user profile
        user_profile = {
            "interests": user_doc.get("student", {}).get("interests", []) if user_doc.get("role") == "student" else [],
            "role": user_doc.get("role"),
            "department": user_doc.get("student", {}).get("department") if user_doc.get("role") == "student" else None,
        }
        
        # Fetch user event history
        events_collection = db.get_collection("events")
        user_events = list(events_collection.find({
            "$or": [
                {"attendees": request.user_id},
                {"registeredUsers": request.user_id},
                {"viewedUsers": request.user_id}
            ]
        }, {"_id": 1}))
        
        user_history = {
            "attended_events": [str(e["_id"]) for e in user_events if request.user_id in e.get("attendees", [])],
            "registered_events": [str(e["_id"]) for e in user_events if request.user_id in e.get("registeredUsers", [])],
            "viewed_events": [str(e["_id"]) for e in user_events if request.user_id in e.get("viewedUsers", [])],
            "favorite_categories": _get_favorite_categories(user_events),
            "followed_organizations": [],
            "participation_rate": len(user_events) / max(1, 10),
        }
        
        # Fetch all available events
        all_events = list(events_collection.find(
            {"status": "active"},
            {"_id": 1, "title": 1, "description": 1, "category": 1, "tags": 1, "organizationId": 1, "createdAt": 1, "attendees": 1, "avgRating": 1}
        ))
        
        # Format events for recommendation
        formatted_events = [
            {
                "event_id": str(e["_id"]),
                "title": e.get("title"),
                "description": e.get("description"),
                "category": e.get("category"),
                "tags": e.get("tags", []),
                "organization_id": str(e.get("organizationId")),
                "days_since_created": (datetime.utcnow() - e.get("createdAt", datetime.utcnow())).days,
                "participant_count": len(e.get("attendees", [])),
                "average_rating": e.get("avgRating", 0)
            }
            for e in all_events
        ]
        
        # Get recommendations
        recommendations = recommendation_engine.recommend_events(
            user_profile=user_profile,
            user_history=user_history,
            available_events=formatted_events,
            num_recommendations=request.num_recommendations or settings.NUM_RECOMMENDATIONS,
            filter_category=request.filter_category
        )
        
        # Log recommendation (async)
        _log_recommendation(request.user_id, recommendations)
        
        return RecommendationResponse(
            user_id=request.user_id,
            recommendations=recommendations,
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating recommendations")

# Batch recommendations endpoint
@app.post("/api/batch-recommendations")
async def batch_recommendations(user_ids: list[str], background_tasks: BackgroundTasks):
    """Generate recommendations for multiple users."""
    try:
        results = {}
        for user_id in user_ids:
            request = RecommendationRequest(user_id=user_id, email="batch@batch.com")
            rec = await get_recommendations(request)
            results[user_id] = {
                "count": len(rec.recommendations),
                "top_recommendation": rec.recommendations[0] if rec.recommendations else None
            }
        
        return {"status": "success", "results": results}
    
    except Exception as e:
        logger.error(f"Error in batch recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Error in batch recommendations")

# Utility functions
def _get_favorite_categories(events: list) -> list:
    """Extract favorite categories from event history."""
    categories = {}
    for event in events:
        cat = event.get("category")
        if cat:
            categories[cat] = categories.get(cat, 0) + 1
    return sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3] if categories else []

def _log_recommendation(user_id: str, recommendations: list):
    """Log recommendation for analytics."""
    try:
        logs_collection = db.get_collection("recommendation_logs")
        logs_collection.insert_one({
            "user_id": user_id,
            "recommendations": [r.get("event_id") for r in recommendations],
            "timestamp": datetime.utcnow(),
            "count": len(recommendations)
        })
    except Exception as e:
        logger.error(f"Error logging recommendation: {e}")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the Aidevo Recommendation Service!"}

# Info endpoint
@app.get("/api/info")
async def service_info():
    """Get service information."""
    return {
        "service": "Aidevo Recommendation Service",
        "version": "1.0.0",
        "algorithm": "Hybrid (Content-based + Collaborative Filtering + Engagement)",
        "features": [
            "Content-based filtering using interests and tags",
            "Collaborative filtering using user behavior",
            "Engagement-based ranking",
            "Real-time recommendations",
            "Category and organization filtering"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
