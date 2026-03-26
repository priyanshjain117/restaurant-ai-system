from .aspect_extractor import extract_aspects
from backend.ml.inference import predict_sentiment, predict_proba

label_map = {
    0: "Very Negative",
    1: "Negative",
    2: "Neutral",
    3: "Positive",
    4: "Very Positive"
}

def analyze_aspects(review):
    aspect_data = extract_aspects(review)
    
    result = {}
    
    for aspect, sentences in aspect_data.items():
        if sentences:
            sentiments = []
            confidences = []
            
            for s in sentences:
                pred = predict_sentiment(s)
                prob = predict_proba(s)
                
                sentiments.append(pred)
                confidences.append(max(prob.values()))
            
            avg_sentiment = int(round(sum(sentiments) / len(sentiments)))
            avg_conf = sum(confidences) / len(confidences)
            
            result[aspect] = {
                "sentiment": label_map[avg_sentiment],
                "confidence": round(avg_conf, 2)
            }
        else:
            result[aspect] = {
                "sentiment": "Not Mentioned",
                "confidence": 0.0
            }
    
    return result