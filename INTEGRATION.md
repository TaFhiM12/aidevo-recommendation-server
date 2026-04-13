# Integration Checklist

Complete integration of the AI Recommendation Service with your main Aidevo backend.

## ✅ Microservice Setup

- [ ] Clone recommendation service to `/aidevo-recommendation-service`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Configure `.env` with MongoDB URI
- [ ] Generate dataset: `python scripts/generate_dataset.py`
- [ ] Train models: `python scripts/train_model.py`
- [ ] Test locally: `python -m app.main`
- [ ] Verify health: `curl http://localhost:5000/health`

## ✅ Backend Integration

- [ ] Create `aidevo-server/src/modules/recommendations/` directory
- [ ] Add `recommendation.routes.js` with endpoints
- [ ] Add `recommendation.controller.js` with logic
- [ ] Update `aidevo-server/src/app.js` to include recommendation routes
- [ ] Add `RECOMMENDATION_SERVICE_URL` to `.env`:
  ```
  RECOMMENDATION_SERVICE_URL=http://localhost:5000
  ```
- [ ] Test backend endpoint: `GET /recommendations`

## ✅ Frontend Integration

- [ ] Create `aidevo-client/src/hooks/useRecommendations.js`
- [ ] Create Recommendations display component
- [ ] Add to event listing pages
- [ ] Test recommendation fetching
- [ ] Verify proper error handling

## ✅ Database

- [ ] Ensure MongoDB collections exist:
  - [ ] `users` (with `uid`, `email`, `role`, `interests`)
  - [ ] `events` (with `attendees`, `tags`, `category`)
- [ ] Create indexes for performance:
  ```bash
  python -c "
  from pymongo import MongoClient
  client = MongoClient('YOUR_URI')
  db = client['aidevo']
  db.users.create_index('uid')
  db.events.create_index('organizationId')
  db.events.create_index('category')
  print('✓ Indexes created')
  "
  ```
- [ ] Verify user interaction data is being collected

## ✅ Local Testing

- [ ] Start recommendation service: `python -m app.main`
- [ ] Start backend: `npm run dev`
- [ ] Start frontend: `npm run dev`
- [ ] Login to app
- [ ] Navigate to event page
- [ ] Verify recommendations appear
- [ ] Check browser console for errors
- [ ] Monitor recommendation service logs

## ✅ Deployment Preparation

### Environment Variables

Backend `.env`:
```
RECOMMENDATION_SERVICE_URL=http://localhost:5000
# Production:
# RECOMMENDATION_SERVICE_URL=https://aidevo-recommendation-service.onrender.com
```

Recommendation Service `.env`:
```
MONGODB_URI=your_connection_string
DB_NAME=aidevo
PORT=5000
NODE_ENV=production
```

Frontend `.env`:
```
VITE_API_URL=https://your-backend-url
```

### Pre-Deployment Checklist

- [ ] All endpoints tested locally
- [ ] Error handling implemented
- [ ] Environment variables documented
- [ ] Models trained on latest data
- [ ] Database queries optimized
- [ ] CORS properly configured
- [ ] Rate limiting considered
- [ ] Logging configured
- [ ] Monitoring setup

## ✅ Production Deployment

### Step 1: Deploy Recommendation Service

**On Render:**
- [ ] New service > GitHub repo
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Add environment variables
- [ ] Deploy
- [ ] Test: `curl https://your-service.onrender.com/health`

### Step 2: Deploy Backend

- [ ] Update `RECOMMENDATION_SERVICE_URL` to production URL
- [ ] Deploy to Render
- [ ] Verify backend can reach recommendation service

### Step 3: Deploy Frontend

- [ ] Rebuild: `npm run build`
- [ ] Deploy to Firebase
- [ ] Test full flow: login → see recommendations

## ✅ Post-Deployment

- [ ] Monitor logs for errors
- [ ] Test all recommendation endpoints
- [ ] Verify user data flows correctly
- [ ] Check error rates
- [ ] Monitor performance metrics
- [ ] Set up alerts for downtime

## ✅ Optional Enhancements

- [ ] Add recommendation tracking/analytics
- [ ] A/B test different algorithms
- [ ] Add user feedback on recommendations
- [ ] Implement caching layer
- [ ] Add rate limiting
- [ ] Setup monitoring dashboards
- [ ] Create admin panel for recommendation tuning

## 🆘 Troubleshooting During Integration

| Issue | Solution |
|-------|----------|
| 404 on recommendations endpoint | Check route is registered in app.js |
| Empty recommendations | Verify user has interests/history in MongoDB |
| CORS errors | Check CORS configuration in main backend |
| Slow recommendations | Check MongoDB indexes, add caching |
| Connection refused | Verify RECOMMENDATION_SERVICE_URL is correct |
| Models not found | Run: `python scripts/train_model.py` |

---

## Support Resources

- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [API.md](API.md) - API reference
- [ADVANCED.md](ADVANCED.md) - Advanced configuration

---

**Last Updated:** January 2026
**Estimated Setup Time:** 15-30 minutes
