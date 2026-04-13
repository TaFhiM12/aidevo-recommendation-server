# Advanced Configuration & Customization

Customize the recommendation algorithm and behavior for your use case.

## Configuration Parameters

### app/config.py

```python
NUM_RECOMMENDATIONS: int = 5              # Default recommendations to return
MIN_SIMILARITY_SCORE: float = 0.3         # Minimum score threshold (0-1)
```

Modify these in `app/config.py`:

```python
class Settings:
    NUM_RECOMMENDATIONS: int = 10           # Return more recommendations
    MIN_SIMILARITY_SCORE: float = 0.5      # Higher threshold = fewer but better results
```

---

## Algorithm Customization

### Adjusting Feature Weights

The hybrid algorithm uses weighted components. Edit `app/recommendation.py` in the `recommend_events()` method:

```python
# Default weights
final_score = (
    content_score * 0.4 +       # Content-based: 40%
    collab_score * 0.35 +       # Collaborative: 35%
    engagement_score * 0.25     # Engagement: 25%
)
```

**Example: Boost content-based for new users**

```python
# For users with few interactions
is_new_user = len(user_history.get('attended_events', [])) < 3

if is_new_user:
    final_score = (
        content_score * 0.6 +       # Higher weight: 60%
        collab_score * 0.2 +        # Lower weight: 20%
        engagement_score * 0.2      # Lower weight: 20%
    )
else:
    final_score = (
        content_score * 0.4 +
        collab_score * 0.35 +
        engagement_score * 0.25
    )
```

---

## Custom Scoring Functions

### Add Department-Based Scoring

```python
def department_affinity(user_profile: Dict, event_metadata: Dict) -> float:
    """Score based on department match."""
    score = 0.0
    
    user_dept = user_profile.get('department', '')
    event_depts = event_metadata.get('departments', [])
    
    if user_dept in event_depts:
        score += 0.2
    
    return min(score, 1.0)
```

Use in recommendation:
```python
dept_score = department_affinity(user_profile, event)
final_score = (
    content_score * 0.35 +
    collab_score * 0.35 +
    engagement_score * 0.25 +
    dept_score * 0.05
)
```

### Add Time-Based Scoring

```python
def event_timing_score(event_metadata: Dict) -> float:
    """Boost upcoming events."""
    from datetime import datetime, timedelta
    
    event_date = event_metadata.get('startDate')
    now = datetime.utcnow()
    
    if event_date:
        days_until = (event_date - now).days
        
        # Boost events in next 3-7 days
        if 3 <= days_until <= 7:
            return 0.15
        # Slight boost for events within a week
        elif days_until <= 3:
            return 0.1
    
    return 0.0
```

---

## Database Optimization

### Add Indexes

```bash
# In MongoDB shell
db.users.createIndex({ "uid": 1 })
db.users.createIndex({ "email": 1 })
db.events.createIndex({ "organizationId": 1 })
db.events.createIndex({ "status": 1, "category": 1 })
db.events.createIndex({ "tags": 1 })
```

### Python Implementation

```python
def create_indexes(db):
    """Create database indexes for performance."""
    users_coll = db['users']
    events_coll = db['events']
    
    users_coll.create_index('uid')
    users_coll.create_index('email')
    
    events_coll.create_index('organizationId')
    events_coll.create_index([('status', 1), ('category', 1)])
    events_coll.create_index('tags')
```

Add to app initialization in `app/main.py`:

```python
@app.on_event("startup")
async def startup():
    db_instance = db.get_database()
    create_indexes(db_instance)
```

---

## Performance Tuning

### Cache Recommendations

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedRecommendationEngine:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = timedelta(hours=24)
    
    def get_cached_recommendations(self, user_id: str):
        """Get recommendations from cache if available."""
        if user_id in self.cache:
            cached_data, timestamp = self.cache[user_id]
            if datetime.utcnow() - timestamp < self.cache_ttl:
                return cached_data
        
        return None
    
    def cache_recommendations(self, user_id: str, recommendations: list):
        """Cache recommendations for future requests."""
        self.cache[user_id] = (recommendations, datetime.utcnow())
```

### Limit Active Events

```python
@app.post("/api/recommendations")
async def get_recommendations(request: RecommendationRequest):
    # Only consider recent events
    recent_date = datetime.utcnow() - timedelta(days=90)
    
    all_events = list(events_collection.find({
        "status": "active",
        "createdAt": {"$gte": recent_date}  # Last 90 days
    }))
    
    # ... rest of implementation
