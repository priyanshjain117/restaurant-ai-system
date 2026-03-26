def aggregate_reviews(reviews, aspect_analyzer):
    aspect_scores = {}

    for review in reviews:
        result = aspect_analyzer(review)
        
        for aspect, data in result.items():
            if data["sentiment"] == "Not Mentioned":
                continue
            
            score = sentiment_to_score(data["sentiment"])
            
            if aspect not in aspect_scores:
                aspect_scores[aspect] = []
            
            aspect_scores[aspect].append(score)

    # Average per aspect
    final = {}
    
    for aspect, scores in aspect_scores.items():
        avg = sum(scores) / len(scores)
        final[aspect] = score_to_label(avg)
    
    return final

def sentiment_to_score(label):
    mapping = {
        "Very Negative": 0,
        "Negative": 1,
        "Neutral": 2,
        "Positive": 3,
        "Very Positive": 4
    }
    return mapping[label]


def score_to_label(score):
    rounded = int(round(score))
    
    reverse = {
        0: "Very Negative",
        1: "Negative",
        2: "Neutral",
        3: "Positive",
        4: "Very Positive"
    }
    return reverse[rounded]