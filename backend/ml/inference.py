from sentence_transformers import SentenceTransformer
import joblib
import numpy as np
# Set environment variables to optimize performance
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
# Load once (VERY IMPORTANT for performance)
# model = SentenceTransformer("models/sentiment/sentence_transformer_model")

model = SentenceTransformer("all-MiniLM-L6-v2",device="cpu")
clf = joblib.load("models/sentiment/ml_classifier.pkl")
scaler = joblib.load("models/sentiment/scaler.pkl")

label_map = {
    0: "Very Negative",
    1: "Negative",
    2: "Neutral",
    3: "Positive",
    4: "Very Positive"
}

def predict_sentiment(text: str):
    embedding = model.encode([text])
    embedding = scaler.transform(embedding)
    
    pred = clf.predict(embedding)[0]
    return pred


def predict_with_label(text: str):
    pred = predict_sentiment(text)
    return label_map[pred]


def predict_proba(text: str):
    """
    Returns confidence scores (VERY IMPORTANT for Phase 3)
    """
    embedding = model.encode([text])
    embedding = scaler.transform(embedding)
    
    probs = clf.predict_proba(embedding)[0]
    
    return {
        label_map[i]: float(probs[i])
        for i in range(len(probs))
    }