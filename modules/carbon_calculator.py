# Carbon Footprint Calculator
# Uses fixed industry-standard emission factors (ISO 14001 aligned)

from modules.knowledge_base import (
    TRANSPORT_EMISSIONS, 
    ACCOMMODATION_EMISSIONS, 
    FOOD_EMISSIONS,
    DESTINATIONS,
    ISO_14001_POINTS
)

def calculate_transport_emissions(transport_mode, distance_km, passengers=1):
    """
    Calculate transport carbon emissions.
    
    Args:
        transport_mode: 'flight', 'train', 'bus', 'car', 'electric_car', 'bicycle'
        distance_km: total distance in kilometers
        passengers: number of passengers (for car sharing calculation)
    
    Returns:
        dict with emissions data and alternatives
    """
    emission_factor = TRANSPORT_EMISSIONS.get(transport_mode, 0.171)
    total_emissions = emission_factor * distance_km
    
    # For car, divide by passengers for per-person calculation
    if transport_mode == "car" and passengers > 1:
        total_emissions = total_emissions / passengers
    
    # Calculate all alternatives
    alternatives = []
    for mode, factor in TRANSPORT_EMISSIONS.items():
        if mode != transport_mode:
            alt_emissions = factor * distance_km
            if mode == "car" and passengers > 1:
                alt_emissions = alt_emissions / passengers
            
            savings = total_emissions - alt_emissions
            if savings > 0:
                alternatives.append({
                    "mode": mode.replace("_", " ").title(),
                    "emissions": round(alt_emissions, 2),
                    "savings": round(savings, 2),
                    "savings_percent": round((savings / total_emissions) * 100, 1)
                })
    
    # Sort by savings
    alternatives.sort(key=lambda x: x["savings"], reverse=True)
    
    return {
        "mode": transport_mode.replace("_", " ").title(),
        "distance_km": distance_km,
        "emissions_kg": round(total_emissions, 2),
        "greener_alternatives": alternatives[:3],  # Top 3 alternatives
        "eco_rating": get_eco_rating(total_emissions, "transport", distance_km)
    }


def calculate_accommodation_emissions(accommodation_type, nights):
    """
    Calculate accommodation carbon emissions.
    """
    emission_factor = ACCOMMODATION_EMISSIONS.get(accommodation_type, 20.9)
    total_emissions = emission_factor * nights
    
    alternatives = []
    for acc_type, factor in ACCOMMODATION_EMISSIONS.items():
        if acc_type != accommodation_type:
            alt_emissions = factor * nights
            savings = total_emissions - alt_emissions
            if savings > 0:
                alternatives.append({
                    "type": acc_type.replace("_", " ").title(),
                    "emissions": round(alt_emissions, 2),
                    "savings": round(savings, 2),
                    "savings_percent": round((savings / total_emissions) * 100, 1) if total_emissions > 0 else 0
                })
    
    alternatives.sort(key=lambda x: x["savings"], reverse=True)
    
    return {
        "type": accommodation_type.replace("_", " ").title(),
        "nights": nights,
        "emissions_kg": round(total_emissions, 2),
        "greener_alternatives": alternatives[:3],
        "eco_rating": get_eco_rating(total_emissions, "accommodation", nights)
    }


def calculate_food_emissions(food_preference, days):
    """
    Calculate food-related carbon emissions.
    """
    emission_factor = FOOD_EMISSIONS.get(food_preference, 5.1)
    total_emissions = emission_factor * days
    
    alternatives = []
    for food_type, factor in FOOD_EMISSIONS.items():
        if food_type != food_preference:
            alt_emissions = factor * days
            savings = total_emissions - alt_emissions
            if savings > 0:
                alternatives.append({
                    "type": food_type.replace("_", " ").title(),
                    "emissions": round(alt_emissions, 2),
                    "savings": round(savings, 2),
                    "savings_percent": round((savings / total_emissions) * 100, 1) if total_emissions > 0 else 0
                })
    
    alternatives.sort(key=lambda x: x["savings"], reverse=True)
    
    return {
        "preference": food_preference.replace("_", " ").title(),
        "days": days,
        "emissions_kg": round(total_emissions, 2),
        "greener_alternatives": alternatives[:3],
        "eco_rating": get_eco_rating(total_emissions, "food", days)
    }


