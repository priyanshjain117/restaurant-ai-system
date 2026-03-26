from fastapi import APIRouter
from backend.services.aspect_service import get_aspect_analysis

from backend.services.recommendation_service import recommend_restaurants
from backend.database.data_loader import load_restaurants

router = APIRouter()

@router.post("/aspect-analysis")
def aspect_analysis(data: dict):
    review = data["review"]
    result = get_aspect_analysis(review)
    return result


@router.post("/recommend")
def recommend(data: dict):
    query = data["query"]
    
    restaurants = load_restaurants()
    
    results = recommend_restaurants(restaurants, query)
    
    return {"results": results}