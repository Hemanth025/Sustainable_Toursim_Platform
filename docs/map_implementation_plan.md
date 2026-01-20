# Intelligent Map-Based Destination Selection

Build a dataset-free, scalable map-based destination selection feature using OpenStreetMap, Nominatim geocoding, and Overpass API for real-time geospatial intelligence. The system will enable users to search and click on a map to select destinations, discover 1000+ nearby places dynamically, calculate distances, and seamlessly redirect to the itinerary page with sustainability-focused recommendations.

## User Review Required

> [!IMPORTANT]
> **Geospatial API Selection**: This implementation uses free, open-source APIs:
> - **OpenStreetMap** with **Leaflet.js** for map visualization
> - **Nominatim API** for geocoding and place search (free, no API key required)
> - **Overpass API** for fetching nearby places by category (beaches, mountains, temples, parks, cultural sites)
> 
> These APIs have rate limits but are sufficient for development and academic use. For production deployment, you may want to consider self-hosting Nominatim or using cached results.

> [!IMPORTANT]
> **Distance Calculation**: Using the **Haversine formula** for great-circle distance calculation between coordinates. This is mathematically explainable and aligns with sustainability goals by showing users the actual travel distance to encourage nearby exploration.

> [!WARNING]
> **No Breaking Changes**: This feature integrates cleanly without modifying existing functionality. The map page is a new standalone feature that redirects to the existing itinerary flow.

## Proposed Changes

### Backend - Geospatial Service Module

#### [NEW] [geospatial_service.py](file:///c:/Users/DELL/Sustainable_Tourism/modules/geospatial_service.py)

Create a new module for all geospatial intelligence operations:

- **Geocoding Service**: Search destinations using Nominatim API
  - Convert place names to coordinates
  - Return formatted results with name, coordinates, type, and display name
  
- **Nearby Places Discovery**: Fetch places using Overpass API
  - Support 5 categories: beach, mountain, temple, park, cultural attractions
  - Query within configurable radius (default 50km)
  - Handle 1000+ results efficiently
  - Return structured data with name, type, coordinates, and distance
  
- **Distance Calculation**: Haversine formula implementation
  - Calculate great-circle distance between two coordinate pairs
  - Return distance in kilometers with sustainability context
  - Provide eco-friendly travel recommendations based on distance
  
- **Sustainability Scoring**: Rule-based logic for place recommendations
  - Score places based on distance (closer = better)
  - Prioritize eco-certified locations
  - Suggest sustainable transportation options

---

### Backend - Flask Routes

#### [MODIFY] [app.py](file:///c:/Users/DELL/Sustainable_Tourism/app.py)

Add new routes for map functionality:

- **`/map` (GET)**: Render the map UI page
  - Check authentication
  - Render `map.html` template
  
- **`/api/geocode` (POST)**: Search for destinations
  - Accept search query from frontend
  - Call Nominatim geocoding service
  - Return JSON with search results
  
- **`/api/nearby-places` (POST)**: Fetch nearby attractions
  - Accept coordinates and place types
  - Query Overpass API for nearby places
  - Calculate distances for each place
  - Return sorted results (closest first)
  
- **`/api/calculate-distance` (POST)**: Calculate distance between two points
  - Accept origin and destination coordinates
  - Use Haversine formula
  - Return distance with sustainability insights
  
- **`/api/calculate-distance` (POST)**: Calculate distance between two points
  - Accept origin and destination coordinates
  - Use Haversine formula
  - Return distance with sustainability insights
  
- **`/api/calculate-distance` (POST)**: Calculate distance between two points
  - Accept origin and destination coordinates
  - Use Haversine formula
  - Return distance with sustainability insights

Update navigation in `base.html` to include Map link.

---

### Frontend - Map UI Page

#### [NEW] [map.html](file:///c:/Users/DELL/Sustainable_Tourism/Templates/map.html)

Create an interactive map interface with:

- **Map Container**: Full-screen Leaflet.js map with OpenStreetMap tiles
  - Interactive pan and zoom
  - Click-to-select destination functionality
  - Custom markers for selected location and nearby places
  
- **Search Panel**: Glassmorphic sidebar with:
  - Search input with autocomplete suggestions
  - Place type filters (beach, mountain, temple, park, cultural)
  - Distance radius slider
  - Results list with place cards
  
- **Destination Preview**: Bottom panel showing:
  - Selected destination details
  - Distance from user location (if available)
  - Nearby attractions count by category
  - "Plan Trip" button to redirect to itinerary
  
- **Sustainability Indicators**:
  - Eco-score visualization for each place
  - Distance-based carbon footprint estimate
  - Nearby exploration encouragement

---

### Frontend - Map JavaScript

#### [NEW] [map.js](file:///c:/Users/DELL/Sustainable_Tourism/static/js/map.js)

Implement all map interactions:

- **Map Initialization**:
  - Initialize Leaflet map with OpenStreetMap tiles
  - Set default view to India (center coordinates)
  - Add zoom controls and scale
  
