from typing import List, Dict, Any
from .model import TransformerWrapper
from .rules import GroomingRules, RiskLevel

class RiskFusion:
    """
    Fuses ML model predictions with rule-based detections
    Applies calibrated scoring and thresholds for final risk assessment
    """

    def __init__(self):
        self.transformer = TransformerWrapper()
        self.rules_engine = GroomingRules()

        # Fusion weights
        self.ml_weight = 0.6
        self.rules_weight = 0.4

        # Calibrated thresholds
        self.low_threshold = 0.3
        self.medium_threshold = 0.6
        self.high_threshold = 0.8

    def analyze_message(self, text: str, conversation_history: List[str] = None) -> Dict[str, Any]:
        """
        Perform comprehensive risk analysis combining ML and rules
        """
        if not text.strip():
            return self._default_response()

        # Get ML prediction
        ml_result = self.transformer.predict(text, conversation_history or [])
        ml_score = ml_result["confidence"]

        # Get rule-based analysis
        rules_score, rule_explanations, rule_risk_level = self.rules_engine.analyze_message(text)

        # Fuse scores
        fused_score = (ml_score * self.ml_weight) + (rules_score * self.rules_weight)

        # Apply rule overrides for high-confidence detections
        if rule_risk_level == RiskLevel.HIGH and rules_score > 0.7:
            fused_score = max(fused_score, 0.8)  # Boost score for high-confidence rule matches

        # Determine final risk level
        final_risk_level = self._determine_risk_level(fused_score, rule_risk_level)

        # Combine explanations
        all_explanations = rule_explanations.copy()
        if ml_result.get("risk_indicators"):
            ml_explanations = [f"ML detected: {indicator}" for indicator in ml_result["risk_indicators"]]
            all_explanations.extend(ml_explanations)

        # Get safety suggestions if needed
        suggestions = []
        if final_risk_level in ["medium", "high"]:
            triggered_rules = [rule for rule in self.rules_engine.rules.keys()
                             if any(explanation in rule_explanations for explanation in [self.rules_engine.rules[rule]["explanation"]])]
            suggestions = self.rules_engine.get_safety_suggestions(triggered_rules)

        return {
            "level": final_risk_level,
            "score": round(fused_score, 3),
            "explanations": all_explanations,
            "suggestions": suggestions,
            "ml_score": round(ml_score, 3),
            "rules_score": round(rules_score, 3),
            "context_analysis": ml_result.get("context_analysis", {})
        }

    def analyze_conversation(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze entire conversation for escalation patterns and overall risk
        """
        if not messages:
            return {"overall_risk": "low", "escalation": False}

        # Extract text from messages
        message_texts = [msg.get("text", "") for msg in messages]

        # Get conversation-level analysis from rules
        conversation_analysis = self.rules_engine.analyze_conversation_patterns(message_texts)

        # Analyze recent message trend
        recent_scores = []
        for i, text in enumerate(message_texts[-5:]):  # Last 5 messages
            history = message_texts[:len(message_texts)-5+i] if i > 0 else []
            result = self.analyze_message(text, history)
            recent_scores.append(result["score"])

        # Overall risk assessment
        max_score = max(recent_scores) if recent_scores else 0
        avg_score = sum(recent_scores) / len(recent_scores) if recent_scores else 0

        overall_risk = self._determine_risk_level(max(max_score, avg_score))

        # Escalation detection
        escalation_detected = conversation_analysis["escalation_detected"]
        if len(recent_scores) >= 3:
            # Check if scores are increasing
            trend_escalation = recent_scores[-1] > recent_scores[0] + 0.2
            escalation_detected = escalation_detected or trend_escalation

        return {
            "overall_risk": overall_risk,
            "escalation_detected": escalation_detected,
            "max_score": round(max_score, 3),
            "average_score": round(avg_score, 3),
            "message_count": len(messages),
            "high_risk_patterns": conversation_analysis["high_risk_patterns"],
            "pattern_frequency": conversation_analysis["pattern_frequency"],
            "recent_trend": recent_scores
        }

    def _determine_risk_level(self, score: float, rule_level: RiskLevel = None) -> str:
        """
        Determine risk level based on fused score and rule overrides
        """
        # Rule-based override
        if rule_level == RiskLevel.HIGH:
            return "high"

        # Score-based determination
        if score >= self.high_threshold:
            return "high"
        elif score >= self.medium_threshold:
            return "medium"
        elif score >= self.low_threshold:
            return "low"
        else:
            return "low"

    def _default_response(self) -> Dict[str, Any]:
        """Return default response for empty/invalid input"""
        return {
            "level": "low",
            "score": 0.0,
            "explanations": [],
            "suggestions": [],
            "ml_score": 0.0,
            "rules_score": 0.0,
            "context_analysis": {}
        }

    def update_thresholds(self, low: float = None, medium: float = None, high: float = None):
        """
        Update risk thresholds for calibration
        """
        if low is not None:
            self.low_threshold = low
        if medium is not None:
            self.medium_threshold = medium
        if high is not None:
            self.high_threshold = high

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model configuration
        """
        return {
            "ml_weight": self.ml_weight,
            "rules_weight": self.rules_weight,
            "thresholds": {
                "low": self.low_threshold,
                "medium": self.medium_threshold,
                "high": self.high_threshold
            },
            "rules_count": len(self.rules_engine.rules),
            "model_loaded": self.transformer.model_loaded
        }