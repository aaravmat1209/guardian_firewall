# DEPRECATED: This file is being replaced by whole_detector.py
# The new Guardian system uses Gemini LLM + Hugging Face models
# instead of the hardcoded rule-based approach.

from typing import List, Dict, Any
from .whole_detector import get_detector

class RiskFusion:
    """
    Legacy wrapper for compatibility - redirects to new whole_detector
    """

    def __init__(self):
        self.detector = get_detector()

    def analyze_message(self, text: str, conversation_history: List[str] = None) -> Dict[str, Any]:
        """
        Legacy method - redirects to new detector
        """
        # Convert old format to new format
        history = []
        if conversation_history:
            for i, msg in enumerate(conversation_history):
                history.append({
                    "username": "Unknown",
                    "text": msg,
                    "timestamp": i  # Use index as fake timestamp
                })

        # Use new detector
        result = self.detector.analyze_message(text, history)

        # Convert back to old format for compatibility
        return {
            "level": result.final_level.lower(),
            "score": result.final_score,
            "explanations": result.explanations,
            "suggestions": [],  # Not implemented in new detector
            "ml_score": 0.0,  # Legacy field
            "rules_score": 0.0,  # Legacy field
            "hf_score": result.hf_score,
            "context_analysis": {}
        }

    def analyze_conversation(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Legacy method for conversation analysis
        """
        if not messages:
            return {"overall_risk": "low", "escalation_detected": False}

        # Analyze the last message with full context
        last_message = messages[-1].get("text", "")
        result = self.detector.analyze_message(last_message, messages[:-1])

        return {
            "overall_risk": result.final_level.lower(),
            "escalation_detected": result.final_score > 0.6,
            "max_score": result.final_score,
            "average_score": result.final_score,
            "message_count": len(messages)
        }