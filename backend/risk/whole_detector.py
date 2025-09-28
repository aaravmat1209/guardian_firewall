import os
import json
from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

class MessageData(BaseModel):
    username: str
    text: str
    timestamp: int

class MessageClassification(BaseModel):
    message: str
    conversation_context: List[str]
    llm_risk: str
    llm_confidence: float
    final_level: str
    final_score: float
    action: str
    explanations: List[str]

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

        # System prompt for message analysis with conversation context
        self._prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an AI threat detector for analyzing text messages sent to children in a game chatting feature.\n"
             "Return one of LOW|MEDIUM|HIGH as llm_risk based on the content of the message and a llm_confidence score from 0-1.\n"
             "LOW risk: Innocuous messages with no harmful content"
             "example: 'Hey, want to join my team for this quest?', 'Good game! That was fun.', 'Let's trade items later' are LOW risk.\n"
             "MEDIUM risk: Messages with mildly inappropriate content or suspicious/flattering language"
             "example: 'You are so mature', 'I like you', 'You are my best friend', 'Let's chat privately for a bit.' are MEDIUM risk.\n"
             "HIGH risk: Messages with explicit, harmful, or dangerous content like asking for personal info, meeting requests, gift or secrecy"
             "example: 'Hey, want to meet up sometime?', 'Can you send me a pic?', 'Don't tell anyone about this', 'Where do you live' are HIGH risk.\n"
             "ONLY CLASSIFY BASED ON THE CONTENT OF THE MESSAGE.\n\n"
             "Respond with format: RISK_LEVEL|confidence_score|brief_explanation\n"
             "Example: HIGH|0.89|User requesting personal information and suggesting meeting"),
            ("user", "Conversation context for reference:\n{conversation}\n\nClassify the following message: {current_message}")
        ])


    def _format_conversation_context(self, messages: List[MessageData]) -> str:
        """Format the last 50 messages into a readable conversation context"""
        if not messages:
            return "No previous conversation context."

        # Take last 50 messages
        recent_messages = messages[-50:] if len(messages) > 50 else messages

        formatted_lines = []
        for msg in recent_messages:
            timestamp_str = f"[{msg.timestamp}]" if hasattr(msg, 'timestamp') else ""
            formatted_lines.append(f"{timestamp_str} {msg.username}: {msg.text}")

        return "\n".join(formatted_lines)

    def _analyze_with_gemini(self, current_message: str, conversation_context: str) -> tuple:
        """Analyze message with Gemini LLM"""
        try:
            chain = self._prompt | self._llm
            response = chain.invoke({
                "conversation": conversation_context,
                "current_message": current_message
            })

            # Parse response: RISK_LEVEL|confidence_score|explanation
            parts = response.content.strip().split("|")
            if len(parts) >= 3:
                risk_level = parts[0].strip().upper()
                confidence = float(parts[1].strip())
                explanation = "|".join(parts[2:]).strip()

                # Validate risk level
                if risk_level not in ["LOW", "MEDIUM", "HIGH"]:
                    risk_level = "MEDIUM"

                return risk_level, confidence, explanation
            else:
                return "MEDIUM", 0.5, "Could not parse LLM response"

        except Exception as e:
            print(f"Gemini analysis error: {e}")
            return "MEDIUM", 0.5, f"LLM analysis failed: {str(e)}"


    def _calculate_final_risk(self, llm_risk: str, llm_confidence: float) -> tuple:
        """Calculate final risk level and score using only Gemini model"""

        # Convert LLM risk to numerical score
        llm_score_map = {"LOW": 0.2, "MEDIUM": 0.5, "HIGH": 0.8}
        llm_score = llm_score_map.get(llm_risk, 0.5)

        # Use LLM confidence as the final score
        final_score = llm_score * llm_confidence

        # Determine final level based on confidence-weighted score
        if final_score >= 0.6:
            final_level = "HIGH"
        elif final_score >= 0.3:
            final_level = "MEDIUM"
        else:
            final_level = "LOW"

        return final_level, final_score

    def analyze_message(self, current_message: str, conversation_history: List[Dict[str, Any]] = None) -> MessageClassification:
        """
        Analyze a message with sliding window of conversation context

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

        # Format conversation context
        conversation_context = self._format_conversation_context(messages)

        # Analyze with Gemini
        llm_risk, llm_confidence, llm_explanation = self._analyze_with_gemini(
            current_message, conversation_context
        )

        # Calculate final risk using only Gemini
        final_level, final_score = self._calculate_final_risk(
            llm_risk, llm_confidence
        )

        # Generate explanations
        explanations = [llm_explanation]

        # Determine action
        action_map = {
            "LOW": "allow",
            "MEDIUM": "flag",
            "HIGH": "block"
        }
        action = action_map.get(final_level, "flag")

        return MessageClassification(
            message=current_message,
            conversation_context=[msg.text for msg in messages[-10:]],  # Last 10 for summary
            llm_risk=llm_risk,
            llm_confidence=llm_confidence,
            final_level=final_level,
            final_score=final_score,
            action=action,
            explanations=explanations
        )

# Global detector instance
_detector = None

def get_detector() -> GuardianDetector:
    """Get or create the global detector instance"""
    global _detector
    if _detector is None:
        _detector = GuardianDetector()
    return _detector