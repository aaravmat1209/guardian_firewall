import re
from typing import List, Dict, Any
from datetime import datetime

class TransformerWrapper:
    """
    Wrapper for transformer-based grooming detection model
    Currently uses rule-based patterns as a placeholder for actual ML model
    """

    def __init__(self):
        self.model_loaded = False
        # Placeholder for actual model weights
        self.confidence_threshold = 0.5

    def load_model(self, model_path: str = None):
        """Load the transformer model"""
        # Placeholder for actual model loading
        print("Loading transformer model (placeholder)")
        self.model_loaded = True

    def predict(self, text: str, context: List[str] = None) -> Dict[str, Any]:
        """
        Predict grooming risk for a message with context
        Returns confidence score and risk indicators
        """
        if not self.model_loaded:
            self.load_model()

        # Placeholder ML logic - replace with actual transformer inference
        risk_score = self._calculate_basic_risk(text, context or [])

        return {
            "confidence": min(risk_score, 1.0),
            "risk_indicators": self._extract_indicators(text),
            "context_analysis": self._analyze_context(context or [])
        }

    def _calculate_basic_risk(self, text: str, context: List[str]) -> float:
        """Basic risk calculation based on patterns"""
        risk_factors = 0
        text_lower = text.lower()

        # Age-related probing
        age_patterns = [
            r'\bhow old\b', r'\bage\b.*\?', r'\byears old\b',
            r'\bbirthday\b', r'\bgrade\b.*school'
        ]
        if any(re.search(pattern, text_lower) for pattern in age_patterns):
            risk_factors += 0.3

        # Personal information requests
        personal_patterns = [
            r'\bwhere.*live\b', r'\baddress\b', r'\bphone\b.*number\b',
            r'\breal name\b', r'\bschool.*name\b'
        ]
        if any(re.search(pattern, text_lower) for pattern in personal_patterns):
            risk_factors += 0.4

        # Isolation/secrecy language
        secrecy_patterns = [
            r'\bsecret\b', r'\bdon\'t tell\b', r'\bbetween us\b',
            r'\balone\b', r'\bprivate\b'
        ]
        if any(re.search(pattern, text_lower) for pattern in secrecy_patterns):
            risk_factors += 0.5

        # Off-platform movement
        platform_patterns = [
            r'\bwhatsapp\b', r'\bdiscord\b', r'\bprivate.*chat\b',
            r'\bmeet.*person\b', r'\bin real life\b'
        ]
        if any(re.search(pattern, text_lower) for pattern in platform_patterns):
            risk_factors += 0.6

        # Context escalation (check if conversation is getting more personal)
        if len(context) > 5:
            recent_messages = ' '.join(context[-5:]).lower()
            if len(re.findall(r'\bpersonal\b|\bspecial\b|\bclose\b', recent_messages)) > 2:
                risk_factors += 0.2

        return min(risk_factors, 1.0)

    def _extract_indicators(self, text: str) -> List[str]:
        """Extract specific risk indicators from text"""
        indicators = []
        text_lower = text.lower()

        if re.search(r'\bhow old\b|\bage\b', text_lower):
            indicators.append("age_inquiry")

        if re.search(r'\bsecret\b|\bdon\'t tell\b', text_lower):
            indicators.append("secrecy_language")

        if re.search(r'\bmeet\b|\bin person\b', text_lower):
            indicators.append("meeting_suggestion")

        if re.search(r'\bspecial\b|\bclose\b|\bunique\b', text_lower):
            indicators.append("relationship_building")

        return indicators

    def _analyze_context(self, context: List[str]) -> Dict[str, Any]:
        """Analyze conversation context for escalation patterns"""
        if not context:
            return {"escalation_detected": False, "pattern": "none"}

        # Simple escalation detection
        recent_text = ' '.join(context[-3:]).lower() if len(context) >= 3 else ''

        patterns = {
            "personal_info_gathering": len(re.findall(r'\bhow\b|\bwhat\b|\bwhere\b', recent_text)),
            "compliment_frequency": len(re.findall(r'\bbeautiful\b|\bspecial\b|\bsmart\b', recent_text)),
            "isolation_language": len(re.findall(r'\balone\b|\bsecret\b|\bprivate\b', recent_text))
        }

        escalation_score = sum(patterns.values())
        escalation_detected = escalation_score > 3

        return {
            "escalation_detected": escalation_detected,
            "escalation_score": escalation_score,
            "patterns": patterns
        }