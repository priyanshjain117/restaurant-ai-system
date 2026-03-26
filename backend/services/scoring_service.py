def score_restaurant(restaurant):
    aspects = restaurant["aspects"]
    
    score_map = {
        "Very Negative": 0,
        "Negative": 1,
        "Neutral": 2,
        "Positive": 3,
        "Very Positive": 4
    }
    
    weights = {
        "food": 0.4,
        "service": 0.2,
        "ambience": 0.2,
        "price": 0.1,
        "cleanliness": 0.1
    }
    
    total_score = 0
    
    for aspect, sentiment in aspects.items():
        if sentiment == "Not Mentioned":
            continue
        
        total_score += score_map[sentiment] * weights.get(aspect, 0)
    
    return total_score
    