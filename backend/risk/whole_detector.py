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
     "Return one of LOW|MEDIUM|HIGH as llm_risk based on the content of the message and a llm_confidence score from 0-1.\n"
     "LOW risk: Innocuous messages with no harmful content"
     "example: 'Hey, want to join my team for this quest?', 'Good game! That was fun.', 'Let's trade items later' are LOW risk.\n"
     "MEDIUM risk: Messages with mildly inappropriate content or suspicious/flattering language"
     "example: 'You are so mature', 'I like you', 'You are my best friend', 'Let\'s chat privately for a bit.' are MEDIUM risk.\n"
     "HIGH risk: Messages with explicit, harmful, or dangerous content like asking for personal info, meeting requests, gift or secrecy"
     "example: 'Hey, want to meet up sometime?', 'Can you send me a pic?', 'Don't tell anyone about this', 'Where do you live' are HIGH risk.\n"
     "ONLY CLASSIFY BASED ON THE CONTENT OF THE MESSAEGE."),
     ("Human", "Classify the following message: {message}")
])


from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
import os

load_dotenv()  # Make sure GOOGLE_API_KEY is loaded

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

class MessageClassification(BaseModel):
    message: str
    llm_risk: str
    llm_confidence: float
    hf_score: float
    final_level: str
    action: str

# ---------------- Gemini setup ----------------
_llm = ChatGoogleGenerativeAI(
    temperature=0, 
    model="gemini-2.5-flash", 
    api_key=GEMINI_API_KEY
)

_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an AI threat detector for analyzing text messages sent to children in a game chatting feature.\n"
     "Return one of LOW|MEDIUM|HIGH as llm_risk based on the content of the message and a llm_confidence score from 0-1."),
    ("human", "Classify the following message: {message}")
])

# ---------------- Test messages ----------------
test_messages = [
    "Hey, want to join my team for this quest?",
    "Good game! That was fun.",
    "Do you have the new sword item?",
    "Let's trade items later.",
    "Can you help me complete this mission?",
    "You’re really good at this game!",
    "I like your avatar, it looks cool.",
    "You’re so mature for your age.",
    "I think we should chat privately for a bit.",
    "Do you want some tips? Don’t tell others.",
    "Hey, how old are you?",
    "Where do you live?",
    "Send me your phone number so we can chat on WhatsApp.",
    "I can give you Robux if you meet me in person.",
    "Don’t tell anyone, this is our secret.",
    "Come to my house and I’ll show you something cool.",
    "Can you send me a pic?",
    "I have a rare item I can trade if you’re careful.",
    "You are my best friend, right?",
    "Let’s meet at the central plaza in the game.",
    "I can help you level up faster if you follow me.",
    "What school do you go to?",
    "Can I see your profile picture?",
    "Do you want to team up for the next event?",
    "Let’s chat on Discord later."
]

'''---------------- classification ----------------'''
response = _llm.invoke(_prompt.format_messages(message=test_messages))

# Print the raw response from Gemini
print(response.content)


