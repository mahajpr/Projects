from pydantic import BaseModel
from typing import List 

class ReviewInput(BaseModel):
    review:str

class ReviewAnalysis(BaseModel):
    prediction:str
    confidence:float
    explanation:str
    suspicious_phrases:List[str]
    similar_reviews:List[str]