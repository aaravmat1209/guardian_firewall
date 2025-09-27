import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from transformers import pipeline
from pydantic import BaseModel
from dotenv import load_dotenv

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
HUGGINGFACE_MODEL = "michellejieli/NSFW_text_classifier"

class MessageClassification(BaseModel):
    message: str
    llm_risk: str
    llm_confidence: float
    hf_score: float
    final_level: str
    action: str

'''----------------gemini setup and prompting----------------'''
_llm = ChatGoogleGenerativeAI(
    temperature=0, 
    model="gemini-2.5-flash", 
    api_key=GEMINI_API_KEY)

_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an AI threat detector for analyzing text messages sent to children in a game chatting feature.\n"
     "Return one of LOW|MEDIUM|HIGH risk levels based on the content of the message and a llm_confidence score from 0-1.\n"
     "LOW risk: Innocuous messages with no harmful content"
     "example: 'Hey, want to join my team for this quest?', 'Good game! That was fun.', 'Let's trade items later' are LOW risk.\n"
     "MEDIUM risk: Messages with mild inappropriate content or suggestive language"
     "example: 'You are so mature', 'I like you', 'You are my best friend' are MEDIUM risk.\n"
     "HIGH risk: Messages with explicit, harmful, or dangerous content like asking for personal info, meeting requests, gift or secrecy"
     "example: 'Hey, want to meet up sometime?', 'Can you send me a pic?', 'Don't tell anyone about this', 'Where do you live' are HIGH risk.\n"
)])




_hf_classifier = pipeline(
    "text-classification", 
    model=HUGGINGFACE_MODEL, 
    device = -1)

