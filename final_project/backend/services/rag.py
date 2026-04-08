from sqlalchemy.orm import Session
from sqlalchemy import text
from dotenv import load_dotenv
from groq import Groq
import re
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_explain(review, suspicious_phrases):

    if not suspicious_phrases:
        return "No suspicious patterns detected."
        
    phrases = []

    for item in suspicious_phrases:
        if isinstance(item, dict):
            phrases.append(item.get("text", ""))
        else:
            phrases.append(str(item))

    joined = ", ".join(phrases)
 
    return  "This review appears suspicious due to the following signals: "+ joined
    
def analyze_review_pipeline(review: str):
    suspicious = []

    if "free" in review.lower():
        suspicious.append("Mentions free product")

    if "discount" in review.lower():
        suspicious.append("Mentions discount")

    if review.count("!") > 3:
        suspicious.append("Too many exclamation marks")

    prediction = "Fake" if len(suspicious) >= 1 else "Genuine"
    confidence = min(0.95, 0.5 + 0.2 * len(suspicious))

    return {
        "prediction": prediction,
        "confidence": confidence,
        "suspicious_phrases": suspicious
    }

