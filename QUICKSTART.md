# Quick Start Guide - Recommendation Service

Get up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- MongoDB Atlas account (or local MongoDB)

## Quick Setup

### 1. Install & Configure (2 min)

```bash
# Install dependencies
pip install -r requirements.txt

# Configure MongoDB
# Edit .env and add:
# MONGODB_URI=your_mongodb_connection_string
```

### 2. Generate Dataset (1 min)

```bash
python scripts/generate_dataset.py
```

You'll see:
```
✓ Inserted 50 students
✓ Inserted 15 organizations
✓ Inserted 75 events
✓ Generated interactions for 50 students
```

### 3. Train Models (1 min)

```bash
python scripts/train_model.py
```

You'll see:
```
✓ TF-IDF vectorizer trained with 100 features
✓ StandardScaler trained
✓ Models saved to ./models/
```

### 4. Start Service (1 min)

```bash
python -m app.main
```

You'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:5000
✓ Services initialized successfully
```

### 5. Test Recommendation (1 min)

```bash
# In another terminal:
curl -X POST http://localhost:5000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "student_1",
    "email": "200142@student.just.edu.bd",
    "num_recommendations": 5
  }'
```

Expected response:
```json
{
  "user_id": "student_1",
  "recommendations": [
    {
      "event_id": "...",
      "title": "Event Title",
      "score": 0.85,
      "category": "Workshop",
      "tags": ["Technical & Coding"]
    },
    ...
  ],
  "timestamp": "2024-01-15T..."
}
```

## What Next?

- **Integrate with backend:** See [README.md](README.md#integration-with-main-backend)
- **Deploy to production:** See [README.md](README.md#deployment)
- **Customize algorithm:** See [ADVANCED.md](ADVANCED.md)
- **Run tests:** See [TESTING.md](TESTING.md)

## Endpoints Cheat Sheet

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| POST | `/api/recommendations` | Get recommendations |
| POST | `/api/batch-recommendations` | Batch recommendations |
| GET | `/api/info` | Service info |

## Troubleshooting

**Models not found?**
```bash
python scripts/generate_dataset.py && python scripts/train_model.py
```

**MongoDB connection failed?**
- Check MONGODB_URI in .env
- Verify MongoDB is running
- For Atlas: whitelist your IP

**Service won't start?**
```bash
# Check if port 5000 is in use
lsof -i :5000

# Use different port
python -m app.main --port 5001
```

---

💡 **Tip:** For production, set `NODE_ENV=production` in your .env file.
