# Knowledge Base Module - Hardcoded Sustainable Tourism Data
# No datasets, no ML - Pure rule-based logic

# Sustainable destinations with eco-scores (1-10)
DESTINATIONS = {
    "manali": {
        "name": "Manali, Himachal Pradesh",
        "type": ["adventure", "nature", "spiritual"],
        "eco_score": 8,
        "budget_level": "medium",
        "best_season": ["march", "april", "may", "june", "october", "november"],
        "carbon_rating": "low",
        "description": "Himalayan hill station known for eco-tourism and adventure sports",
        "sustainability_features": ["Solar-powered hotels", "Plastic-free zones", "Local community tours"],
        "local_guides": ["Himalayan Eco Treks", "Green Valley Tours"],
        "homestays": ["Mountain View Homestay", "Eco Cottage Manali"],
        "distance_from_delhi": 540,
        "lat": 32.2432,
        "lon": 77.1892,
        "ar_content": {
            "cultural_info": "Ancient Hadimba Temple, built in 1553, showcases traditional Himalayan architecture",
            "eco_tips": "Carry reusable water bottles, avoid plastic bags, respect local wildlife"
        }
    },
    "kerala_backwaters": {
        "name": "Kerala Backwaters",
        "type": ["nature", "relaxation", "cultural"],
        "eco_score": 9,
        "budget_level": "medium",
        "best_season": ["september", "october", "november", "december", "january", "february"],
        "carbon_rating": "low",
        "description": "Sustainable houseboat tourism with responsible tourism practices",
        "sustainability_features": ["Solar houseboats", "Organic food", "Zero-waste initiatives"],
        "local_guides": ["Responsible Tourism Kerala", "Green Palm Tours"],
        "homestays": ["Coconut Lagoon Homestay", "Backwater Breeze Home"],
        "distance_from_delhi": 2200,
        "lat": 9.4981,
        "lon": 76.3388,
        "ar_content": {
            "cultural_info": "Traditional Kettuvallam houseboats made from eco-friendly jackwood and bamboo",
            "eco_tips": "Choose certified responsible tourism operators, avoid feeding wildlife"
        }
    },
    "rishikesh": {
        "name": "Rishikesh, Uttarakhand",
        "type": ["spiritual", "adventure", "nature"],
        "eco_score": 8,
        "budget_level": "low",
        "best_season": ["february", "march", "april", "may", "september", "october", "november"],
        "carbon_rating": "low",
        "description": "Yoga capital of the world with strong eco-consciousness",
        "sustainability_features": ["Vegetarian food culture", "Ganga conservation", "Ashram stays"],
        "local_guides": ["Ganga Eco Adventures", "Spiritual Rishikesh Tours"],
        "homestays": ["Yoga Ashram Stay", "Riverside Eco Cottage"],
        "distance_from_delhi": 250,
        "lat": 30.0869,
        "lon": 78.2676,
        "ar_content": {
            "cultural_info": "Sacred Triveni Ghat where three holy rivers meet, center of Hindu spirituality",
            "eco_tips": "Participate in Ganga cleanup drives, use biodegradable products near the river"
        }
    },
    "jaipur": {
        "name": "Jaipur, Rajasthan",
        "type": ["cultural", "heritage", "luxury"],
        "eco_score": 6,
        "budget_level": "medium",
        "best_season": ["october", "november", "december", "january", "february", "march"],
        "carbon_rating": "medium",
        "description": "Pink City with heritage hotels and cultural experiences",
        "sustainability_features": ["Heritage hotel restoration", "Traditional crafts support", "Water conservation"],
        "local_guides": ["Pink City Walks", "Rajasthan Heritage Tours"],
        "homestays": ["Haveli Heritage Home", "Royal Courtyard Stay"],
        "distance_from_delhi": 280,
        "lat": 26.9124,
        "lon": 75.7873,
        "ar_content": {
            "cultural_info": "Amber Fort, a UNESCO World Heritage site showcasing Rajput architecture from 1592",
            "eco_tips": "Support local artisans, choose heritage hotels that practice water recycling"
        }
    },
    "coorg": {
        "name": "Coorg, Karnataka",
        "type": ["nature", "relaxation", "adventure"],
        "eco_score": 9,
        "budget_level": "medium",
        "best_season": ["october", "november", "december", "january", "february", "march"],
        "carbon_rating": "low",
        "description": "Coffee country with sustainable plantation tourism",
        "sustainability_features": ["Organic coffee estates", "Wildlife corridors", "Tribal community support"],
        "local_guides": ["Coorg Eco Trails", "Plantation Discovery Tours"],
        "homestays": ["Coffee Blossom Homestay", "Misty Hills Cottage"],
        "distance_from_delhi": 2100,
        "lat": 12.4244,
        "lon": 75.7382,
        "ar_content": {
            "cultural_info": "Kodava culture with unique traditions, martial arts heritage and organic farming",
            "eco_tips": "Buy directly from local coffee farmers, avoid disturbing wildlife areas"
        }
    },
    "ladakh": {
        "name": "Ladakh",
        "type": ["adventure", "spiritual", "nature"],
        "eco_score": 7,
        "budget_level": "high",
        "best_season": ["may", "june", "july", "august", "september"],
        "carbon_rating": "high",
        "description": "High-altitude desert with unique Buddhist culture",
        "sustainability_features": ["Solar energy adoption", "Waste management projects", "Homestay network"],
        "local_guides": ["Ladakh Eco Tourism", "Himalayan Brotherhood"],
        "homestays": ["Leh View Homestay", "Nubra Valley Home"],
        "distance_from_delhi": 1000,
        "lat": 34.1526,
        "lon": 77.5771,
        "ar_content": {
            "cultural_info": "1000-year-old Buddhist monasteries preserving Tibetan Buddhism traditions",
            "eco_tips": "Acclimatize properly, carry out all waste, respect monastery rules"
        }
    },
    "andaman": {
        "name": "Andaman Islands",
        "type": ["beach", "adventure", "nature"],
        "eco_score": 8,
        "budget_level": "high",
        "best_season": ["october", "november", "december", "january", "february", "march", "april", "may"],
        "carbon_rating": "high",
        "description": "Pristine islands with coral reef conservation efforts",
        "sustainability_features": ["Coral restoration projects", "Plastic-free beaches", "Marine protected areas"],
        "local_guides": ["Island Green Tours", "Coral Conservation Divers"],
        "homestays": ["Beachside Eco Hut", "Island Life Home"],
        "distance_from_delhi": 3500,
        "lat": 11.6234,
        "lon": 92.7265,
        "ar_content": {
            "cultural_info": "Cellular Jail, a symbol of India's freedom struggle and colonial history",
            "eco_tips": "Don't touch corals while snorkeling, use reef-safe sunscreen, avoid single-use plastic"
        }
    },
    "varanasi": {
        "name": "Varanasi, Uttar Pradesh",
        "type": ["spiritual", "cultural", "heritage"],
        "eco_score": 5,
        "budget_level": "low",
        "best_season": ["october", "november", "december", "january", "february", "march"],
        "carbon_rating": "low",
        "description": "Ancient spiritual city with Ganga conservation initiatives",
        "sustainability_features": ["Ganga cleanup projects", "Heritage walk initiatives", "Local artisan support"],
        "local_guides": ["Varanasi Walks", "Spiritual Banaras Tours"],
        "homestays": ["Ghat View Home", "Old City Heritage Stay"],
        "distance_from_delhi": 800,
        "lat": 25.3176,
        "lon": 82.9739,
        "ar_content": {
            "cultural_info": "One of the oldest continuously inhabited cities, center of Hindu spirituality for 3000+ years",
            "eco_tips": "Support Ganga conservation, buy from local weavers, avoid contributing to ghat pollution"
        }
    },
    "munnar": {
        "name": "Munnar, Kerala",
        "type": ["nature", "relaxation", "adventure"],
        "eco_score": 9,
        "budget_level": "medium",
        "best_season": ["september", "october", "november", "december", "january", "february", "march"],
        "carbon_rating": "low",
        "description": "Tea plantations with sustainable agriculture practices",
        "sustainability_features": ["Organic tea gardens", "Wildlife sanctuaries", "Tribal welfare programs"],
        "local_guides": ["Tea Trail Explorers", "Munnar Nature Walks"],
        "homestays": ["Tea Garden Cottage", "Hill View Homestay"],
        "distance_from_delhi": 2400,
        "lat": 10.0889,
        "lon": 77.0595,
        "ar_content": {
            "cultural_info": "Historic tea estates dating back to 1880s British colonial era",
            "eco_tips": "Buy certified organic tea, respect wildlife in sanctuaries, support tribal communities"
        }
    },
    "goa": {
        "name": "Goa",
        "type": ["beach", "relaxation", "cultural"],
        "eco_score": 6,
        "budget_level": "medium",
        "best_season": ["october", "november", "december", "january", "february", "march"],
        "carbon_rating": "medium",
        "description": "Beach destination with growing eco-tourism initiatives",
        "sustainability_features": ["Beach cleanup drives", "Sustainable seafood", "Heritage village tourism"],
        "local_guides": ["Eco Goa Tours", "Village Trail Goa"],
        "homestays": ["Portuguese Heritage Home", "Beachside Eco Stay"],
        "distance_from_delhi": 1900,
        "ar_content": {
            "cultural_info": "16th century Portuguese churches, UNESCO World Heritage sites blending East-West architecture",
            "eco_tips": "Choose eco-certified beach shacks, avoid disturbing nesting turtles, participate in beach cleanups"
        }
    }
}

