def generate_explanation(restaurant):
    aspects = restaurant["aspects"]
    
    positives = []
    negatives = []
    
    for aspect, sentiment in aspects.items():
        if sentiment in ["Positive", "Very Positive"]:
            positives.append(aspect)
        elif sentiment in ["Negative", "Very Negative"]:
            negatives.append(aspect)
    
    explanation = ""
    
    if positives:
        explanation += f"Great {', '.join(positives)}. "
    
    if negatives:
        explanation += f"But some issues with {', '.join(negatives)}. "
    
    return explanation.strip()