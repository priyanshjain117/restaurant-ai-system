from backend.ml.aspect.aspect_pipeline import analyze_aspects

def get_aspect_analysis(review):
    return analyze_aspects(review)