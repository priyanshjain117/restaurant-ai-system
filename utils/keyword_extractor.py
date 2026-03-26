from collections import Counter

def extract_keywords(reviews):
    words = []
    
    for r in reviews:
        words.extend(r.lower().split())
    
    common = Counter(words).most_common(10)
    
    return [w[0] for w in common]