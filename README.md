# Aidevo AI Recommendation Service

Complete AI-powered event recommendation microservice built with FastAPI and machine learning. Uses a hybrid approach combining content-based filtering, collaborative filtering, and engagement metrics.

## 📋 Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Dataset Generation](#dataset-generation)
6. [Model Training](#model-training)
7. [Running the Service](#running-the-service)
8. [API Documentation](#api-documentation)
9. [Integration with Main Backend](#integration-with-main-backend)
10. [Deployment](#deployment)
11. [Troubleshooting](#troubleshooting)

---

## ✨ Features

- **Hybrid Recommendation Algorithm**
  - 40% Content-based (interests & tags)
  - 35% Collaborative filtering (user behavior)
  - 25% Engagement metrics (popularity & ratings)

- **Real-time Recommendations**
  - Fast inference
  - Scalable architecture

- **Batch Processing**
  - Process recommendations for multiple users
  - Analytics and logging

- **Flexible Filtering**
  - Filter by event category
  - Filter by organization

- **RESTful API**
  - Easy integration
  - CORS enabled
  - Production-ready

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
│                    Firebase Hosted                          │
└──────────────────────────┬──────────────────────────────────┘
                          │ HTTP/REST
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Main Backend                             │
│                    (Node.js + Express)                      │
│                    Render Deployed                          │
└─────────────────────────┬──────────────────────────────────┘
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
        ┌─────────────────┐  ┌─────────────────────────┐
        │    MongoDB      │  │ AI Recommendation       │
        │    Database     │  │ Service (FastAPI)       │
        │                 │  │ Port: 5000              │
        └─────────────────┘  │ Render Deployed         │
                             └─────────────────────────┘
                                    │
                             ┌──────┴──────┐
                             ▼             ▼
                        Models      Algorithms
                      - TF-IDF      - Content
                      - Scaler      - Collab
                                    - Engagement
```

---

## 📦 Prerequisites

- Python 3.8+
- MongoDB (Atlas or local)
- pip

---

## 🚀 Installation

### Step 1: Clone and Setup

```bash
cd /path/to/project
cd aidevo-recommendation-service

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your MongoDB connection string
nano .env
```

Required environment variables:
```
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true
DB_NAME=aidevo
PORT=5000
HOST=0.0.0.0
NODE_ENV=development
```

---

## 📊 Dataset Generation

The project includes a script to generate a realistic dataset with:
- 50 sample students
- 15 sample organizations
- 75 sample events
- User-event interactions

### Generate Dataset

```bash
python scripts/generate_dataset.py
```

Output:
```
============================================================
Aidevo Recommendation Dataset Generator
============================================================

[1/5] Cleaning up existing collections...
✓ Collections cleaned

[2/5] Generating 50 sample students...
✓ Inserted 50 students

[3/5] Generating 15 sample organizations...
✓ Inserted 15 organizations

[4/5] Generating 75 sample events (5 per organization)...
✓ Inserted 75 events

[5/5] Generating user-event interactions...
✓ Generated interactions for 50 students

============================================================
Dataset Summary
============================================================
Total Students: 50
Total Organizations: 15
Total Events: 75
Total Event Attendances: 287
Total Event Registrations: 412
Total Event Views: 892
============================================================

✓ Dataset generation completed successfully!
```

---

## 🤖 Model Training

Train the recommendation models using the dataset:

```bash
python scripts/train_model.py
```

Output:
```
============================================================
Aidevo Recommendation Model Training
============================================================

[1/3] Fetching event data from MongoDB...
✓ Loaded 75 events

[2/3] Training TF-IDF vectorizer on event descriptions...
✓ TF-IDF vectorizer trained with 100 features

[3/3] Training StandardScaler for numerical features...
✓ StandardScaler trained
✓ Models saved to ./models/

============================================================
Training Statistics
============================================================
Events processed: 75
TF-IDF features: 100
Average attendees per event: 3.8
Average event rating: 4.15
============================================================

✓ Model training completed successfully!
```

Models saved:
- `models/recommendation_model.pkl` - Main model
- `models/tfidf_vectorizer.pkl` - Text vectorizer
- `models/scaler.pkl` - Feature scaler

---

## ▶️ Running the Service

### Development Mode

```bash
python -m app.main
```

Or with auto-reload:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

Output:
```
INFO:     Uvicorn running on http://0.0.0.0:5000
✓ Services initialized successfully
```

### Production Mode

```bash
NODE_ENV=production uvicorn app.main:app --host 0.0.0.0 --port 5000 --workers 4
```

---

## 📡 API Documentation

### Health Check

**Endpoint:** `GET /health`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Aidevo Recommendation Service",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

### Get Recommendations

**Endpoint:** `POST /api/recommendations`

Generate personalized event recommendations for a user.

**Request:**
```json
{
  "user_id": "student_1",
  "email": "200142@student.just.edu.bd",
  "num_recommendations": 5,
  "filter_category": null,
  "filter_organization_id": null
}
```

**Response:**
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

---

### Batch Recommendations

**Endpoint:** `POST /api/batch-recommendations`

Get recommendations for multiple users.

**Request:**
```json
{
  "user_ids": ["student_1", "student_2", "student_3"]
}
```

**Response:**
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
      "top_recommendation": {...}
    }
  }
}
```

---

### Service Info

**Endpoint:** `GET /api/info`

Get service metadata and algorithm info.

**Response:**
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

## 🔗 Integration with Main Backend

### Step 1: Update Main Backend Routes

Add a new route to your Node.js backend to call the recommendation service:

**File:** `aidevo-server/src/modules/recommendations/recommendation.routes.js`

```javascript
import { Router } from "express";
import { authenticateJWT } from "../../middleware/authenticateJWT.js";
import recommendationController from "./recommendation.controller.js";

const router = Router();

// Get recommendations for current user
router.get(
  "/",
  authenticateJWT,
  recommendationController.getRecommendations
);

// Get recommendations with filters
router.get(
  "/category/:category",
  authenticateJWT,
  recommendationController.getRecommendationsByCategory
);

export default router;
```

**File:** `aidevo-server/src/modules/recommendations/recommendation.controller.js`

```javascript
import asyncHandler from "../../utils/asyncHandler.js";
import sendResponse from "../../utils/sendResponse.js";
import axios from "axios";
import env from "../../config/env.js";

const RECOMMENDATION_SERVICE_URL = process.env.RECOMMENDATION_SERVICE_URL || 
  "http://localhost:5000";

const getRecommendations = asyncHandler(async (req, res) => {
  const { numReccommendations = 5, filterCategory, filterOrganization } = req.query;
  
  try {
    const response = await axios.post(
      `${RECOMMENDATION_SERVICE_URL}/api/recommendations`,
      {
        user_id: req.user.uid,
        email: req.user.email,
        num_recommendations: parseInt(numReccommendations),
        filter_category: filterCategory || null,
        filter_organization_id: filterOrganization || null
      }
    );

    return sendResponse(res, {
      statusCode: 200,
      success: true,
      message: "Recommendations fetched successfully",
      data: response.data.recommendations
    });
  } catch (error) {
    return sendResponse(res, {
      statusCode: 500,
      success: false,
      message: "Failed to fetch recommendations",
      error: error.message
    });
  }
});

const getRecommendationsByCategory = asyncHandler(async (req, res) => {
  const { category } = req.params;
  const { numReccommendations = 5 } = req.query;
  
  const response = await axios.post(
    `${RECOMMENDATION_SERVICE_URL}/api/recommendations`,
    {
      user_id: req.user.uid,
      email: req.user.email,
      num_recommendations: parseInt(numReccommendations),
      filter_category: category
    }
  );

  return sendResponse(res, {
    statusCode: 200,
    success: true,
    message: "Category recommendations fetched",
    data: response.data.recommendations
  });
});

const recommendationController = {
  getRecommendations,
  getRecommendationsByCategory
};

export default recommendationController;
```

### Step 2: Update Main App Routes

**File:** `aidevo-server/src/app.js`

```javascript
import recommendationRoutes from "./modules/recommendations/recommendation.routes.js";

// ... other imports

// Add to app.use() section:
app.use("/recommendations", recommendationRoutes);
```

### Step 3: Update Environment

Add to your backend `.env`:

```
RECOMMENDATION_SERVICE_URL=http://localhost:5000
# For production:
# RECOMMENDATION_SERVICE_URL=https://aidevo-recommendation-service.onrender.com
```

### Step 4: Frontend Integration

**File:** `aidevo-client/src/hooks/useRecommendations.js`

```javascript
import { useEffect, useState } from "react";
import API from "../utils/api";

const useRecommendations = (numReccommendations = 5) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      const response = await API.get("/recommendations", {
        params: {
          numReccommendations
        }
      });
      setRecommendations(response.data);
      setError(null);
    } catch (err) {
      setError(err);
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, [numReccommendations]);

  return { recommendations, loading, error, refetch: fetchRecommendations };
};

export default useRecommendations;
```

---

## 🚀 Deployment

### Option 1: Deploy on Render (Recommended)

1. Create new service on Render
2. Connect your GitHub repository
3. Set deploy command: `pip install -r requirements.txt && python scripts/generate_dataset.py && python scripts/train_model.py`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard
6. Deploy!

### Option 2: Docker Deployment

**File:** `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python scripts/generate_dataset.py
RUN python scripts/train_model.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

**File:** `docker-compose.yml`

```yaml
version: '3.8'

services:
  recommendation-service:
    build: .
    ports:
      - "5000:5000"
    environment:
      MONGODB_URI: ${MONGODB_URI}
      DB_NAME: aidevo
      NODE_ENV: production
    depends_on:
      - mongodb

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

Deploy:
```bash
docker-compose up -d
```

---

## 🔧 Troubleshooting

### Models not found error

**Problem:** `FileNotFoundError: [Errno 2] No such file or directory: './models/recommendation_model.pkl'`

**Solution:**
```bash
# Ensure models directory exists
mkdir -p models

# Train models
python scripts/train_model.py
```

### MongoDB connection error

**Problem:** `pymongo.errors.ServerSelectionTimeoutError`

**Solution:**
- Verify MongoDB URI in `.env`
- Check MongoDB is running (Atlas or local)
- Ensure network access (for Atlas, whitelist IP)

```bash
# Test connection
python -c "from pymongo import MongoClient; client = MongoClient('YOUR_URI'); print(client.server_info())"
```

### Empty recommendations

**Problem:** Getting empty recommendations list

**Solution:**
```bash
# Regenerate dataset
python scripts/generate_dataset.py

# Retrain models
python scripts/train_model.py

# Restart service
python -m app.main
```

### Port already in use

**Problem:** `Address already in use`

**Solution:**
```bash
# Kill process on port 5000
lsof -i :5000
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 5001
```

---

## 📊 ML Algorithm Details

### Content-Based Filtering (40% weight)

Calculates Jaccard similarity between user interests and event tags:

```
similarity = |user_interests ∩ event_tags| / |user_interests ∪ event_tags|
```

### Collaborative Filtering (35% weight)

Based on user behavior patterns:
- Attended same category events
- Followed same organizations  
- Event participation rate
- Recent event activity

### Engagement Metrics (25% weight)

Event popularity and quality:
- Participant count
- Average rating
- Recent creation

### Final Score

```
final_score = (content × 0.4) + (collaborative × 0.35) + (engagement × 0.25)

Recommendations filtered by: final_score ≥ MIN_SIMILARITY_SCORE (0.3)
```

---

## 📝 File Structure

```
aidevo-recommendation-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Settings
│   ├── database.py             # MongoDB connection
│   ├── models.py               # Pydantic models
│   └── recommendation.py        # ML engine
├── scripts/
│   ├── __init__.py
│   ├── generate_dataset.py     # Dataset generation
│   └── train_model.py          # Model training
├── models/                      # Trained models (generated)
│   ├── recommendation_model.pkl
│   ├── tfidf_vectorizer.pkl
│   └── scaler.pkl
├── data/                        # Data files (if needed)
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── .env.example                 # Example env file
└── README.md                    # This file
```

---

## 🤝 Support

For issues or questions:
1. Check troubleshooting section
2. Review API documentation
3. Check MongoDB connection
4. Verify dataset is generated and models are trained

---

## 📄 License

ISC

---

**Last Updated:** January 2026
**Version:** 1.0.0
