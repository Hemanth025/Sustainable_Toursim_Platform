"""
Geospatial Intelligence Module
Handles OpenStreetMap integration, geocoding, and distance calculations
"""

import requests
import math
from math import radians, cos, sin, asin, sqrt

# Constants for Overpass API
OVERPASS_URL = "http://overpass-api.de/api/interpreter"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
REVERSE_GEOCODE_URL = "https://nominatim.openstreetmap.org/reverse"

# Helper for Haversine distance
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

class GeospatialService:
    """Service for handling all geospatial operations"""
    
    @staticmethod
    def geocode_place(query):
        """
        Search for a place using Nominatim API
        Returns a list of matching locations
        """
        params = {
            'q': query,
            'format': 'json',
            'limit': 5,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'EcoJourney_StudentProject/1.0'
        }
        
        try:
            response = requests.get(NOMINATIM_URL, params=params, headers=headers)
            if response.status_code == 200:
                results = response.json()
                processed_results = []
                
                for res in results:
                    processed_results.append({
                        'name': res.get('display_name').split(',')[0],
                        'full_name': res.get('display_name'),
                        'lat': float(res.get('lat')),
                        'lon': float(res.get('lon')),
                        'type': res.get('type', 'unknown'),
                        'importance': res.get('importance', 0)
                    })
                return processed_results
            return []
        except Exception as e:
            print(f"Geocoding error: {e}")
            return []

    @staticmethod
    def get_nearby_places(lat, lon, radius=5000, place_type='all'):
        """
        Fetch nearby places using Overpass API
        radius in meters (default 5km)
        place_type: 'beach', 'mountain', 'temple', 'park', 'cultural', or 'all'
        """
        # Define Overpass QL queries for different types
        queries = {
            'beach': f"""
                node["natural"="beach"](around:{radius},{lat},{lon});
                way["natural"="beach"](around:{radius},{lat},{lon});
            """,
            'mountain': f"""
                node["natural"="peak"](around:{radius},{lat},{lon});
                node["place"="locality"]["natural"~"mountain|valley"](around:{radius},{lat},{lon});
            """,
            'temple': f"""
                node["amenity"="place_of_worship"](around:{radius},{lat},{lon});
                way["amenity"="place_of_worship"](around:{radius},{lat},{lon});
            """,
            'park': f"""
                node["leisure"="park"](around:{radius},{lat},{lon});
                way["leisure"="nature_reserve"](around:{radius},{lat},{lon});
            """,
            'cultural': f"""
                node["tourism"="museum"](around:{radius},{lat},{lon});
                node["historic"](around:{radius},{lat},{lon});
            """
        }
        
        # Construct the query
        ql_query = "[out:json];("
        if place_type == 'all':
            for q in queries.values():
                ql_query += q
        elif place_type in queries:
            ql_query += queries[place_type]
        ql_query += ");out body;>;out skel qt;"
        
        try:
            response = requests.get(OVERPASS_URL, params={'data': ql_query})
            if response.status_code == 200:
                data = response.json()
                places = []
                
                for element in data.get('elements', []):
                    if 'tags' in element and 'name' in element['tags']:
                        # Determine lat/lon based on element type
                        p_lat = element.get('lat')
                        p_lon = element.get('lon')
                        
                        if not p_lat and 'center' in element:
                             p_lat = element['center']['lat']
                             p_lon = element['center']['lon']
                             
                        if p_lat and p_lon:
                            dist = haversine_distance(lat, lon, p_lat, p_lon)
                            
                            # Determine type tag
                            p_type = 'attraction'
                            tags = element['tags']
                            if 'natural' in tags:
                                p_type = tags['natural']
                            elif 'amenity' in tags:
                                p_type = tags['amenity']
                            elif 'leisure' in tags:
                                p_type = tags['leisure']
                            elif 'tourism' in tags:
                                p_type = tags['tourism']
                                
                            places.append({
                                'name': tags['name'],
                                'lat': p_lat,
                                'lon': p_lon,
                                'type': p_type,
                                'distance_km': round(dist, 2),
                                'category': GeospatialService._categorize_place(tags)
                            })
                
                # Sort by distance
                places.sort(key=lambda x: x['distance_km'])
                return places
            return []
        except Exception as e:
            print(f"Overpass API error: {e}")
            return []

    @staticmethod
    def _categorize_place(tags):
        """Helper to categorize place based on OSM tags"""
        if 'natural' in tags and tags['natural'] == 'beach':
            return 'beach'
        if 'natural' in tags and tags['natural'] == 'peak':
            return 'mountain'
        if 'amenity' in tags and tags['amenity'] == 'place_of_worship':
            return 'temple'
        if 'leisure' in tags and tags['leisure'] in ['park', 'nature_reserve']:
            return 'park'
        if 'tourism' in tags or 'historic' in tags:
            return 'cultural'
        return 'other'

    @staticmethod
    def get_trip_recommendation(distance_km):
        """
        Provide sustainability recommendation based on distance
        """
        if distance_km < 50:
            return {
                'mode': 'Bicycle/Electric Vehicle',
                'impact': 'Very Low',
                'message': 'Great for a local cycling trip or EV drive!'
            }
        elif distance_km < 300:
            return {
                'mode': 'Electric Train/Bus',
                'impact': 'Low',
                'message': 'Perfect distance for a scenic train or bus ride.'
            }
        elif distance_km < 1000:
            return {
                'mode': 'Train',
                'impact': 'Medium',
                'message': 'Consider an overnight train to reduce carbon footprint.'
            }
        else:
            return {
                'mode': 'Train/Direct Flight',
                'impact': 'High',
                'message': 'Long distance - try to stay longer to offset travel carbon.'
            }
