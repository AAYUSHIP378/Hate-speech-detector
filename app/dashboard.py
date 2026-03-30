from fastapi import APIRouter
from app.database import SessionLocal, Prediction
from collections import Counter

router = APIRouter()

@router.get("/admin/data")
def dashboard_data():

    db = SessionLocal()
    records = db.query(Prediction).all()
    db.close()

    total = len(records)

    predictions = [r.prediction for r in records]
    languages = [r.language for r in records]

    return {
        "total_predictions": total,
        "prediction_count": dict(Counter(predictions)),
        "language_count": dict(Counter(languages))
    }
