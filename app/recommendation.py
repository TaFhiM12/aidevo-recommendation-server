import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """ML-based event recommendation engine."""
    
    def __init__(self, model_path="./models/recommendation_model.pkl", 
                 tfidf_path="./models/tfidf_vectorizer.pkl",
                 scaler_path="./models/scaler.pkl"):
        self.model_path = model_path
        self.tfidf_path = tfidf_path
        self.scaler_path = scaler_path
        self.tfidf_vectorizer = None
        self.scaler = None
        
        # Weights for hybrid approach
        self.content_weight = 0.4
        self.collaborative_weight = 0.35
        self.engagement_weight_factor = 0.25
        self.min_score_threshold = 0.3
    
    def load_models(self):
        """Load trained models from disk."""
        try:
            if os.path.exists(self.tfidf_path):
                self.tfidf_vectorizer = joblib.load(self.tfidf_path)
                logger.info("✓ TF-IDF vectorizer loaded")
            else:
                logger.warning("TF-IDF vectorizer not found, using default")
                self.tfidf_vectorizer = TfidfVectorizer(max_features=100, stop_words='english', ngram_range=(1, 2))
            
            if os.path.exists(self.scaler_path):
                self.scaler = joblib.load(self.scaler_path)
                logger.info("✓ StandardScaler loaded")
            else:
                logger.warning("StandardScaler not found, using default")
                self.scaler = StandardScaler()
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.tfidf_vectorizer = TfidfVectorizer(max_features=100, stop_words='english', ngram_range=(1, 2))
            self.scaler = StandardScaler()
    
    def save_models(self):
        """Save models to disk."""
        try:
            os.makedirs("./models", exist_ok=True)
            if self.tfidf_vectorizer:
                joblib.dump(self.tfidf_vectorizer, self.tfidf_path)
            if self.scaler:
                joblib.dump(self.scaler, self.scaler_path)
            logger.info("Models saved successfully")
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def content_similarity(self, user_interests: list, event_tags: list) -> float:
        """Calculate content-based similarity using Jaccard index.
        
        Args:
            user_interests: List of user interests
            event_tags: List of event tags
        
        Returns:
            Similarity score between 0 and 1
        """
        if not user_interests or not event_tags:
            return 0.0
        
        user_set = set(user_interests)
        event_set = set(event_tags)
        
        intersection = len(user_set & event_set)
        union = len(user_set | event_set)
        
        return intersection / union if union > 0 else 0.0
    
    def collaborative_similarity(self, user_history: dict, event_info: dict) -> float:
        """Calculate collaborative filtering score.
        
        Args:
            user_history: User's event history and behavior
            event_info: Event information
        
        Returns:
            Collaborative score between 0 and 1
        """
        score = 0.0
        
        # Category preference (0.3)
        favorite_categories = [cat[0] for cat in user_history.get("favorite_categories", [])]
        if event_info.get("category") in favorite_categories:
            score += 0.3
        
        # Organization following (0.2)
        if event_info.get("organization_id") in user_history.get("followed_organizations", []):
            score += 0.2
        
        # User participation rate (0.1)
        participation_rate = user_history.get("participation_rate", 0)
        if participation_rate > 0.5:
            score += 0.1
        
        # Recency boost (0.15)
        days_since_created = event_info.get("days_since_created", 100)
        if days_since_created < 7:
            score += 0.15
        elif days_since_created < 30:
            score += 0.08
        
        return min(score, 1.0)
    
    def engagement_weight(self, event_info: dict) -> float:
        """Calculate engagement-based weight.
        
        Args:
            event_info: Event information
        
        Returns:
            Engagement weight between 0 and 1
        """
        score = 0.5  # Base score
        
        participant_count = event_info.get("participant_count", 0)
        if participant_count > 50:
            score += 0.2
        elif participant_count > 20:
            score += 0.1
        
        avg_rating = event_info.get("average_rating", 3.5)
        if avg_rating >= 4.5:
            score += 0.15
        elif avg_rating >= 4.0:
            score += 0.1
        elif avg_rating >= 3.5:
            score += 0.05
        
        return min(score, 1.0)
    
    def has_attended_event(self, event_id: str, user_history: dict) -> bool:
        """Check if user has already attended or registered for event."""
        return (event_id in user_history.get("attended_events", []) or 
                event_id in user_history.get("registered_events", []))
    
    def recommend_events(self, user_profile: dict, user_history: dict, 
                        available_events: list, num_recommendations: int = 5,
                        filter_category: str = None) -> list:
        """Generate event recommendations using hybrid algorithm.
        
        Args:
            user_profile: User's profile (interests, department, role)
            user_history: User's event history and behavior
            available_events: List of available events
            num_recommendations: Number of recommendations to return
            filter_category: Optional category filter
        
        Returns:
            List of recommended events with scores
        """
        try:
            recommendations = []
            
            # Filter out already attended events
            candidate_events = [
                e for e in available_events 
                if not self.has_attended_event(e.get("event_id"), user_history)
            ]
            
            # Apply category filter if specified
            if filter_category:
                candidate_events = [
                    e for e in candidate_events 
                    if e.get("category") == filter_category
                ]
            
            # Score each event
            for event in candidate_events:
                # Content-based score
                content_score = self.content_similarity(
                    user_profile.get("interests", []),
                    event.get("tags", [])
                )
                
                # Collaborative score
                collab_score = self.collaborative_similarity(
                    user_history,
                    event
                )
                
                # Engagement score
                engagement_score = self.engagement_weight(event)
                
                # Hybrid score (weighted combination)
                final_score = (
                    content_score * self.content_weight +
                    collab_score * self.collaborative_weight +
                    engagement_score * self.engagement_weight_factor
                )
                
                # Only include if above threshold
                if final_score >= self.min_score_threshold:
                    recommendations.append({
                        "event_id": event.get("event_id"),
                        "title": event.get("title"),
                        "category": event.get("category"),
                        "score": round(final_score, 3),
                        "content_score": round(content_score, 3),
                        "collaborative_score": round(collab_score, 3),
                        "engagement_score": round(engagement_score, 3),
                        "reason": self._generate_reason(content_score, collab_score, engagement_score)
                    })
            
            # Sort by score descending
            recommendations.sort(key=lambda x: x["score"], reverse=True)
            
            # Return top N
            return recommendations[:num_recommendations]
        
        except Exception as e:
            logger.error(f"Error in recommendation engine: {e}")
            return []
    
    def _generate_reason(self, content_score: float, collab_score: float, engage_score: float) -> str:
        """Generate human-readable reason for recommendation."""
        reasons = []
        
        if content_score > 0.5:
            reasons.append("matches your interests")
        
        if collab_score > 0.3:
            reasons.append("popular with similar users")
        
        if engage_score > 0.6:
            reasons.append("highly rated event")
        
        if not reasons:
            reasons = ["recommended for you"]
        
        return " & ".join(reasons)
    
    def set_weights(self, content: float = None, collaborative: float = None, engagement: float = None):
        """Update recommendation weights.
        
        Args:
            content: Weight for content-based (0-1)
            collaborative: Weight for collaborative (0-1)
            engagement: Weight for engagement (0-1)
        """
        if content is not None:
            self.content_weight = content
        if collaborative is not None:
            self.collaborative_weight = collaborative
        if engagement is not None:
            self.engagement_weight_factor = engagement
        
        logger.info(
            f"Weights updated: content={self.content_weight}, "
            f"collaborative={self.collaborative_weight}, "
            f"engagement={self.engagement_weight_factor}"
        )


# Global recommendation engine instance
recommendation_engine = RecommendationEngine()
