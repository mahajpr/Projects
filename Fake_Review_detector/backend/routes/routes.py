from database.deps import get_db
from sqlalchemy.orm import Session
from models.pydantic import  ReviewInput , ReviewAnalysis
from fastapi import APIRouter , Depends
from services.rag import generate_explain , analyze_review_pipeline
from services.data import get_rag_context
from sqlalchemy import func
from datetime import datetime
from models.tables import Review, FlaggedReview


router = APIRouter()

@router.post("/analyze", response_model=ReviewAnalysis)
def analyze_review(data: ReviewInput, db: Session = Depends(get_db)):

    result = analyze_review_pipeline(data.review)

    context = get_rag_context(data.review)

    explanation = generate_explain(data.review, context)

    review_db = Review(
        review_text = data.review,
        prediction = result["prediction"],
        confidence=result["confidence"],
        explanation =explanation
    )
    db.add(review_db)
    db.commit()

    if result["prediction"]=="Fake":
        flagged =FlaggedReview(
            review_text=data.review,
            reason ="suspicious language",
            confidence = result["confidence"]
        )
        db.add(flagged)
        db.commit()

    return ReviewAnalysis(
        prediction=result["prediction"],
        confidence=result["confidence"],
        explanation=explanation,
        suspicious_phrases=result["suspicious_phrases"],
        similar_reviews=[c["text"] for c in context[:2]]
    )

@router.get("/reviews")
def get_all_reviews(db:Session = Depends(get_db)):
    return db.query(Review).all()

@router.get("/flagged")
def get_flagged_reviews(db:Session = Depends(get_db)):
    return db.query(FlaggedReview).all()


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    total_reviews = db.query(func.count(Review.id)).scalar()

    detected_fake = (
        db.query(func.count(Review.id))
        .filter(Review.prediction == "Fake")
        .scalar()
    )

    flagged_reviews = db.query(func.count(FlaggedReview.id)).scalar()

    now = datetime.utcnow()
    month_reviews = (
        db.query(func.count(Review.id))
        .filter(
            func.strftime("%m", Review.created_at) == f"{now.month:02d}",
            func.strftime("%Y", Review.created_at) == str(now.year)
        )
        .scalar()
    )

    return {
        "total_reviews": total_reviews,
        "detected_fake": detected_fake,
        "flagged_reviews": flagged_reviews,
        "monthly_reviews": month_reviews
    }
