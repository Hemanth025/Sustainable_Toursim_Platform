# Dynamic Pricing Engine
# Logic-based pricing rules without real-time APIs

from datetime import datetime
from modules.knowledge_base import SEASONAL_PRICING, FESTIVAL_PERIODS, DESTINATIONS

def get_current_season():
    """
    Determine current season based on month.
    """
    current_month = datetime.now().month
    
    for season, data in SEASONAL_PRICING.items():
        if current_month in data["months"]:
            return {
                "season": season,
                "label": data["label"],
                "multiplier": data["multiplier"]
            }
    
    return {"season": "shoulder", "label": "Shoulder Season", "multiplier": 1.0}


def check_festival_period():
    """
    Check if current date falls in a festival period.
    """
    current_month = datetime.now().month
    current_week = (datetime.now().day - 1) // 7 + 1
    
    for festival, data in FESTIVAL_PERIODS.items():
        if current_month == data["month"] and current_week in data["weeks"]:
            return {
                "is_festival": True,
                "festival_name": festival.replace("_", " ").title(),
                "multiplier": data["multiplier"]
            }
    
    return {"is_festival": False, "festival_name": None, "multiplier": 1.0}


def calculate_price_level(destination_id, travel_month=None):
    """
    Calculate price level and booking recommendations.
    
    Args:
        destination_id: ID of destination
        travel_month: Target month for travel (1-12), defaults to current
    
    Returns:
        Price analysis with recommendations
    """
    if destination_id not in DESTINATIONS:
        return None
    
    dest = DESTINATIONS[destination_id]
    target_month = travel_month if travel_month else datetime.now().month
    
    # Base price levels (relative indices)
    base_prices = {
        "low": 100,
        "medium": 200,
        "high": 350
    }
    
    base_price = base_prices.get(dest["budget_level"], 200)
    
    # Determine season for target month
    for season, data in SEASONAL_PRICING.items():
        if target_month in data["months"]:
            season_info = {
                "season": season,
                "label": data["label"],
                "multiplier": data["multiplier"]
            }
            break
    else:
        season_info = {"season": "shoulder", "label": "Shoulder Season", "multiplier": 1.0}
    
    # Check for festival premium
    festival_info = {"is_festival": False, "multiplier": 1.0}
    for festival, data in FESTIVAL_PERIODS.items():
        if target_month == data["month"]:
            festival_info = {
                "is_festival": True,
                "festival_name": festival.replace("_", " ").title(),
                "multiplier": data["multiplier"]
            }
            break
    
    # Calculate final price index
    final_multiplier = season_info["multiplier"]
    if festival_info["is_festival"]:
        final_multiplier = max(final_multiplier, festival_info["multiplier"])
    
    final_price_index = base_price * final_multiplier
    
    # Generate price level label
    if final_multiplier <= 0.9:
        price_level = "Low"
        price_color = "green"
    elif final_multiplier <= 1.1:
        price_level = "Moderate"
        price_color = "yellow"
    elif final_multiplier <= 1.4:
        price_level = "High"
        price_color = "orange"
    else:
        price_level = "Premium"
        price_color = "red"
    
    return {
        "destination": dest["name"],
        "month": target_month,
        "season": season_info,
        "festival": festival_info,
        "price_level": price_level,
        "price_color": price_color,
        "price_index": round(final_price_index),
        "multiplier": round(final_multiplier, 2)
    }


def get_best_time_to_book(destination_id):
    """
    Find the best months to book for a destination.
    """
    if destination_id not in DESTINATIONS:
        return None
    
    dest = DESTINATIONS[destination_id]
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    monthly_analysis = []
    
    for month in range(1, 13):
        price_info = calculate_price_level(destination_id, month)
        month_name = month_names[month - 1]
        
        # Check if it's in best season
        is_best_season = month_name.lower() in dest["best_season"]
        
        monthly_analysis.append({
            "month": month,
            "month_name": month_name,
            "price_level": price_info["price_level"],
            "price_index": price_info["price_index"],
            "multiplier": price_info["multiplier"],
            "is_best_season": is_best_season,
            "season_label": price_info["season"]["label"],
            "festival": price_info["festival"]["festival_name"] if price_info["festival"]["is_festival"] else None
        })
    
    # Find best value months (good weather + lower prices)
    best_value_months = [
        m for m in monthly_analysis 
        if m["is_best_season"] and m["multiplier"] <= 1.2
    ]
    
    # If no best value, find lowest price months
    if not best_value_months:
        monthly_analysis_sorted = sorted(monthly_analysis, key=lambda x: x["multiplier"])
        best_value_months = monthly_analysis_sorted[:3]
    
    # Find cheapest month overall
    cheapest = min(monthly_analysis, key=lambda x: x["multiplier"])
    
    return {
        "destination": dest["name"],
        "monthly_analysis": monthly_analysis,
        "best_value_months": [m["month_name"] for m in best_value_months],
        "cheapest_month": cheapest["month_name"],
        "cheapest_multiplier": cheapest["multiplier"],
        "booking_advice": generate_booking_advice(dest, best_value_months, cheapest)
    }


def generate_booking_advice(destination, best_value_months, cheapest):
    """
    Generate personalized booking advice.
    """
    advice = []
    
    if best_value_months:
        month_list = ", ".join([m["month_name"] for m in best_value_months[:3]])
        advice.append(f"🌟 Best value: Book for {month_list} - ideal weather with moderate prices")
    
    if cheapest["multiplier"] < 1.0:
        advice.append(f"💰 Budget tip: {cheapest['month_name']} offers up to {int((1 - cheapest['multiplier']) * 100)}% savings")
    
    advice.append(f"📅 Book 6-8 weeks in advance for best rates on sustainable accommodations")
    
    if destination["eco_score"] >= 8:
        advice.append(f"🌿 Eco bonus: This destination has excellent sustainability practices")
    
    return advice


def get_pricing_comparison(destination_ids):
    """
    Compare pricing across multiple destinations.
    """
    current_month = datetime.now().month
    comparisons = []
    
    for dest_id in destination_ids:
        if dest_id in DESTINATIONS:
            price_info = calculate_price_level(dest_id, current_month)
            best_time = get_best_time_to_book(dest_id)
            
            comparisons.append({
                "destination_id": dest_id,
                "destination_name": price_info["destination"],
                "current_price_level": price_info["price_level"],
                "current_multiplier": price_info["multiplier"],
                "best_value_months": best_time["best_value_months"][:2],
                "eco_score": DESTINATIONS[dest_id]["eco_score"]
            })
    
    # Sort by price index (lower is better value)
    comparisons.sort(key=lambda x: x["current_multiplier"])
    
    return {
        "current_month": datetime.now().strftime("%B"),
        "comparisons": comparisons
    }
