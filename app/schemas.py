from pydantic import BaseModel


class PredictionResponse(BaseModel):
    text: str
    prediction: str
    hate_type: str
    confidence: float
    language: str
    model: str