# Transport emission factors (kg CO2 per km per person)
TRANSPORT_EMISSIONS = {
    "flight": 0.255,
    "train": 0.041,
    "bus": 0.089,
    "car": 0.171,
    "electric_car": 0.053,
    "bicycle": 0.0
}

# Accommodation emission factors (kg CO2 per night)
ACCOMMODATION_EMISSIONS = {
    "luxury_hotel": 31.0,
    "standard_hotel": 20.9,
    "budget_hotel": 12.5,
    "homestay": 6.0,
    "eco_lodge": 4.5,
    "camping": 2.0
}

# Food emission factors (kg CO2 per day)
FOOD_EMISSIONS = {
    "non_vegetarian": 7.2,
    "mixed": 5.1,
    "vegetarian": 3.8,
    "vegan": 2.9,
    "local_organic": 2.5
}

# Seasonal pricing multipliers
SEASONAL_PRICING = {
    "peak": {"months": [10, 11, 12, 1, 2, 3], "multiplier": 1.5, "label": "Peak Season"},
    "shoulder": {"months": [4, 5, 9], "multiplier": 1.2, "label": "Shoulder Season"},
    "off_peak": {"months": [6, 7, 8], "multiplier": 0.8, "label": "Off-Peak Season"}
}

# Festival periods with premium pricing
FESTIVAL_PERIODS = {
    "diwali": {"month": 10, "weeks": [3, 4], "multiplier": 1.8},
    "christmas": {"month": 12, "weeks": [4], "multiplier": 1.7},
    "new_year": {"month": 1, "weeks": [1], "multiplier": 1.9},
    "holi": {"month": 3, "weeks": [2, 3], "multiplier": 1.4}
}

# UNWTO Sustainable Development Goals mapping
UNWTO_GOALS = {
    "local_economy": "Support local communities and reduce economic leakage",
    "cultural_preservation": "Protect and promote cultural heritage",
    "environmental_protection": "Minimize environmental impact",
    "visitor_education": "Educate tourists on sustainable practices",
    "community_benefit": "Ensure tourism benefits local communities"
}

# ISO 14001 alignment points
ISO_14001_POINTS = {
    "environmental_policy": "Carbon footprint transparency and eco-scoring",
    "planning": "Assessment of environmental impacts before travel",
    "implementation": "Providing greener alternatives for each choice",
    "checking": "Continuous monitoring through eco-scores",
    "management_review": "Feedback loop for improvement recommendations"
}
