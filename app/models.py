from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserProfile(BaseModel):
    """User profile data for recommendations."""
    user_id: str
    email: str
    role: str  # student or organization
    interests: Optional[List[str]] = []
    department: Optional[str] = None  # For students
    session: Optional[str] = None  # For students
    organization_type: Optional[str] = None  # For organizations
    

class EventData(BaseModel):
    """Event data for recommendations."""
    event_id: str
    title: str
    description: str
    category: str
    tags: List[str]
    organization_id: str
    created_at: datetime
    participant_count: int


class UserEventInteraction(BaseModel):
    """User interaction with events."""
    user_id: str
    event_id: str
    interaction_type: str  # viewed, attended, registered, shared, etc.
    interaction_score: float  # 0-1 scale
    timestamp: datetime


class RecommendationRequest(BaseModel):
    """Request for event recommendations."""
    user_id: str
    email: str
    num_recommendations: Optional[int] = 5
    filter_category: Optional[str] = None
    filter_organization_id: Optional[str] = None


class RecommendationResponse(BaseModel):
    """Response with recommended events."""
    user_id: str
    recommendations: List[dict]
    timestamp: datetime


class UserEventHistory(BaseModel):
    """User's complete event history."""
    user_id: str
    attended_events: List[str]
    registered_events: List[str]
    viewed_events: List[str]
    interests: List[str]
