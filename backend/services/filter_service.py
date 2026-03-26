def filter_restaurants(restaurants, query):
    filtered = []
    
    for r in restaurants:
        # Veg filter
        if "veg" in query.lower() and not r["is_veg"]:
            continue
        
        # Location filter
        if "jaipur" in query.lower() and "jaipur" not in r["location"].lower():
            continue
        
        filtered.append(r)
    
    return filtered