def get_eco_rating(emissions, category, unit_count):
    """
    Calculate eco rating (A to E) based on emissions per unit.
    """
    per_unit = emissions / unit_count if unit_count > 0 else emissions
    
    thresholds = {
        "transport": [(0.05, "A"), (0.1, "B"), (0.15, "C"), (0.2, "D"), (float("inf"), "E")],
        "accommodation": [(5, "A"), (10, "B"), (15, "C"), (25, "D"), (float("inf"), "E")],
        "food": [(3, "A"), (4, "B"), (5, "C"), (6, "D"), (float("inf"), "E")]
    }
    
    for threshold, rating in thresholds.get(category, thresholds["transport"]):
        if per_unit <= threshold:
            return rating
    return "E"


def calculate_total_footprint(transport_mode, distance_km, accommodation_type, 
                               nights, food_preference, passengers=1):
    """
    Calculate complete trip carbon footprint.
    """
    transport = calculate_transport_emissions(transport_mode, distance_km, passengers)
    accommodation = calculate_accommodation_emissions(accommodation_type, nights)
    food = calculate_food_emissions(food_preference, nights)
    
    total_emissions = transport["emissions_kg"] + accommodation["emissions_kg"] + food["emissions_kg"]
    
    # Calculate overall eco-score (1-10)
    # Based on average Indian's daily carbon footprint: ~5.5 kg CO2
    baseline_per_day = 5.5 * nights
    ratio = total_emissions / baseline_per_day if baseline_per_day > 0 else 1
    
    if ratio <= 0.5:
        eco_score = 10
    elif ratio <= 0.75:
        eco_score = 9
    elif ratio <= 1.0:
        eco_score = 8
    elif ratio <= 1.25:
        eco_score = 7
    elif ratio <= 1.5:
        eco_score = 6
    elif ratio <= 2.0:
        eco_score = 5
    elif ratio <= 2.5:
        eco_score = 4
    elif ratio <= 3.0:
        eco_score = 3
    else:
        eco_score = 2
    
    # Calculate potential savings
    best_transport = min(TRANSPORT_EMISSIONS.values()) * distance_km
    best_accommodation = min(ACCOMMODATION_EMISSIONS.values()) * nights
    best_food = min(FOOD_EMISSIONS.values()) * nights
    best_possible = best_transport + best_accommodation + best_food
    potential_savings = total_emissions - best_possible
    
    return {
        "transport": transport,
        "accommodation": accommodation,
        "food": food,
        "total_emissions_kg": round(total_emissions, 2),
        "eco_score": eco_score,
        "potential_savings_kg": round(potential_savings, 2),
        "trees_to_offset": round(total_emissions / 21, 1),  # Avg tree absorbs 21kg CO2/year
        "iso_14001_alignment": ISO_14001_POINTS,
        "breakdown": {
            "transport_percent": round((transport["emissions_kg"] / total_emissions) * 100, 1) if total_emissions > 0 else 0,
            "accommodation_percent": round((accommodation["emissions_kg"] / total_emissions) * 100, 1) if total_emissions > 0 else 0,
            "food_percent": round((food["emissions_kg"] / total_emissions) * 100, 1) if total_emissions > 0 else 0
        }
    }


def get_destination_carbon_info(destination_id):
    """
    Get carbon-related information for a destination.
    """
    if destination_id not in DESTINATIONS:
        return None
    
    dest = DESTINATIONS[destination_id]
    return {
        "name": dest["name"],
        "carbon_rating": dest["carbon_rating"],
        "eco_score": dest["eco_score"],
        "distance_from_delhi": dest["distance_from_delhi"],
        "sustainability_features": dest["sustainability_features"],
        "recommended_transport": "train" if dest["distance_from_delhi"] < 1000 else "flight",
        "eco_tips": dest["ar_content"]["eco_tips"]
    }
