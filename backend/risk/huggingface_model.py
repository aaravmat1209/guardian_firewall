"""
Hugging Face integration for enhanced risk scoring
"""
import requests
import os
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class HuggingFaceRiskScorer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.api_url = "https://api-inference.huggingface.co/models"

        # Model endpoints for different types of analysis
        self.models = {
            "toxicity": "martin-ha/toxic-comment-model",
            "sentiment": "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "safety": "unitary/toxic-bert",
            "grooming": "Hate-speech-CNERG/dehatebert-mono-english"  # Can be fine-tuned for grooming
        }

    def query_model(self, model_name: str, text: str) -> Dict:
        """Query a Hugging Face model via API"""
        if not self.api_key:
            logger.warning("No Hugging Face API key provided")
            return {"error": "No API key"}

        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.api_url}/{model_name}"

        payload = {"inputs": text}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error querying {model_name}: {e}")
            return {"error": str(e)}

    def analyze_toxicity(self, text: str) -> Dict:
        """Analyze text toxicity using specialized model"""
        result = self.query_model(self.models["toxicity"], text)

        if "error" in result:
            return {"toxicity_score": 0.0, "confidence": 0.0, "error": result["error"]}

        try:
            # Parse the result based on model output format
            if isinstance(result, list) and len(result) > 0:
                scores = result[0]
                if isinstance(scores, list):
                    # Find toxic/non-toxic scores
                    toxic_score = 0.0
                    for item in scores:
                        if item.get("label", "").lower() in ["toxic", "toxicity"]:
                            toxic_score = item.get("score", 0.0)
                            break

                    return {
                        "toxicity_score": toxic_score,
                        "confidence": max([item.get("score", 0.0) for item in scores]),
                        "details": scores
                    }

            return {"toxicity_score": 0.0, "confidence": 0.0, "raw_result": result}

        except Exception as e:
            logger.error(f"Error parsing toxicity result: {e}")
            return {"toxicity_score": 0.0, "confidence": 0.0, "error": str(e)}

    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment to detect manipulation patterns"""
        result = self.query_model(self.models["sentiment"], text)

        if "error" in result:
            return {"sentiment": "neutral", "confidence": 0.0, "error": result["error"]}

        try:
            if isinstance(result, list) and len(result) > 0:
                scores = result[0]
                if isinstance(scores, list):
                    # Find highest scoring sentiment
                    best_sentiment = max(scores, key=lambda x: x.get("score", 0.0))
                    return {
                        "sentiment": best_sentiment.get("label", "neutral").lower(),
                        "confidence": best_sentiment.get("score", 0.0),
                        "all_scores": scores
                    }

            return {"sentiment": "neutral", "confidence": 0.0, "raw_result": result}

        except Exception as e:
            logger.error(f"Error parsing sentiment result: {e}")
            return {"sentiment": "neutral", "confidence": 0.0, "error": str(e)}

    def detect_grooming_patterns(self, text: str) -> Dict:
        """Use hate speech model as proxy for inappropriate content detection"""
        result = self.query_model(self.models["grooming"], text)

        if "error" in result:
            return {"grooming_risk": 0.0, "confidence": 0.0, "error": result["error"]}

        try:
            if isinstance(result, list) and len(result) > 0:
                scores = result[0]
                if isinstance(scores, list):
                    # Look for hate/inappropriate content indicators
                    risk_score = 0.0
                    for item in scores:
                        label = item.get("label", "").lower()
                        if "hate" in label or "offensive" in label:
                            risk_score = max(risk_score, item.get("score", 0.0))

                    return {
                        "grooming_risk": risk_score,
                        "confidence": max([item.get("score", 0.0) for item in scores]),
                        "details": scores
                    }

            return {"grooming_risk": 0.0, "confidence": 0.0, "raw_result": result}

        except Exception as e:
            logger.error(f"Error parsing grooming detection result: {e}")
            return {"grooming_risk": 0.0, "confidence": 0.0, "error": str(e)}

    def comprehensive_analysis(self, text: str, conversation_history: List[Dict] = None) -> Dict:
        """Run comprehensive analysis combining multiple models"""

        # Analyze individual message
        toxicity = self.analyze_toxicity(text)
        sentiment = self.analyze_sentiment(text)
        grooming = self.detect_grooming_patterns(text)

        # Calculate composite risk score
        risk_factors = {
            "toxicity": toxicity.get("toxicity_score", 0.0) * 0.4,
            "grooming_indicators": grooming.get("grooming_risk", 0.0) * 0.5,
            "sentiment_manipulation": self._assess_sentiment_risk(sentiment) * 0.1
        }

        # Analyze conversation context if provided
        if conversation_history:
            context_risk = self._analyze_conversation_context(conversation_history)
            risk_factors["conversation_escalation"] = context_risk * 0.3

        # Calculate final risk score (0-1)
        total_risk = min(sum(risk_factors.values()), 1.0)

        # Determine risk level
        if total_risk >= 0.7:
            risk_level = "high"
        elif total_risk >= 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "risk_score": total_risk,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "model_results": {
                "toxicity": toxicity,
                "sentiment": sentiment,
                "grooming": grooming
            },
            "explanations": self._generate_explanations(risk_factors, total_risk)
        }

    def _assess_sentiment_risk(self, sentiment_result: Dict) -> float:
        """Assess risk based on sentiment analysis"""
        sentiment = sentiment_result.get("sentiment", "neutral")
        confidence = sentiment_result.get("confidence", 0.0)

        # Overly positive sentiment might indicate manipulation
        if sentiment == "positive" and confidence > 0.8:
            return 0.3  # Moderate concern for manipulation
        elif sentiment == "negative" and confidence > 0.7:
            return 0.6  # Higher concern for aggressive behavior

        return 0.0

    def _analyze_conversation_context(self, conversation_history: List[Dict]) -> float:
        """Analyze conversation history for escalation patterns"""
        if not conversation_history or len(conversation_history) < 2:
            return 0.0

        # Simple escalation detection - can be enhanced
        recent_messages = conversation_history[-5:]  # Last 5 messages
        risk_progression = []

        for msg in recent_messages:
            # Quick toxicity check on historical messages
            if isinstance(msg, dict) and "text" in msg:
                toxicity = self.analyze_toxicity(msg["text"])
                risk_progression.append(toxicity.get("toxicity_score", 0.0))

        if len(risk_progression) >= 2:
            # Check if risk is escalating
            recent_avg = sum(risk_progression[-2:]) / 2
            earlier_avg = sum(risk_progression[:-2]) / max(len(risk_progression) - 2, 1)

            if recent_avg > earlier_avg * 1.5:  # 50% increase indicates escalation
                return min(recent_avg * 1.2, 1.0)

        return sum(risk_progression) / len(risk_progression) if risk_progression else 0.0

    def _generate_explanations(self, risk_factors: Dict, total_risk: float) -> List[str]:
        """Generate human-readable explanations for the risk assessment"""
        explanations = []

        if risk_factors.get("toxicity", 0) > 0.3:
            explanations.append("Message contains toxic or harmful language")

        if risk_factors.get("grooming_indicators", 0) > 0.4:
            explanations.append("Potential grooming patterns detected")

        if risk_factors.get("sentiment_manipulation", 0) > 0.2:
            explanations.append("Sentiment patterns suggest potential manipulation")

        if risk_factors.get("conversation_escalation", 0) > 0.3:
            explanations.append("Conversation shows escalating risk pattern")

        if total_risk >= 0.7:
            explanations.append("Multiple high-risk indicators present")

        return explanations if explanations else ["Content appears safe"]


# For use without API key - local fallback models could be added here
class LocalRiskScorer:
    """Fallback scorer for when Hugging Face API is not available"""

    def comprehensive_analysis(self, text: str, conversation_history: List[Dict] = None) -> Dict:
        """Simple rule-based fallback analysis"""

        # Basic keyword-based risk assessment
        high_risk_keywords = [
            "secret", "don't tell", "between us", "age", "old are you",
            "meet", "address", "phone", "personal", "private"
        ]

        medium_risk_keywords = [
            "alone", "parents", "family", "school", "real name"
        ]

        text_lower = text.lower()

        high_risk_count = sum(1 for keyword in high_risk_keywords if keyword in text_lower)
        medium_risk_count = sum(1 for keyword in medium_risk_keywords if keyword in text_lower)

        # Calculate basic risk score
        risk_score = min((high_risk_count * 0.3 + medium_risk_count * 0.15), 1.0)

        if risk_score >= 0.6:
            risk_level = "high"
        elif risk_score >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"

        explanations = []
        if high_risk_count > 0:
            explanations.append(f"Contains {high_risk_count} high-risk keywords")
        if medium_risk_count > 0:
            explanations.append(f"Contains {medium_risk_count} medium-risk keywords")

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": {
                "keyword_analysis": risk_score,
                "high_risk_keywords": high_risk_count,
                "medium_risk_keywords": medium_risk_count
            },
            "explanations": explanations if explanations else ["Content appears safe"],
            "model": "local_fallback"
        }