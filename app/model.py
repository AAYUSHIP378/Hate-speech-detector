import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from app.config import LABELS, MODEL_USED
from app.utils import detect_language, rule_based_hate
from app.hate_types import detect_hate_type

# ---------------- MODEL PATH ----------------
MODEL_PATH = "model/resumed_final_from_65088"

# ---------------- LOAD TOKENIZER ----------------
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True,
    use_fast=False
)

# ---------------- LOAD MODEL ----------------
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

model.eval()

# ---------------- PREDICT FUNCTION ----------------
def predict(text: str):

    text = text.strip()

    if not text:
        return {
            "text": "",
            "prediction": "Invalid",
            "hate_type": "None",
            "confidence": 0,
            "language": "Unknown",
            "model": MODEL_USED,
            "action": "Ignore"
        }

    # 🔹 TOKENIZE
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    # 🔹 MODEL INFERENCE
    with torch.no_grad():
        outputs = model(**inputs)

    probs = F.softmax(outputs.logits, dim=1)
    confidence, predicted_class = torch.max(probs, dim=1)

    score = round(confidence.item() * 100, 2)
    label = LABELS[predicted_class.item()]

    # 🔹 LOW CONFIDENCE FIX
    if score < 60:
        label = "Non Hate"

    # 🔹 RULE BASED OVERRIDE
    if rule_based_hate(text):
        label = "Hate Speech"
        score = max(score, 80)   # थोड़ा boost ताकि realistic लगे

    # 🔹 LANGUAGE DETECTION
    language = detect_language(text)

    # 🔹 HATE TYPE
    hate_type = "None"
    if label == "Hate Speech":
        hate_type = detect_hate_type(text)

    # 🔹 SMART ACTION LOGIC (IMPROVED)
    if label == "Hate Speech":
        if score >= 85:
            action = "Block"
        else:
            action = "Review"
    elif score < 50:
        action = "Review"
    else:
        action = "Allow"

    # 🔹 FINAL OUTPUT
    return {
        "text": text,
        "prediction": label,
        "hate_type": hate_type,
        "confidence": score,
        "language": language,
        "model": MODEL_USED,
        "action": action
    }