from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from risk.fuse import RiskFusion

router = APIRouter(prefix="/classify", tags=["classification"])

class MessageRequest(BaseModel):
    text: str
    conversation_history: Optional[List[dict]] = []
    user_id: Optional[str] = None

class ClassificationResponse(BaseModel):
    risk_level: str
    confidence_score: float
    explanations: List[str]
    suggestions: List[str]
    should_pause: bool

risk_fusion = RiskFusion()

@router.post("/message", response_model=ClassificationResponse)
async def classify_message(request: MessageRequest):
    """
    Classify a single message for grooming risk
    """
    try:
        result = risk_fusion.analyze_message(
            request.text,
            request.conversation_history
        )

        return ClassificationResponse(
            risk_level=result["level"],
            confidence_score=result["score"],
            explanations=result["explanations"],
            suggestions=result.get("suggestions", []),
            should_pause=result["level"] in ["medium", "high"]
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

        # Get risk scores for recent messages
        recent_scores = []
        for i, msg in enumerate(messages[-10:]):  # Last 10 messages
            history = messages[:len(messages)-10+i] if i > 0 else []
            result = risk_fusion.analyze_message(msg.get("text", ""), history)
            recent_scores.append(result["score"])

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