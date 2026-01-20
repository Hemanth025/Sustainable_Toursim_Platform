/**
 * Itinerary Map Logic
 * Handles route visualization between user location and destination
 */

document.addEventListener('DOMContentLoaded', () => {
    // Map container check
    const mapContainer = document.getElementById('itinerary-map');
    if (!mapContainer) return;

    // Data from template
    const destLat = parseFloat(mapContainer.dataset.destLat);
    const destLon = parseFloat(mapContainer.dataset.destLon);
    let originLat = parseFloat(mapContainer.dataset.originLat);
    let originLon = parseFloat(mapContainer.dataset.originLon);
    const destName = mapContainer.dataset.destName;

    // Initialize map
    const map = L.map('itinerary-map').setView([destLat, destLon], 10);

    // Tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        className: 'map-tiles'  // Re-using dark mode class if applied globally
    }).addTo(map);

    // Custom Icons
    const destIcon = L.divIcon({
        className: 'custom-div-icon',
        html: `<div style="background-color: #ef4444; width: 30px; height: 30px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.5);"></div>`,
        iconSize: [30, 30]
    });

    const userIcon = L.divIcon({
        className: 'custom-div-icon',
        html: `<div style="background-color: #3b82f6; width: 24px; height: 24px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.5);"></div>`,
        iconSize: [24, 24]
    });

    // Destination Marker
    L.marker([destLat, destLon], { icon: destIcon })
        .addTo(map)
        .bindPopup(`<b>${destName}</b><br>Destination`)
        .openPopup();

    // Route Layer
    let routeLayer = null;

    // If origin is known immediately (passed from server)
    if (!isNaN(originLat) && !isNaN(originLon)) {
        showRoute(originLat, originLon, destLat, destLon);
    } else {
        // Try getting location from browser if not passed
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    originLat = pos.coords.latitude;
                    originLon = pos.coords.longitude;
                    showRoute(originLat, originLon, destLat, destLon);
                },
                (err) => console.log("Location access denied or error")
            );
        }
    }

    // Function to fetch and draw route
    async function showRoute(startLat, startLon, endLat, endLon) {
        // Add user marker
        L.marker([startLat, startLon], { icon: userIcon })
            .addTo(map)
            .bindPopup("Start Point");

        // Fit bounds
        const group = new L.featureGroup([
            L.marker([startLat, startLon]),
            L.marker([endLat, endLon])
        ]);
        map.fitBounds(group.getBounds(), { padding: [50, 50] });

        // Fetch route from OSRM
        try {
            const response = await fetch(`https://router.project-osrm.org/route/v1/driving/${startLon},${startLat};${endLon},${endLat}?overview=full&geometries=geojson`);
            const data = await response.json();

            if (data.routes && data.routes.length > 0) {
                const route = data.routes[0];
                const geometry = route.geometry;

                routeLayer = L.geoJSON(geometry, {
                    style: {
                        color: '#10b981', // Emerald-500
                        weight: 5,
                        opacity: 0.8
                    }
                }).addTo(map);

                // Update info if needed
                const distKm = (route.distance / 1000).toFixed(1);
                console.log(`Route distance: ${distKm} km`);
            }
        } catch (error) {
            console.error("Routing error:", error);
            // Fallback: simple line
            L.polyline([[startLat, startLon], [endLat, endLon]], {
                color: '#94a3b8',
                dashArray: '10, 10'
            }).addTo(map);
        }
    }

    // Handle Travel Mode Selection interactions
    const modeCards = document.querySelectorAll('.travel-mode-card');
    modeCards.forEach(card => {
        card.addEventListener('click', () => {
            // Remove active class from all
            modeCards.forEach(c => c.classList.remove('ring-2', 'ring-eco-400', 'bg-slate-700'));
            modeCards.forEach(c => c.classList.add('bg-slate-800/50'));

            // Add active to click
            card.classList.remove('bg-slate-800/50');
            card.classList.add('bg-slate-700', 'ring-2', 'ring-eco-400');

            // Here we could update simple carbon text depending on selection
            // For now just visual selection
        });
    });
});
