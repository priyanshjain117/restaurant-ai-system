from backend.ml.aspect.aspect_pipeline import analyze_aspects

def process_restaurant(restaurant):
    all_aspects = []

    for review in restaurant["reviews"]:
        result = analyze_aspects(review)
        all_aspects.append(result)

    # Aggregate
    aggregated = {}

    for aspect_data in all_aspects:
        for aspect, val in aspect_data.items():
            if val["sentiment"] == "Not Mentioned":
                continue

            if aspect not in aggregated:
                aggregated[aspect] = []

            aggregated[aspect].append(val["sentiment"])

    # Simple majority
    final = {}
    for aspect, sentiments in aggregated.items():
        final[aspect] = max(set(sentiments), key=sentiments.count)

    restaurant["aspects"] = final

    return restaurant