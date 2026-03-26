from .filter_service import filter_restaurants
from .scoring_service import score_restaurant
from .explanation_service import generate_explanation
from .restaurant_service import process_restaurant

def recommend_restaurants(restaurants, query):

    # Step 1: Process restaurants (add aspects)
    processed = [process_restaurant(r) for r in restaurants]

    # Step 2: Filter
    filtered = filter_restaurants(processed, query)

    results = []

    for r in filtered:
        score = score_restaurant(r)
        explanation = generate_explanation(r)

        results.append({
            "name": r["name"],
            "score": round(score, 2),
            "explanation": explanation
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results
