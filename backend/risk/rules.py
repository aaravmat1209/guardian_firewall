import re
from typing import List, Dict, Tuple
from enum import Enum

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class GroomingRules:
    """
    High-precision rule-based detection for grooming patterns
    Uses regex and finite-state patterns for specific behaviors
    """

    def __init__(self):
        self.rules = self._initialize_rules()

    def _initialize_rules(self) -> Dict[str, Dict]:
        """Initialize rule patterns with their risk levels and explanations"""
        return {
            "age_probing": {
                "patterns": [
                    r'\b(?:how old are you|what\'s your age|how old)\b',
                    r'\b(?:age|birthday|born in|year.*born)\b.*\?',
                    r'\b(?:young|older|younger)\b.*\?',
                    r'\b(?:grade|school year)\b.*\?'
                ],
                "risk_level": RiskLevel.MEDIUM,
                "explanation": "Attempting to determine victim's age",
                "weight": 0.4
            },

            "secrecy_enforcement": {
                "patterns": [
                    r'\b(?:don\'t tell|keep.*secret|between us|our secret)\b',
                    r'\b(?:don\'t mention|don\'t say|private conversation)\b',
                    r'\b(?:just between|only we know|secret friend)\b'
                ],
                "risk_level": RiskLevel.HIGH,
                "explanation": "Enforcing secrecy - major red flag",
                "weight": 0.8
            },

            "isolation_tactics": {
                "patterns": [
                    r'\b(?:nobody understands|only I understand|special connection)\b',
                    r'\b(?:different from others|mature for your age|not like other)\b',
                    r'\b(?:our special|unique relationship|special bond)\b'
                ],
                "risk_level": RiskLevel.HIGH,
                "explanation": "Isolation and special relationship building",
                "weight": 0.7
            },

            "gift_offers": {
                "patterns": [
                    r'\b(?:buy you|get you.*gift|send you money|give you)\b',
                    r'\b(?:present|surprise|reward|treat)\b.*\bfor\b',
                    r'\b(?:allowance|pocket money|cash|gift card)\b'
                ],
                "risk_level": RiskLevel.MEDIUM,
                "explanation": "Offering gifts or money",
                "weight": 0.5
            },

            "platform_migration": {
                "patterns": [
                    r'\b(?:whatsapp|telegram|discord|private chat)\b',
                    r'\b(?:my phone|text me|call me|video call)\b',
                    r'\b(?:different app|another platform|private server)\b',
                    r'\b(?:add me on|friend me on)\b'
                ],
                "risk_level": RiskLevel.HIGH,
                "explanation": "Attempting to move conversation off platform",
                "weight": 0.9
            },

            "meeting_requests": {
                "patterns": [
                    r'\b(?:meet in person|see you|meet up|hang out)\b',
                    r'\b(?:in real life|IRL|face to face)\b',
                    r'\b(?:come over|visit|my place|your place)\b',
                    r'\b(?:pick you up|drive you|meet somewhere)\b'
                ],
                "risk_level": RiskLevel.HIGH,
                "explanation": "Requesting in-person meeting",
                "weight": 1.0
            },

            "personal_info_gathering": {
                "patterns": [
                    r'\b(?:where do you live|what city|your address)\b',
                    r'\b(?:phone number|real name|last name)\b',
                    r'\b(?:school name|which school|where.*study)\b',
                    r'\b(?:parents.*work|family|siblings)\b'
                ],
                "risk_level": RiskLevel.MEDIUM,
                "explanation": "Gathering personal information",
                "weight": 0.6
            },

            "inappropriate_compliments": {
                "patterns": [
                    r'\b(?:sexy|hot|beautiful|gorgeous|attractive)\b',
                    r'\b(?:body|figure|looks|appearance)\b.*\b(?:nice|good|great)\b',
                    r'\b(?:cute|pretty)\b.*\b(?:girl|boy)\b'
                ],
                "risk_level": RiskLevel.MEDIUM,
                "explanation": "Inappropriate appearance-focused compliments",
                "weight": 0.5
            },

            "trust_building": {
                "patterns": [
                    r'\b(?:trust me|you can tell me|I understand)\b',
                    r'\b(?:safe with me|won\'t judge|here for you)\b',
                    r'\b(?:best friend|special friend|close friend)\b'
                ],
                "risk_level": RiskLevel.LOW,
                "explanation": "Excessive trust-building language",
                "weight": 0.3
            }
        }

    def analyze_message(self, text: str) -> Tuple[float, List[str], RiskLevel]:
        """
        Analyze a single message against all rules
        Returns (risk_score, explanations, risk_level)
        """
        triggered_rules = []
        total_score = 0.0
        explanations = []

        text_lower = text.lower()

        for rule_name, rule_data in self.rules.items():
            for pattern in rule_data["patterns"]:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    triggered_rules.append(rule_name)
                    total_score += rule_data["weight"]
                    explanations.append(rule_data["explanation"])
                    break  # Only count each rule once per message

        # Normalize score and determine risk level
        normalized_score = min(total_score, 1.0)

        if normalized_score >= 0.7:
            risk_level = RiskLevel.HIGH
        elif normalized_score >= 0.4:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW

        return normalized_score, explanations, risk_level

    def analyze_conversation_patterns(self, messages: List[str]) -> Dict:
        """
        Analyze patterns across multiple messages for escalation
        """
        if not messages:
            return {"escalation_detected": False, "pattern_frequency": {}}

        pattern_frequency = {rule: 0 for rule in self.rules.keys()}
        message_scores = []

        for message in messages:
            score, _, _ = self.analyze_message(message)
            message_scores.append(score)

            # Count pattern occurrences
            text_lower = message.lower()
            for rule_name, rule_data in self.rules.items():
                for pattern in rule_data["patterns"]:
                    if re.search(pattern, text_lower, re.IGNORECASE):
                        pattern_frequency[rule_name] += 1
                        break

        # Detect escalation
        escalation_detected = False
        if len(message_scores) >= 3:
            recent_avg = sum(message_scores[-3:]) / 3
            earlier_avg = sum(message_scores[:-3]) / len(message_scores[:-3]) if len(message_scores) > 3 else 0
            escalation_detected = recent_avg > earlier_avg + 0.2

        return {
            "escalation_detected": escalation_detected,
            "pattern_frequency": pattern_frequency,
            "message_scores": message_scores,
            "high_risk_patterns": [
                rule for rule, count in pattern_frequency.items()
                if count > 0 and self.rules[rule]["risk_level"] == RiskLevel.HIGH
            ]
        }

    def get_safety_suggestions(self, triggered_rules: List[str]) -> List[str]:
        """
        Provide safety suggestions based on triggered rules
        """
        suggestions = []

        rule_to_suggestion = {
            "age_probing": "Consider not sharing personal age information with strangers",
            "secrecy_enforcement": "Be cautious of anyone asking you to keep conversations secret",
            "isolation_tactics": "Healthy relationships don't require cutting off others",
            "gift_offers": "Never accept gifts from strangers online",
            "platform_migration": "Keep conversations on the original platform",
            "meeting_requests": "Never meet strangers from online in person",
            "personal_info_gathering": "Don't share personal information like address or school",
            "inappropriate_compliments": "Report inappropriate comments to platform moderators",
            "trust_building": "Take time to build trust naturally - be wary of instant 'best friends'"
        }

        for rule in triggered_rules:
            if rule in rule_to_suggestion:
                suggestions.append(rule_to_suggestion[rule])

        return suggestions