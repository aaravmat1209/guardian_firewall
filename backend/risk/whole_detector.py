import os
import json
from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from . import keyword_fallback
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
            model="gemini-2.5-pro",
            api_key=GEMINI_API_KEY
        )

        # System prompt for message analysis with conversation context
        self._prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an expert AI safety system analyzing chat messages sent to children in gaming platforms.\n\n"
     
             "GROOMING BEHAVIOR PATTERNS TO RECOGNIZE:\n"
             "• Trust building: excessive compliments, 'you're mature', 'special connection'\n"
             "• Isolation: 'just between us', 'don't tell parents', 'our secret'\n"
             "• Information gathering: asking location, school, personal details, photos\n"
             "• Relationship escalation: 'meet in person', gift offers, 'come over'\n"
             "• Boundary testing: inappropriate topics, sexual content, rule breaking\n\n"
     
             "CONVERSATION CONTEXT ANALYSIS:\n"
             "Consider how the conversation has progressed:\n"
             "• Is this the first concerning message or part of a pattern?\n"
             "• Has the sender been building trust before making requests?\n"
             "• Are messages escalating in intimacy or risk level?\n\n"
     
             "RISK LEVELS:\n"
             "LOW: Normal gaming chat, friendly conversation, appropriate requests\n"
             "MEDIUM: Mildly inappropriate, boundary-testing, suspicious but not dangerous\n"  
             "HIGH: Clear grooming indicators, personal info requests, meeting suggestions, secrecy requests\n\n"
     
             "RESPONSE FORMAT:\n"
             "RISK_LEVEL|confidence_score|detailed_explanation_with_reasoning, Explanation should be no more than 15 words.\n\n"
     
             "Example: HIGH|0.92|Message requests personal meeting and asks for secrecy, matching classic grooming escalation pattern"),
            ("user", "Previous conversation:\n{conversation}\n\nAnalyze this new message: \"{current_message}\"")
        ])

        self.initial_context_size = 15
        self.expanded_context_size = 35  # 15 more messages
        self.enable_adaptive_context = True




    def _format_conversation_context(self, messages: List[MessageData]) -> str:
        if not messages:
            return "No previous conversation context."

        recent_messages = messages[-15:] if len(messages) > 15 else messages

        formatted_lines = []
        for i, msg in enumerate(recent_messages):
            position = f"Message {i+1}"
            formatted_lines.append(f"{position} - {msg.username}: {msg.text}")

        return "\n".join(formatted_lines)


    def _analyze_with_gemini(self, current_message: str, conversation_context: str, prompt: ChatPromptTemplate = None) -> tuple:
        try:
            chain_prompt = prompt if prompt is not None else self._prompt
            chain = chain_prompt | self._llm
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
                    print(f"Invalid risk level from Gemini: {risk_level}, using fallback")
                    return keyword_fallback.analyze_message(current_message)

                return risk_level, confidence, explanation
            else:
                print(f"Could not parse response: {response.content}")
                return keyword_fallback.analyze_message(current_message)
            
        except Exception as e:
            print(f"Gemini analysis error: {e}")
            # Fallback to keyword analysis on error
            fallback_risk, fallback_confidence, fallback_explanation = keyword_fallback.analyze_message(current_message)
            
            return fallback_risk, fallback_confidence, f"AI unavailable - {fallback_explanation} (Error: {str(e)})"

    def _analyze_with_adaptive_context(self, current_message: str, messages: List[MessageData], suppress_explanations: bool = False) -> tuple:
        """
        Analyze message with adaptive context expansion.
        If initial analysis shows risk, expand context for deeper analysis.
        """
        # Step 1: Initial analysis with standard context
        initial_context = self._format_conversation_context(messages[-self.initial_context_size:])
        initial_risk, initial_confidence, initial_explanation = self._analyze_with_gemini(
            current_message, initial_context
        )

        # Step 2: Expand if needed
        if (self.enable_adaptive_context and
            initial_risk in ["MEDIUM", "HIGH"] and
            len(messages) > self.initial_context_size):

            print(f"Initial risk: {initial_risk} - Expanding context for deeper analysis")

            expanded_context = self._format_conversation_context(messages[-self.expanded_context_size:])

            deeper_prompt = ChatPromptTemplate.from_messages([
                ("system",
                "You are conducting a DEEPER ANALYSIS of a potentially concerning conversation.\n\n"
                "INITIAL ASSESSMENT indicated {initial_risk} risk with {initial_confidence:.1%} confidence.\n"
                "INITIAL REASONING: {initial_explanation}\n\n"
                "Now analyze the FULL conversation context to:\n"
                "• Confirm or adjust the risk assessment\n"
                "• Look for grooming escalation patterns over time\n"
                "• Identify relationship building → boundary testing → risk escalation\n"
                "• Consider if this is an isolated incident or part of a concerning pattern\n\n"
                "RESPONSE FORMAT:\n"
                "RISK_LEVEL|confidence_score|detailed_timeline_analysis"),
                ("user",
                "FULL CONVERSATION HISTORY:\n{conversation}\n\n"
                "CURRENT MESSAGE TO ANALYZE: \"{message}\"")
            ])

            deeper_risk, deeper_confidence, deeper_explanation = self._analyze_with_gemini(
                current_message,
                expanded_context,
                prompt=deeper_prompt
            )

            analysis_type = f"Gemini AI (Expanded Context - {len(messages)} msgs)"
            if suppress_explanations:
                combined_explanation = ""  # **suppress intermediate explanation**
            else:
                combined_explanation = (
                    f"INITIAL: {initial_explanation} | "
                    f"DEEPER ANALYSIS: {deeper_explanation}"
                )
            print(f"Deeper analysis result: {deeper_risk} (was {initial_risk})")
            return deeper_risk, deeper_confidence, f"{analysis_type}: {combined_explanation}"
        
        # Normal return
        if suppress_explanations:
            explanation = ""
        else:
            explanation = initial_explanation

        return initial_risk, initial_confidence, explanation


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

        # Analyze with Gemini
        llm_risk, llm_confidence, llm_explanation = self._analyze_with_adaptive_context(
            current_message, messages
        )

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
    
    def get_system_stats(self) -> dict:
        """Get statistics about the detection system"""
        keyword_stats = keyword_fallback.get_keyword_stats()
        
        return {
            "ai_model": "gemini-2.5-pro",
            "fallback_system": "comprehensive_keywords",
            "keyword_patterns": keyword_stats["total_keywords"],
            "protection_categories": len(keyword_stats["categories"]),
            "system_status": "active"
        }

# Global detector instance
_detector = None

def get_detector() -> GuardianDetector:
    """Get or create the global detector instance"""
    global _detector
    if _detector is None:
        _detector = GuardianDetector()
    return _detector