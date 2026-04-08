from sqlalchemy import Column ,String , Integer , Text , Float , DateTime
from database.db import Base
from datetime import datetime

class Review(Base):
    __tablename__ = "reviews"

    id =Column(Integer , primary_key=True , index=True)
    review_text = Column(Text , nullable =False)
    prediction = Column(String , nullable=False)
    confidence = Column(Float , nullable=False)
    explanation = Column(Text)
    created_at = Column(DateTime , default=datetime.utcnow)


class FlaggedReview(Base):
    __tablename__="flagged_reviews"

    id = Column(Integer , primary_key=True , index=True)
    review_text = Column(Text , nullable=False)
    reason = Column(Text)
    confidence = Column(Float)
    created_at = Column(DateTime , default=datetime.utcnow)