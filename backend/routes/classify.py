from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from risk.whole_detector import get_detector

router = APIRouter(prefix="/classify", tags=["classification"])

class ConversationMessage(BaseModel):
    username: Optional[str] = "Unknown"
    text: str
    timestamp: Optional[int] = 0

class MessageRequest(BaseModel):
    text: str
    conversation_history: Optional[List[ConversationMessage]] = []
    user_id: Optional[str] = None

class ClassificationResponse(BaseModel):
    risk_level: str
    confidence_score: float
    explanations: List[str]
    action: str
    should_pause: bool
    llm_confidence: float

class ConversationResponse(BaseModel):
    risk_level: str
    trend: str
    scores: List[float]
    messages: List[ClassificationResponse]

class ConversationRequest(BaseModel):
    messages: List[ConversationMessage]

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
            llm_confidence=result.llm_confidence
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")
    

@router.post("/conversation", response_model=ConversationResponse)
async def classify_conversation(request: ConversationRequest):
    messages = request.messages
    if not messages:
        return ConversationResponse(
            risk_level="low",
            trend="stable",
            conversation_length=0,
            messages=[]
        )

    classified_messages = []
    recent_scores = []

    for i, msg in enumerate(messages):
        history_texts = [m.text for m in messages[:i]]  # conversation context so far
        result = guardian_detector.analyze_message(msg.text, history_texts)

        classified_messages.append(
            ClassificationResponse(
                text=msg.text,
                risk_level=result.final_level.lower(),
                confidence_score=result.final_score,
                explanations=result.explanations,
                action=result.action,
                should_pause=result.final_level in ["MEDIUM", "HIGH"],
                llm_confidence=result.llm_confidence
            )
        )

        recent_scores.append(result.final_score)

    # Determine trend
    trend = "stable"
    if len(recent_scores) > 1:
        trend = "escalating" if recent_scores[-1] > recent_scores[0] else "stable"

    # Determine overall conversation level
    max_risk = max(recent_scores)
    if max_risk > 0.7:
        overall_level = "high"
    elif max_risk > 0.4:
        overall_level = "medium"
    else:
        overall_level = "low"

    return ConversationResponse(
        risk_level=overall_level,
        trend=trend,
        conversation_length=len(messages),
        messages=classified_messages,
        scores=recent_scores
    )