```

---

## Adding New Data Sources

### Integrate User Feedback

```python
def feedback_score(user_id: str, event_id: str, db) -> float:
    """Score based on explicit user feedback."""
    feedback_coll = db['feedback']
    
    feedback = feedback_coll.find_one({
        'user_id': user_id,
        'event_id': event_id
    })
    
    if feedback:
        rating = feedback.get('rating', 0)  # 1-5 scale
        return rating / 5.0  # Normalize to 0-1
    
    return 0.0
```

### Integrate Social Signals

```python
def social_score(user_id: str, event_metadata: Dict, db) -> float:
    """Score based on friend attendance."""
    friends_attending = db.events.count_documents({
        '_id': event_metadata['event_id'],
        'attendees': {'$in': get_user_friends(user_id, db)}
    })
    
    if friends_attending > 0:
        return min(friends_attending * 0.1, 0.3)  # Max 0.3 boost
    
    return 0.0
```

---

## Monitoring & Analytics

### Log Recommendation Metrics

```python
def log_metrics(user_id: str, recommendations: list, db):
    """Log recommendation metrics for analysis."""
    metrics = {
        'user_id': user_id,
        'timestamp': datetime.utcnow(),
        'recommendation_count': len(recommendations),
        'average_score': sum(r['score'] for r in recommendations) / len(recommendations) if recommendations else 0,
        'categories': [r['category'] for r in recommendations],
        'tags': [tag for r in recommendations for tag in r.get('tags', [])]
    }
    
    db['recommendation_metrics'].insert_one(metrics)
```

### Track Conversion Rates

```python
def track_conversion(user_id: str, event_id: str, action: str, db):
    """Track if user acts on recommendation."""
    db['conversions'].insert_one({
        'user_id': user_id,
        'event_id': event_id,
        'action': action,  # 'viewed', 'registered', 'attended'
        'timestamp': datetime.utcnow()
    })
```

---

## Testing Custom Changes

```python
# test_custom_algorithm.py

def test_custom_scoring():
    from app.recommendation import recommendation_engine
    
    user_profile = {
        'interests': ['Technical & Coding', 'Leadership'],
        'role': 'student',
        'department': 'CSE'
    }
    
    user_history = {
        'attended_events': [],
        'registered_events': [],
        'favorite_categories': [],
        'participation_rate': 0
    }
    
    test_events = [
        {
            'event_id': 'event_1',
            'title': 'Python Workshop',
            'category': 'Workshop',
            'tags': ['Technical & Coding'],
            'organization_id': 'org_1',
            'days_since_created': 5,
            'participant_count': 50,
            'average_rating': 4.5
        }
    ]
    
    recommendations = recommendation_engine.recommend_events(
        user_profile,
        user_history,
        test_events,
        num_recommendations=5
    )
    
    assert len(recommendations) > 0
    assert recommendations[0]['score'] > 0.3
    print(f"✓ Recommendation score: {recommendations[0]['score']}")
```

Run tests:
```bash
python -m pytest test_custom_algorithm.py
```

---

## A/B Testing

Run two algorithms in parallel:

```python
from typing import List

class ABTestingEngine:
    def __init__(self, engine_a, engine_b, split_ratio=0.5):
        self.engine_a = engine_a
        self.engine_b = engine_b
        self.split_ratio = split_ratio
    
    def recommend(self, user_id: str, **kwargs) -> dict:
        """A/B test two algorithms."""
        import random
        
        use_engine_a = random.random() < self.split_ratio
        
        if use_engine_a:
            recommendations = self.engine_a.recommend_events(**kwargs)
            variant = 'A'
        else:
            recommendations = self.engine_b.recommend_events(**kwargs)
            variant = 'B'
        
        # Log variant for analysis
        return {
            'recommendations': recommendations,
            'variant': variant
        }
```

---

## Environment-Specific Configuration

```python
# app/config.py

if settings.NODE_ENV == "production":
    settings.MIN_SIMILARITY_SCORE = 0.5
    settings.NUM_RECOMMENDATIONS = 10
elif settings.NODE_ENV == "staging":
    settings.MIN_SIMILARITY_SCORE = 0.4
    settings.NUM_RECOMMENDATIONS = 8
else:  # development
    settings.MIN_SIMILARITY_SCORE = 0.3
    settings.NUM_RECOMMENDATIONS = 5
```

---

**For more help, see [README.md](README.md) and [API.md](API.md)**
