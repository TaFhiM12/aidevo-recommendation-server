# API Specification - Recommendation Service

Complete API reference for all endpoints.

## Base URL

- **Development:** `http://localhost:5000`
- **Production:** `https://aidevo-recommendation-service.onrender.com`

---

## Endpoints

### 1. Health Check

Check if the service is operational.

**Request**
```http
GET /health HTTP/1.1
```

**Response (200 OK)**
```json
{
  "status": "healthy",
  "service": "Aidevo Recommendation Service",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

### 2. Get Recommendations

Generate personalized event recommendations for a user based on their profile, interests, and past behavior.

**Request**
```http
POST /api/recommendations HTTP/1.1
Content-Type: application/json

{
  "user_id": "student_1",
  "email": "user@student.just.edu.bd",
  "num_recommendations": 5,
  "filter_category": "Workshop",
  "filter_organization_id": "org_1"
}
```

**Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string | Yes | Unique user identifier |
| `email` | string | Yes | User email address |
| `num_recommendations` | integer | No | Number of recommendations (default: 5, max: 20) |
| `filter_category` | string | No | Filter by event category |
| `filter_organization_id` | string | No | Filter by organization ID |

**Response (200 OK)**
```json
{
  "user_id": "student_1",
  "recommendations": [
    {
      "event_id": "507f1f77bcf86cd799439011",
      "title": "Web Development Workshop",
      "score": 0.85,
      "content_score": 0.8,
      "collab_score": 0.7,
      "engagement_score": 0.95,
      "category": "Workshop",
      "tags": ["Technical & Coding", "Web Development"]
    },
    {
      "event_id": "507f1f77bcf86cd799439012",
      "title": "Leadership Seminar",
      "score": 0.72,
      "content_score": 0.7,
      "collab_score": 0.75,
      "engagement_score": 0.68,
      "category": "Seminar",
      "tags": ["Leadership & Development"]
    }
  ],
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Error Response (404 Not Found)**
```json
{
  "detail": "User not found"
}
```

**Error Response (500 Internal Server Error)**
```json
{
  "detail": "Error generating recommendations"
}
```

---

### 3. Batch Recommendations

Get recommendations for multiple users in a single request.

**Request**
```http
POST /api/batch-recommendations HTTP/1.1
Content-Type: application/json

{
  "user_ids": ["student_1", "student_2", "student_3"]
}
```

**Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_ids` | array | Yes | List of user IDs (max: 100) |

**Response (200 OK)**
```json
{
  "status": "success",
  "results": {
    "student_1": {
      "count": 5,
      "top_recommendation": {
        "event_id": "507f1f77bcf86cd799439011",
        "title": "Web Development Workshop",
        "score": 0.85
      }
    },
    "student_2": {
      "count": 3,
      "top_recommendation": {
        "event_id": "507f1f77bcf86cd799439012",
        "title": "Leadership Seminar",
        "score": 0.72
      }
    },
    "student_3": {
      "count": 5,
      "top_recommendation": {
        "event_id": "507f1f77bcf86cd799439013",
        "title": "Networking Event",
        "score": 0.68
      }
    }
  }
}
```

---

### 4. Service Info

Get metadata about the recommendation service.

**Request**
```http
GET /api/info HTTP/1.1
```

**Response (200 OK)**
```json
{
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
```

---

## Request/Response Details

### Scoring Components

Each recommendation includes three sub-scores:

- **`content_score`** (0-1): How well event tags match user interests
- **`collab_score`** (0-1): Based on similar users' behavior
- **`engagement_score`** (0-1): Event popularity and quality metrics

**Final Score Formula:**
```
score = (content_score × 0.4) + (collab_score × 0.35) + (engagement_score × 0.25)
```

Only recommendations with score ≥ 0.3 are returned.

### Event Object Structure

```json
{
  "event_id": "507f1f77bcf86cd799439011",
  "title": "string",
  "category": "Workshop|Seminar|Tournament|Conference|Social|etc",
  "tags": ["string"],
  "score": 0.85
}
```

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error description"
}
```

### Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 404 | User not found |
| 500 | Server error |

---

## Rate Limiting

- No rate limiting implemented by default
- For production: implement rate limiting using middleware

---

## CORS Support

- ✅ All origins allowed (`*`)
- ✅ Credentials supported
- ✅ All HTTP methods allowed
- ✅ All headers allowed

---

## Pagination

Not currently supported. Use `num_recommendations` to limit results (max: 20).

---

## Caching

No caching implemented. Each request generates fresh recommendations.

---

## Authentication

Current implementation is open (no authentication required).

For production deployment, consider adding:
- JWT token validation
- API key authentication
- OAuth2

---

## Example Usage

### JavaScript/Fetch

```javascript
const getRecommendations = async (userId) => {
  const response = await fetch('http://localhost:5000/api/recommendations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId,
      email: userEmail,
      num_recommendations: 5
    })
  });

  return response.json();
};
```

### Python/Requests

```python
import requests

response = requests.post(
    'http://localhost:5000/api/recommendations',
    json={
        'user_id': 'student_1',
        'email': 'user@student.just.edu.bd',
        'num_recommendations': 5
    }
)

print(response.json())
```

### cURL

```bash
curl -X POST http://localhost:5000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "student_1",
    "email": "user@student.just.edu.bd",
    "num_recommendations": 5
  }'
```

---

## API Version

Current version: `1.0.0`

Breaking changes will increment major version.

---

**Last Updated:** January 2026