- **Search Functionality**:
  - Debounced search input to prevent excessive API calls
  - Fetch geocoding results from `/api/geocode`
  - Display results in dropdown/list
  - Handle result selection
  
- **Click-to-Select**:
  - Add click event listener to map
  - Place marker at clicked location
  - Reverse geocode to get place name
  - Fetch nearby places automatically
  
- **Nearby Places Visualization**:
  - Fetch places from `/api/nearby-places`
  - Add color-coded markers by category
  - Create marker clusters for better performance
  - Show place details on marker click
  
- **Distance Calculation**:
  - Get user's current location (with permission)
  - Calculate distance to selected destination
  - Display in UI with sustainability context
  
- **Redirection to Itinerary**:
  - Store selected destination in session
  - Redirect to `/itinerary/<destination_id>` or create dynamic itinerary
  - Pass location data and nearby places

---

### Frontend - Navigation Update

#### [MODIFY] [base.html](file:///c:/Users/DELL/Sustainable_Tourism/Templates/base.html)

Add "Map Explorer" link to navigation:
- Desktop navigation (line ~183)
- Mobile navigation (line ~269)
- Use map icon from heroicons

## Verification Plan

### Automated Tests

Due to the nature of this feature (external API integration and browser-based map interaction), automated unit tests would require mocking external APIs. Instead, we'll focus on comprehensive manual testing with clear steps.

### Manual Verification

#### 1. Map Page Access and Rendering
```
1. Start the Flask application: python app.py
2. Navigate to http://localhost:5000/map
3. Verify:
   - Map loads with OpenStreetMap tiles
   - Search panel is visible on the left
   - Map is interactive (can pan and zoom)
   - No console errors in browser DevTools
```

#### 2. Search Functionality
```
1. On the map page, enter "Manali" in the search box
2. Verify:
   - Search results appear below the input
   - Results show place names and locations
   - Clicking a result centers the map on that location
   - A marker appears at the selected location
3. Try searching for "Kerala", "Goa", "Ladakh"
4. Verify each search works correctly
```

#### 3. Click-to-Select Destination
```
1. Click anywhere on the map
2. Verify:
   - A marker appears at the clicked location
   - The location coordinates are captured
   - Nearby places are automatically fetched
   - Loading indicator shows while fetching
```

#### 4. Nearby Places Discovery (1000+ places)
```
1. Select a destination (e.g., search for "Mumbai")
2. Check the place type filters (beach, mountain, temple, park, cultural)
3. Select "temple" filter
4. Verify:
   - Nearby temples appear as markers on the map
   - Results list shows temple names and distances
   - Can handle and display many results (test with 100+ places)
   - Markers are color-coded by category
5. Repeat with other categories
```

#### 5. Distance Calculation
```
1. Allow browser to access your location (when prompted)
2. Select a destination on the map
3. Verify:
   - Distance from your location to destination is displayed
   - Distance is shown in kilometers
   - Sustainability message appears (e.g., "Consider train travel for distances over 500km")
```

#### 6. Redirection to Itinerary
```
1. Select a destination on the map
2. Click the "Plan Trip" or "View Itinerary" button
3. Verify:
   - Redirects to the itinerary page
   - Destination information is passed correctly
   - Nearby places are displayed on the itinerary
   - No errors occur during transition
```

#### 7. Sustainability Alignment
```
1. Select multiple destinations at varying distances
2. Verify:
   - Closer destinations are highlighted/prioritized
   - Eco-friendly travel suggestions appear
   - Carbon footprint estimates are shown
   - System encourages nearby exploration
```

#### 8. Responsive Design
```
1. Test the map page on different screen sizes:
   - Desktop (1920x1080)
   - Tablet (768x1024)
   - Mobile (375x667)
2. Verify:
   - Map and search panel adapt to screen size
   - All features remain accessible
   - Touch interactions work on mobile
```

#### 9. Performance with Large Datasets
```
1. Select a major city (e.g., "Delhi")
2. Fetch all place types simultaneously
3. Verify:
   - Page remains responsive
   - Markers load progressively
   - No browser freezing or crashes
   - Can handle 1000+ results
```

#### 10. Error Handling
```
1. Test with invalid searches (e.g., "xyzabc123")
2. Test with network disconnected
3. Test with location permission denied
4. Verify:
   - Appropriate error messages appear
   - Application doesn't crash
   - User can recover and try again
```

### User Acceptance Testing

After implementation, please test the following user journey:

1. **Discovery**: Navigate to the Map page from the main navigation
2. **Search**: Search for your desired destination
3. **Explore**: View nearby attractions by category
4. **Select**: Click on a destination to select it
5. **Plan**: Click to view the itinerary for that destination
6. **Verify**: Confirm that the itinerary includes nearby places and sustainability recommendations

Please provide feedback on:
- Ease of use and intuitiveness
- Map performance and responsiveness
- Accuracy of nearby places
- Usefulness of sustainability indicators
- Any bugs or unexpected behavior
