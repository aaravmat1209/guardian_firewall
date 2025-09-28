from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from risk.whole_detector import get_detector

router = APIRouter(prefix="/classify", tags=["classification"])

class MessageRequest(BaseModel):
    text: str
    conversation_history: Optional[List[dict]] = []
    user_id: Optional[str] = None

class ClassificationResponse(BaseModel):
    risk_level: str
    confidence_score: float
    explanations: List[str]
    action: str
    should_pause: bool
    llm_confidence: float
    patterns: List[dict] = []
    conversation_risk_trend: str = "stable"

guardian_detector = get_detector()

@router.post("/message", response_model=ClassificationResponse)
async def classify_message(request: MessageRequest):
    """
    Classify a single message for grooming risk
    """
    try:
        result = guardian_detector.analyze_message(
            request.text,
            request.conversation_history
        )

        return ClassificationResponse(
            risk_level=result.final_level.lower(),
            confidence_score=result.final_score,
            explanations=result.explanations,
            action=result.action,
            should_pause=result.final_level in ["MEDIUM", "HIGH"],
            llm_confidence=result.llm_confidence,
            patterns=[{
                "name": pattern.name,
                "severity": pattern.severity,
                "confidence": pattern.confidence
            } for pattern in result.patterns],
            conversation_risk_trend=result.conversation_risk_trend
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@router.post("/conversation")
async def classify_conversation(messages: List[dict]):
    """
    Analyze an entire conversation for escalating risk patterns
    """
    try:
        # Analyze the full conversation context
        if not messages:
            return {"risk_level": "low", "trend": "stable"}

        # Analyze the last message with full conversation context
        last_message = messages[-1].get("text", "")
        result = guardian_detector.analyze_message(last_message, messages[:-1])

        recent_scores = [result.final_score]

        # Determine trend
        if len(recent_scores) > 1:
            trend = "escalating" if recent_scores[-1] > recent_scores[0] else "stable"
        else:
            trend = "stable"

        max_risk = max(recent_scores) if recent_scores else 0

        if max_risk > 0.7:
            level = "high"
        elif max_risk > 0.4:
            level = "medium"
        else:
            level = "low"

        return {
            "risk_level": level,
            "trend": trend,
            "scores": recent_scores,
            "conversation_length": len(messages)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversation analysis failed: {str(e)}")