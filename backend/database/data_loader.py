import json

def load_restaurants():
    with open("data/restaurants.json", "r") as f:
        return json.load(f)