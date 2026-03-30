from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import joblib
import time
import re
import json
import os

app = FastAPI()

# Allow the React frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ─── 1. LOAD ARTEFACTS ON STARTUP ───
print("Loading embeddings model... (this takes a moment)")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

print("Loading ML models and scaler...")
try:
    scaler = joblib.load("models/scaler.pkl")
    ml_models = {
        "XGBoost": joblib.load("models/xgb_model.pkl"),
        "Logistic Regression": joblib.load("models/lr_model.pkl"),
        "Linear SVM": joblib.load("models/svm_model.pkl"),
    }
    with open("models/classes.json", "r") as f:
        class_names = json.load(f)
    print("All artefacts loaded successfully ✓")
except Exception as e:
    print(f"Error loading models: {e}. Make sure the 'models' folder exists and contains the .pkl files.")

# ─── 2. DATA MODELS ───
class PredictRequest(BaseModel):
    review: str
    model: str = "all"  

# ─── 3. PREPROCESSING LOGIC ───
def preprocess_text(text: str) -> str:
    """Basic NLP preprocessing mirroring the frontend pipeline description."""
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text) 
    
    
    return " ".join(text.split())

# ─── 4. API ENDPOINT ───
@app.post("/api/predict")
async def predict(req: PredictRequest):
    start_time = time.time()
    
    # Clean and check text
    clean_text = preprocess_text(req.review)
    if not clean_text:
        raise HTTPException(status_code=400, detail="Review text is empty after preprocessing.")
        
    # Generate 384-dim embedding
    embedding = embedder.encode([clean_text])
    
    # Scale embedding
    scaled_embedding = scaler.transform(embedding)
    
    # Route to requested model(s)
    target_models = {}
    if req.model == "all":
        target_models = ml_models
    elif req.model == "xgboost":
        target_models = {"XGBoost": ml_models["XGBoost"]}
    elif req.model == "logistic_regression":
        target_models = {"Logistic Regression": ml_models["Logistic Regression"]}
    elif req.model == "svm":
        target_models = {"Linear SVM": ml_models["Linear SVM"]}
    else:
        raise HTTPException(status_code=400, detail="Invalid model selection.")
        
    # Run Inference
    results = {}
    for name, clf in target_models.items():
        pred_val = clf.predict(scaled_embedding)[0]
        
        # Get confidence/probabilities if the model supports it
        probs = {}
        conf = None
        if hasattr(clf, "predict_proba"):
            proba_array = clf.predict_proba(scaled_embedding)[0]
            conf = float(max(proba_array))
            # Map probabilities to class names safely
            probs = {str(c): float(p) for c, p in zip(clf.classes_, proba_array)}
            
        results[name] = {
            "prediction": str(pred_val),
            "confidence": conf,
            "probabilities": probs
        }
        
    latency = round((time.time() - start_time) * 1000, 2)
    
    return {
        "clean_text": clean_text,
        "model_used": req.model,
        "results": results,
        "latency_ms": latency
    }