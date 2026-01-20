/**
 * EcoJourney Map Logic
 * Handles interactive map, geocoding, and nearby place discovery
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- Configuration ---
    const DEFAULT_COORDS = [20.5937, 78.9629]; // Center of India
    const DEFAULT_ZOOM = 5;
    let map = null;
    let selectedMarker = null;
    let nearbyMarkers = [];
    let currentRadius = 5000; // in meters
    let userLocation = null;
    let userMarker = null;

    // --- Icons ---
    const createIcon = (color, size = 30) => {
        return L.divIcon({
            className: 'custom-div-icon',
            html: `<div style="background-color: ${color}; width: ${size}px; height: ${size}px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.5);"></div>`,
            iconSize: [size, size],
            iconAnchor: [size / 2, size / 2]
        });
    };

    const mainIcon = createIcon('#22c55e', 40); // Green for selected
    const userLocationIcon = L.divIcon({
        className: 'user-location-marker',
        html: `<div class="relative w-6 h-6">
                <div class="absolute w-6 h-6 bg-blue-500 rounded-full border-2 border-white shadow-lg z-10"></div>
                <div class="absolute w-6 h-6 bg-blue-500 rounded-full opacity-50 animate-ping"></div>
               </div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    });

    const beachIcon = createIcon('#3b82f6');     // Blue
    const mountainIcon = createIcon('#78350f');  // Brown
    const templeIcon = createIcon('#f59e0b');    // Orange
    const parkIcon = createIcon('#16a34a');      // Dark Green
    const culturalIcon = createIcon('#8b5cf6');  // Purple

    // --- Initialization ---
    // Initialize map
    map = L.map('map').setView(DEFAULT_COORDS, DEFAULT_ZOOM);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19,
        className: 'map-tiles'
    }).addTo(map);

    // Dark mode filter for map
    const style = document.createElement('style');
    style.innerHTML = `
        .leaflet-layer { filter: brightness(0.6) invert(1) contrast(3) hue-rotate(200deg) saturate(0.3) brightness(0.7); }
        .leaflet-control-attribution { background: rgba(0,0,0,0.5) !important; color: #aaa !important; }
        .leaflet-container { background: #0f172a; }
        .user-location-popup .leaflet-popup-content-wrapper { background: #1e293b; color: white; border-radius: 12px; }
        .user-location-popup .leaflet-popup-tip { background: #1e293b; }
    `;
    document.head.appendChild(style);

    // Request User Location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLocation = {
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                };

                // Add user marker
                userMarker = L.marker([userLocation.lat, userLocation.lon], { icon: userLocationIcon })
                    .addTo(map)
                    .bindPopup("You are here", { className: 'user-location-popup' });

                // Fly to user
                map.flyTo([userLocation.lat, userLocation.lon], 10);
            },
            () => {
                console.log('Location permission denied');
                // Could retry or show message
            }
        );
    }

    // --- Event Listeners ---

    // Map Click
    map.on('click', async (e) => {
        const { lat, lng } = e.latlng;
        handleLocationSelect(lat, lng);
    });

    // Search Box
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    let debounceTimer;

    searchInput.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        const query = e.target.value.trim();

        if (query.length < 3) {
            searchResults.classList.add('hidden');
            return;
        }

        debounceTimer = setTimeout(() => {
            performSearch(query);
        }, 500);
    });

    // AI Recommendation Logic
    const aiInput = document.getElementById('ai-input');
    const aiBtn = document.getElementById('ai-btn');
    const aiResults = document.getElementById('ai-results');

    const handleAIRequest = async () => {
        const query = aiInput.value.trim();
        if (!query) return;

        aiBtn.innerHTML = '<span class="animate-spin">↻</span>';

        try {
            const response = await fetch('/api/ai-recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            const results = await response.json();

            displayAIResults(results);
        } catch (error) {
            console.error('AI Recommend failed:', error);
        } finally {
            aiBtn.innerHTML = '✨';
        }
    };

    aiBtn.addEventListener('click', handleAIRequest);
    aiInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleAIRequest();
    });

    function displayAIResults(results) {
        aiResults.innerHTML = '';
        if (results.length === 0) {
            aiResults.innerHTML = '<p class="text-xs text-gray-400 italic">No matches found. Try describing "mountains" or "beaches".</p>';
            aiResults.classList.remove('hidden');
            return;
        }

        results.forEach(res => {
            const div = document.createElement('div');
            div.className = 'bg-slate-700/50 p-2 rounded-lg border border-white/5 hover:border-eco-500/50 cursor-pointer transition-all group';
            div.innerHTML = `
                <div class="flex justify-between items-start">
                    <h4 class="text-sm font-bold text-white group-hover:text-eco-400">${res.name}</h4>
                    <span class="text-[10px] bg-eco-900/50 text-eco-400 px-1.5 py-0.5 rounded">${res.match_score}% Match</span>
                </div>
                <p class="text-[11px] text-gray-400 line-clamp-2 mt-1">${res.description}</p>
            `;

            div.addEventListener('click', () => {
                performSearch(res.name).then(() => {
                    const searchInput = document.getElementById('search-input');
                    searchInput.value = res.name;
                    // Trigger search explicitly to show dropdown
                    searchInput.dispatchEvent(new Event('input'));
                });
            });

            aiResults.appendChild(div);
        });
        aiResults.classList.remove('hidden');
    }

    // Filters
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Toggle active state if needed, currently just one active
            // For now let's just trigger nearby search with this type
            const type = btn.dataset.type;
            if (selectedMarker) {
                const latlng = selectedMarker.getLatLng();
                fetchNearbyPlaces(latlng.lat, latlng.lng, currentRadius, type);
            } else {
                // Suggest clicking somewhere first
                alert('Please select a location on the map first.');
            }
        });
    });

    // Radius Slider
    const radiusSlider = document.getElementById('radius-slider');
    const radiusValue = document.getElementById('radius-value');

    radiusSlider.addEventListener('input', (e) => {
        const val = e.target.value;
        currentRadius = val * 1000;
        radiusValue.textContent = `${val} km`;

        if (selectedMarker) {
            const latlng = selectedMarker.getLatLng();
            // Re-fetch nearby places with new radius
            // Debounce this too
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                fetchNearbyPlaces(latlng.lat, latlng.lng, currentRadius, 'all');
            }, 300);
        }
    });

    // Plan Trip Button
    document.getElementById('plan-trip-btn').addEventListener('click', () => {
        // Redirect to itinerary with dynamic destination
        if (selectedMarker) {
            const name = document.getElementById('panel-title').innerText;
            const latlng = selectedMarker.getLatLng();

            // Build query params
            const params = new URLSearchParams({
                destination: name,
                lat: latlng.lat,
                lon: latlng.lng,
            });

            if (userLocation) {
                params.append('origin_lat', userLocation.lat);
                params.append('origin_lon', userLocation.lon);

                // Get pre-calculated distance
                const distText = document.getElementById('panel-distance').innerText;
                const dist = parseFloat(distText.split(' ')[0]);
                if (!isNaN(dist)) {
                    params.append('distance', dist);
                }
            }

            // Redirect to generic itinerary or planner
            // Since standard route is /itinerary/<id>, we might need a special handler
            // or we use /planner with pre-filled inputs
            // Let's use a new route /plan-custom which we'll add to app.py
            window.location.href = `/plan-custom?${params.toString()}`;
        }
    });

    document.getElementById('close-panel').addEventListener('click', () => {
        document.getElementById('destination-panel').classList.remove('translate-y-0', 'opacity-100');
        document.getElementById('destination-panel').classList.add('translate-y-full', 'opacity-0');
        setTimeout(() => {
            document.getElementById('destination-panel').style.display = 'none';
        }, 300);
    });


    // --- Functions ---

    async function performSearch(query) {
        try {
            const response = await fetch('/api/geocode', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            const results = await response.json();

            displaySearchResults(results);
        } catch (error) {
            console.error('Search failed:', error);
        }
    }

    function displaySearchResults(results) {
        searchResults.innerHTML = '';
        if (results.length === 0) {
            searchResults.classList.add('hidden');
            return;
        }

        results.forEach(res => {
            const div = document.createElement('div');
            div.className = 'px-4 py-3 hover:bg-slate-700 cursor-pointer border-b border-slate-700 last:border-0';
            div.innerHTML = `
                <p class="text-white text-sm font-medium">${res.name}</p>
                <p class="text-gray-400 text-xs truncate">${res.full_name}</p>
            `;
            div.addEventListener('click', () => {
                handleLocationSelect(res.lat, res.lon, res.name);
                searchResults.classList.add('hidden');
                searchInput.value = res.name;
            });
            searchResults.appendChild(div);
        });

        searchResults.classList.remove('hidden');
    }

    async function handleLocationSelect(lat, lon, name = null) {
        // Center map
        map.setView([lat, lon], 12);

        // Remove old markers
        if (selectedMarker) map.removeLayer(selectedMarker);
        nearbyMarkers.forEach(m => map.removeLayer(m));
        nearbyMarkers = [];

        // Add new marker
        selectedMarker = L.marker([lat, lon], { icon: mainIcon }).addTo(map);

        // Name placeholder if geocoding delayed/skipped
        const displayName = name || "Selected Coordinates";

        // Show panel
        updatePanel(displayName, lat, lon);

        // Calculate distance if user location known
        if (userLocation) {
            calculateDistance(userLocation.lat, userLocation.lon, lat, lon);
        } else {
            document.getElementById('panel-distance').textContent = "Unknown";
            document.getElementById('eco-message').textContent = "Enable location services to see eco-travel advice.";
        }

        // Fetch nearby places
        fetchNearbyPlaces(lat, lon, currentRadius);
    }

    function updatePanel(name, lat, lon) {
        const panel = document.getElementById('destination-panel');
        document.getElementById('panel-title').textContent = name;
        document.getElementById('panel-coords').textContent = `${lat.toFixed(4)}, ${lon.toFixed(4)}`;

        panel.style.display = 'block';
        // Force reflow
        void panel.offsetWidth;
        panel.classList.remove('translate-y-full', 'opacity-0');
        panel.classList.add('translate-y-0', 'opacity-100');
    }

    async function calculateDistance(lat1, lon1, lat2, lon2) {
        try {
            const response = await fetch('/api/calculate-distance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat1, lon1, lat2, lon2 })
            });
            const data = await response.json();

            document.getElementById('panel-distance').textContent = `${data.distance_km} km`;
            document.getElementById('eco-message').textContent = data.recommendation.message;
        } catch (error) {
            console.error('Distance calc failed:', error);
        }
    }

    async function fetchNearbyPlaces(lat, lon, radius, type = 'all') {
        try {
            // Show loading state...

            const response = await fetch('/api/nearby-places', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat, lon, radius, type })
            });
            const places = await response.json();

            // clear existing nearby markers
            nearbyMarkers.forEach(m => map.removeLayer(m));
            nearbyMarkers = [];

            // Add markers
            places.forEach(place => {
                let icon = parkIcon;
                if (place.category === 'beach') icon = beachIcon;
                if (place.category === 'mountain') icon = mountainIcon;
                if (place.category === 'temple') icon = templeIcon;
                if (place.category === 'cultural') icon = culturalIcon;

                const marker = L.marker([place.lat, place.lon], { icon: icon })
                    .bindPopup(`
                        <div class="p-2 text-slate-800 text-center">
                            <h3 class="font-bold">${place.name}</h3>
                            <p class="text-xs text-slate-600 capitalize mb-2">${place.category}</p>
                            <p class="text-xs text-slate-500 mb-2">${place.distance_km} km away</p>
                            <button onclick="window.selectNearbyLocation(${place.lat}, ${place.lon}, '${place.name.replace(/'/g, "\\'")}')" 
                                class="bg-eco-500 text-white text-xs px-3 py-1 rounded hover:bg-eco-600 transition-colors">
                                Select Destination
                            </button>
                        </div>
                    `);

                marker.addTo(map);
                nearbyMarkers.push(marker);
            });

            document.getElementById('panel-spots').textContent = places.length;

        } catch (error) {
            console.error('Nearby places fetch failed:', error);
        }
    }
});
