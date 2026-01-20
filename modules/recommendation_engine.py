# Rule-Based Recommendation Engine
# No ML training - Pure decision logic

from modules.knowledge_base import DESTINATIONS
from datetime import datetime

def get_recommendations(budget, travel_type, duration, sustainability_pref):
    """
    Generate personalized travel recommendations using rule-based logic.
    
    Args:
        budget: 'low', 'medium', 'high'
        travel_type: 'adventure', 'nature', 'spiritual', 'cultural', 'beach', 'relaxation'
        duration: number of days (int)
        sustainability_pref: 1-10 scale (int)
    
    Returns:
        List of recommended destinations with scores
    """
    recommendations = []
    current_month = datetime.now().strftime("%B").lower()
    
    for dest_id, dest in DESTINATIONS.items():
        score = 0
        match_reasons = []
        
        # Budget matching (25 points max)
        if dest["budget_level"] == budget:
            score += 25
            match_reasons.append(f"Matches your {budget} budget")
        elif (budget == "medium" and dest["budget_level"] in ["low", "medium"]) or \
             (budget == "high"):
            score += 15
            match_reasons.append("Within budget range")
        
        # Travel type matching (30 points max)
        if travel_type in dest["type"]:
            score += 30
            match_reasons.append(f"Perfect for {travel_type} travelers")
        elif any(t in ["nature", "relaxation"] for t in dest["type"]):
            score += 10  # Nature/relaxation are universally appealing
        
        # Duration-distance optimization (20 points max)
        distance = dest["distance_from_delhi"]
        if duration <= 3 and distance <= 500:
            score += 20
            match_reasons.append("Ideal for short trips")
        elif duration <= 5 and distance <= 1000:
            score += 18
            match_reasons.append("Good for medium duration")
        elif duration > 5 and distance <= 2500:
            score += 15
            match_reasons.append("Suitable for longer stays")
        elif duration > 7:
            score += 10  # Long trips can go anywhere
        
        # Sustainability preference matching (25 points max)
        eco_match = abs(dest["eco_score"] - sustainability_pref)
        if eco_match <= 1:
            score += 25
            match_reasons.append(f"Eco-score {dest['eco_score']}/10 matches your preference")
        elif eco_match <= 2:
            score += 20
            match_reasons.append(f"Good eco-score: {dest['eco_score']}/10")
        elif eco_match <= 3:
            score += 15
        else:
            score += 10
        
        # Seasonal bonus (10 points)
        if current_month in dest["best_season"]:
            score += 10
            match_reasons.append("Great time to visit!")
        
        # Compile recommendation
        recommendations.append({
            "id": dest_id,
            "name": dest["name"],
            "description": dest["description"],
            "eco_score": dest["eco_score"],
            "budget_level": dest["budget_level"],
            "score": score,
            "match_reasons": match_reasons[:3],  # Top 3 reasons
            "sustainability_features": dest["sustainability_features"],
            "carbon_rating": dest["carbon_rating"],
            "distance": distance
        })
    
    # Sort by score descending
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    return recommendations[:5]  # Return top 5


def generate_itinerary(destination_id, duration, budget, sustainability_pref):
    """
    Generate a day-by-day itinerary using rule-based logic.
    """
    if destination_id not in DESTINATIONS:
        return None
    
    dest = DESTINATIONS[destination_id]
    itinerary = {
        "destination": dest["name"],
        "destination_name": dest["name"], # Added for consistency with map flow
        "dest_lat": dest.get("lat"),
        "dest_lon": dest.get("lon"),
        "duration": duration,
        "eco_score": dest["eco_score"],
        "days": []
    }
    
    # Rule-based activity assignment
    activities_pool = {
        "adventure": ["Trekking", "River rafting", "Mountain biking", "Paragliding", "Camping"],
        "nature": ["Nature walk", "Bird watching", "Wildlife safari", "Botanical garden visit", "Sunrise viewing"],
        "spiritual": ["Temple visit", "Yoga session", "Meditation retreat", "Ganga Aarti", "Ashram experience"],
        "cultural": ["Heritage walk", "Museum visit", "Local craft workshop", "Folk dance show", "Cooking class"],
        "beach": ["Beach cleanup activity", "Snorkeling", "Sunset cruise", "Beach yoga", "Coastal walk"],
        "relaxation": ["Spa treatment", "Houseboat cruise", "Tea tasting", "Ayurvedic therapy", "Scenic picnic"]
    }
    
    # Sustainable options based on preference
    sustainable_activities = [
        "Visit local organic farm",
        "Community interaction",
        "Local artisan workshop",
        "Eco-trail hike",
        "Traditional cooking with locals"
    ]
    
    for day in range(1, duration + 1):
        day_plan = {
            "day": day,
            "morning": "",
            "afternoon": "",
            "evening": "",
            "eco_tip": ""
        }
        
        # Assign activities based on destination type and day
        dest_types = dest["type"]
        primary_type = dest_types[0]
        
        if day == 1:
            day_plan["morning"] = "Arrival and check-in at eco-friendly accommodation"
            day_plan["afternoon"] = "Local area orientation walk"
            day_plan["evening"] = "Welcome dinner with local cuisine"
        elif day == duration:
            day_plan["morning"] = "Leisure morning / packing"
            day_plan["afternoon"] = "Departure"
            day_plan["evening"] = "Travel"
        else:
            # Rotate through activities
            pool = activities_pool.get(primary_type, activities_pool["nature"])
            idx = (day - 2) % len(pool)
            day_plan["morning"] = pool[idx]
            
            if sustainability_pref >= 7:
                sus_idx = (day - 2) % len(sustainable_activities)
                day_plan["afternoon"] = sustainable_activities[sus_idx]
            else:
                secondary_type = dest_types[1] if len(dest_types) > 1 else primary_type
                sec_pool = activities_pool.get(secondary_type, pool)
                day_plan["afternoon"] = sec_pool[(idx + 1) % len(sec_pool)]
            
            day_plan["evening"] = "Local dining experience" if day % 2 == 0 else "Rest and cultural show"
        
        # Add eco-tips
        eco_tips = [
            "Use refillable water bottles to reduce plastic waste",
            "Support local businesses by buying handmade souvenirs",
            "Use public transport or walk when possible",
            "Respect local customs and dress codes",
            "Conserve water and electricity at your accommodation",
            "Avoid single-use plastics",
            "Participate in any available cleanup activities"
        ]
        day_plan["eco_tip"] = eco_tips[(day - 1) % len(eco_tips)]
        
        itinerary["days"].append(day_plan)
    
    # Add accommodation suggestion
    if sustainability_pref >= 7:
        itinerary["accommodation"] = dest["homestays"][0] if dest["homestays"] else "Eco Lodge"
        itinerary["accommodation_type"] = "Sustainable Homestay"
    elif budget == "low":
        itinerary["accommodation"] = "Budget Eco Hotel"
        itinerary["accommodation_type"] = "Budget Friendly"
    else:
        itinerary["accommodation"] = "Green Certified Hotel"
        itinerary["accommodation_type"] = "Eco-Certified"
    
    # Add local guide recommendation
    itinerary["local_guide"] = dest["local_guides"][0] if dest["local_guides"] else "Local Community Guide"
    
    return itinerary
