import os
import json
import re
from typing import List, Dict, Any, Tuple
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from dotenv import load_dotenv
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

class MessageData(BaseModel):
    username: str
    text: str
    timestamp: int

class ThreatPattern(BaseModel):
    name: str
    severity: str  # "low", "medium", "high"
    confidence: float
    detected_in_message: bool

class MessageClassification(BaseModel):
    message: str
    conversation_context: List[str]
    llm_risk: str
    llm_confidence: float
    final_level: str
    final_score: float
    action: str
    explanations: List[str]
    patterns: List[ThreatPattern]
    conversation_risk_trend: str  # "stable", "escalating", "de-escalating"

class GuardianDetector:
    def __init__(self):
        """Initialize the Guardian threat detector with Gemini and Hugging Face models"""

        # Initialize Gemini LLM
        if not GEMINI_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")

        self._llm = ChatGoogleGenerativeAI(
            temperature=0,
            model="gemini-2.5-flash",
            api_key=GEMINI_API_KEY
        )

        # Initialize Hugging Face models for enhanced detection
        self._init_huggingface_models()

        # Define comprehensive threat patterns
        self._threat_patterns = self._init_threat_patterns()

        # System prompt for message analysis with conversation context
        self._prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an AI threat detector for analyzing text messages sent to children in a game chatting feature.\n"
             "Return a risk score from 0.0-1.0 and classification as llm_risk based on the content of the message.\n"
             "Provide granular scoring within categories:\n"
             "LOW risk (0.0-0.3): Innocuous gaming messages\n"
             "- 0.05-0.10: Pure gaming ('Nice shot!', 'Good game!', 'Let's play')\n"
             "- 0.10-0.20: Friendly gaming chat ('You're good at this', 'Want to team up?')\n"
             "- 0.20-0.30: Slightly personal but innocent ('That was fun', 'You seem cool')\n"
             "MEDIUM risk (0.3-0.6): Mildly inappropriate or suspicious content\n"
             "- 0.30-0.45: Flattering language ('You're so mature', 'You're different')\n"
             "- 0.45-0.60: Boundary testing ('Let's chat privately', 'You can trust me')\n"
             "HIGH risk (0.6-1.0): Dangerous content requiring intervention\n"
             "- 0.60-0.80: Personal info requests ('How old are you?', 'Where do you live?')\n"
             "- 0.80-1.0: Serious threats ('Meet me', 'Send pics', 'Keep this secret')\n\n"
             "Respond with format: SCORE|CLASSIFICATION|brief_explanation\n"
             "Example: 0.85|HIGH|User requesting personal information and suggesting meeting"),
            ("user", "Conversation context for reference:\n{conversation}\n\nClassify the following message: {current_message}")
        ])

    def _init_huggingface_models(self):
        """Initialize Hugging Face models for enhanced threat detection"""
        try:
            # Initialize sentiment analysis for emotional manipulation detection
            self._sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True,
                use_safetensors=True
            )

            # Initialize toxicity detection model
            self._toxicity_analyzer = pipeline(
                "text-classification",
                model="unitary/toxic-bert",
                return_all_scores=True,
                use_safetensors=True
            )

            # Initialize NSFW content detection
            self._nsfw_analyzer = pipeline(
                "text-classification",
                model="michellejieli/NSFW_text_classifier",
                return_all_scores=True,
                use_safetensors=True
            )

            print("✅ Hugging Face models initialized successfully")
        except Exception as e:
            print(f"⚠️ Warning: Some Hugging Face models failed to load: {e}")
            print("Falling back to rule-based pattern detection only")
            # Fallback: simple rule-based detection
            self._sentiment_analyzer = None
            self._toxicity_analyzer = None
            self._nsfw_analyzer = None

    def _init_threat_patterns(self) -> Dict[str, Dict]:
        """Initialize comprehensive threat pattern definitions like the demo"""
        return {
            "age_inquiry": {
                "patterns": [
                    r"\bhow old are you\b", r"\bwhat.*age\b", r"\byour age\b",
                    r"\bage.*you\b", r"\bold.*you\b", r"\byoung.*you\b",
                    r"\bgrade.*you\b", r"\bschool.*grade\b"
                ],
                "severity": "medium",
                "name": "Age inquiry"
            },
            "personal_info": {
                "patterns": [
                    r"\bwhere.*live\b", r"\byour.*address\b", r"\bphone.*number\b",
                    r"\breal.*name\b", r"\bfull.*name\b", r"\blast.*name\b",
                    r"\bschool.*name\b", r"\bwhere.*go.*school\b"
                ],
                "severity": "high",
                "name": "Personal info request"
            },
            "external_platform": {
                "patterns": [
                    r"\bdiscord\b", r"\bsnap.*chat\b", r"\binstagram\b", r"\btiktok\b",
                    r"\bwhatsapp\b", r"\btelegram\b", r"\bskype\b", r"\bzoom\b",
                    r"\bmeet.*private\b", r"\bprivate.*chat\b"
                ],
                "severity": "high",
                "name": "External platform"
            },
            "secrecy_request": {
                "patterns": [
                    r"\bdon't tell\b", r"\bkeep.*secret\b", r"\bsecret.*between\b",
                    r"\bdon't.*parents\b", r"\bour.*secret\b", r"\bhide.*this\b",
                    r"\bdelete.*message\b", r"\bdon't.*anyone\b"
                ],
                "severity": "high",
                "name": "Secrecy request"
            },
            "image_request": {
                "patterns": [
                    r"\bsend.*pic\b", r"\bsend.*photo\b", r"\byour.*picture\b",
                    r"\bshow.*yourself\b", r"\bselfie\b", r"\bimage.*you\b",
                    r"\bpic.*you\b", r"\bphoto.*you\b"
                ],
                "severity": "high",
                "name": "Image request"
            },
            "meeting_request": {
                "patterns": [
                    r"\bmeet.*up\b", r"\bmeet.*person\b", r"\bmeet.*real\b",
                    r"\bcome.*house\b", r"\bvisit.*me\b", r"\bhang.*out\b",
                    r"\bmeet.*somewhere\b", r"\bin.*person\b"
                ],
                "severity": "high",
                "name": "Meeting request"
            },
            "grooming_language": {
                "patterns": [
                    r"\bspecial.*friend\b", r"\bmature.*age\b", r"\bold.*soul\b",
                    r"\bdifferent.*others\b", r"\bunderstand.*you\b", r"\btrust.*me\b",
                    r"\bbest.*friend\b", r"\bclose.*friend\b"
                ],
                "severity": "medium",
                "name": "Grooming language"
            },
            "gift_promises": {
                "patterns": [
                    r"\bbuy.*you\b", r"\bgift.*you\b", r"\bgive.*money\b",
                    r"\bpresent.*you\b", r"\breward.*you\b", r"\bpay.*you\b"
                ],
                "severity": "medium",
                "name": "Gift promises"
            }
        }


    def _format_conversation_context(self, messages: List[MessageData], context_size: int = 15) -> str:
        """Format conversation messages into a readable context with dynamic sizing"""
        if not messages:
            return "No previous conversation context."

        # Take the specified number of recent messages
        recent_messages = messages[-context_size:] if len(messages) > context_size else messages

        formatted_lines = []
        for msg in recent_messages:
            timestamp_str = f"[{msg.timestamp}]" if hasattr(msg, 'timestamp') else ""
            formatted_lines.append(f"{timestamp_str} {msg.username}: {msg.text}")

        return "\n".join(formatted_lines)

    def _detect_patterns(self, message: str, conversation_history: List[MessageData]) -> List[ThreatPattern]:
        """Detect comprehensive threat patterns in message and conversation"""
        detected_patterns = []
        message_lower = message.lower()

        # Rule-based pattern detection
        for pattern_id, pattern_data in self._threat_patterns.items():
            confidence = 0.0
            detected_in_current = False

            # Check current message
            for regex_pattern in pattern_data["patterns"]:
                if re.search(regex_pattern, message_lower, re.IGNORECASE):
                    confidence += 0.4
                    detected_in_current = True

            # Check conversation history for escalating patterns
            if conversation_history:
                recent_messages = conversation_history[-5:]  # Last 5 messages
                for msg in recent_messages:
                    msg_lower = msg.text.lower()
                    for regex_pattern in pattern_data["patterns"]:
                        if re.search(regex_pattern, msg_lower, re.IGNORECASE):
                            confidence += 0.1

            # Hugging Face model enhancements
            if self._toxicity_analyzer and pattern_id in ["secrecy_request", "personal_info"]:
                try:
                    toxicity_result = self._toxicity_analyzer(message)[0]
                    if toxicity_result['label'] == 'TOXIC' and toxicity_result['score'] > 0.7:
                        confidence += 0.2
                except Exception:
                    pass

            if self._nsfw_analyzer and pattern_id in ["image_request", "meeting_request"]:
                try:
                    nsfw_result = self._nsfw_analyzer(message)[0]
                    if nsfw_result['label'] == 'NSFW' and nsfw_result['score'] > 0.6:
                        confidence += 0.3
                except Exception:
                    pass

            # If pattern detected with sufficient confidence
            if confidence >= 0.3:
                detected_patterns.append(ThreatPattern(
                    name=pattern_data["name"],
                    severity=pattern_data["severity"],
                    confidence=min(confidence, 1.0),
                    detected_in_message=detected_in_current
                ))

        return detected_patterns

    def _analyze_conversation_trend(self, conversation_history: List[MessageData], current_patterns: List[ThreatPattern]) -> str:
        """Analyze if conversation risk is escalating over time"""
        if len(conversation_history) < 3:
            return "stable"

        # Analyze recent message patterns vs earlier ones
        recent_messages = conversation_history[-3:]
        earlier_messages = conversation_history[:-3][-3:] if len(conversation_history) > 3 else []

        recent_risk_score = 0
        earlier_risk_score = 0

        # Calculate risk scores for message segments
        for msg in recent_messages:
            recent_patterns = self._detect_patterns(msg.text, [])
            recent_risk_score += sum(p.confidence for p in recent_patterns)

        for msg in earlier_messages:
            earlier_patterns = self._detect_patterns(msg.text, [])
            earlier_risk_score += sum(p.confidence for p in earlier_patterns)

        # Add current message patterns
        current_risk = sum(p.confidence for p in current_patterns)
        recent_risk_score += current_risk

        # Determine trend
        if recent_risk_score > earlier_risk_score * 1.5:
            return "escalating"
        elif recent_risk_score < earlier_risk_score * 0.7:
            return "de-escalating"
        else:
            return "stable"

    def _analyze_with_gemini(self, current_message: str, conversation_context: str) -> tuple:
        """Analyze message with Gemini LLM using granular scoring"""
        try:
            chain = self._prompt | self._llm
            response = chain.invoke({
                "conversation": conversation_context,
                "current_message": current_message
            })

            # Parse response: SCORE|CLASSIFICATION|explanation
            parts = response.content.strip().split("|")
            if len(parts) >= 3:
                score = float(parts[0].strip())
                classification = parts[1].strip().upper()
                explanation = "|".join(parts[2:]).strip()

                # Validate score range
                score = max(0.0, min(1.0, score))

                # Ensure classification matches score
                if score <= 0.3:
                    classification = "LOW"
                elif score <= 0.6:
                    classification = "MEDIUM"
                else:
                    classification = "HIGH"

                return classification, score, explanation
            else:
                return "MEDIUM", 0.5, "Could not parse LLM response"

        except Exception as e:
            print(f"Gemini analysis error: {e}")
            return "MEDIUM", 0.5, f"LLM analysis failed: {str(e)}"


    def _calculate_final_risk(self, llm_risk: str, llm_score: float, patterns: List[ThreatPattern], conversation_trend: str) -> tuple:
        """Calculate final risk level and score using Gemini + patterns + HF models"""

        # Use Gemini's granular score directly as base score
        base_score = llm_score

        # Pattern-based score enhancement
        pattern_boost = 0.0
        high_severity_patterns = [p for p in patterns if p.severity == "high"]
        medium_severity_patterns = [p for p in patterns if p.severity == "medium"]

        # High severity patterns significantly boost risk
        pattern_boost += len(high_severity_patterns) * 0.15
        pattern_boost += len(medium_severity_patterns) * 0.08

        # Multiple patterns create multiplicative risk
        if len(patterns) >= 3:
            pattern_boost *= 1.3
        elif len(patterns) >= 2:
            pattern_boost *= 1.15

        # Conversation trend affects final score
        trend_multiplier = 1.0
        if conversation_trend == "escalating":
            trend_multiplier = 1.2
        elif conversation_trend == "de-escalating":
            trend_multiplier = 0.9

        # Calculate final score
        final_score = (base_score + pattern_boost) * trend_multiplier
        final_score = min(final_score, 1.0)  # Cap at 1.0

        # Determine final level with enhanced thresholds
        if final_score >= 0.65 or len(high_severity_patterns) >= 2:
            final_level = "HIGH"
        elif final_score >= 0.35 or len(patterns) >= 2:
            final_level = "MEDIUM"
        else:
            final_level = "LOW"

        return final_level, final_score

    def analyze_message(self, current_message: str, conversation_history: List[Dict[str, Any]] = None) -> MessageClassification:
        """
        Analyze a message with dynamic conversation context based on risk level

        Args:
            current_message: The latest message to analyze
            conversation_history: List of previous messages with format [{"username": str, "text": str, "timestamp": int}]

        Returns:
            MessageClassification with risk assessment
        """

        # Convert conversation history to MessageData objects
        messages = []
        if conversation_history:
            for msg in conversation_history:
                try:
                    messages.append(MessageData(
                        username=msg.get("username", "Unknown"),
                        text=msg.get("text", ""),
                        timestamp=msg.get("timestamp", 0)
                    ))
                except Exception:
                    continue

        # Start with default context size of 15
        initial_context_size = 15
        conversation_context = self._format_conversation_context(messages, initial_context_size)

        # Detect comprehensive threat patterns
        patterns = self._detect_patterns(current_message, messages)

        # Analyze conversation trend
        conversation_trend = self._analyze_conversation_trend(messages, patterns)

        # Analyze with Gemini
        llm_risk, llm_score, llm_explanation = self._analyze_with_gemini(
            current_message, conversation_context
        )

        # If high risk detected or multiple patterns, expand context and re-analyze
        if (llm_risk == "HIGH" or len(patterns) >= 2) and len(messages) > initial_context_size:
            # Expand to 50 messages for deeper context analysis
            expanded_context_size = min(50, len(messages))
            expanded_conversation_context = self._format_conversation_context(messages, expanded_context_size)

            # Re-analyze with expanded context
            llm_risk, llm_score, llm_explanation = self._analyze_with_gemini(
                current_message, expanded_conversation_context
            )

            # Re-detect patterns with expanded context
            patterns = self._detect_patterns(current_message, messages[-expanded_context_size:])

            # Add note about expanded analysis
            llm_explanation += " (Analyzed with expanded conversation history due to high risk/pattern detection)"

        # Calculate final risk using Gemini + patterns + conversation trend
        final_level, final_score = self._calculate_final_risk(
            llm_risk, llm_score, patterns, conversation_trend
        )

        # Generate comprehensive explanations
        explanations = [llm_explanation]

        # Add pattern explanations
        for pattern in patterns:
            explanations.append(f"{pattern.name} detected (confidence: {pattern.confidence:.2f})")

        # Add trend analysis
        if conversation_trend != "stable":
            explanations.append(f"Conversation risk is {conversation_trend}")

        # Determine action
        action_map = {
            "LOW": "allow",
            "MEDIUM": "flag",
            "HIGH": "block"
        }
        action = action_map.get(final_level, "flag")

        # Return summary context (last 10 messages)
        summary_context_size = min(10, len(messages))
        summary_context = [msg.text for msg in messages[-summary_context_size:]]

        return MessageClassification(
            message=current_message,
            conversation_context=summary_context,
            llm_risk=llm_risk,
            llm_confidence=llm_score,
            final_level=final_level,
            final_score=final_score,
            action=action,
            explanations=explanations,
            patterns=patterns,
            conversation_risk_trend=conversation_trend
        )

# Global detector instance
_detector = None

def get_detector() -> GuardianDetector:
    """Get or create the global detector instance"""
    global _detector
    if _detector is None:
        _detector = GuardianDetector()
    return _detector