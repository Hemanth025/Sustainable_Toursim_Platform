/**
 * EcoJourney - Main JavaScript
 * Sustainable Tourism Platform
 */

// Utility Functions
const EcoJourney = {
    // Format numbers with commas
    formatNumber: (num) => {
        return new Intl.NumberFormat('en-IN').format(num);
    },

    // Calculate eco score color
    getEcoScoreColor: (score) => {
        if (score >= 8) return '#22c55e'; // Green
        if (score >= 6) return '#eab308'; // Yellow
        if (score >= 4) return '#f97316'; // Orange
        return '#ef4444'; // Red
    },

    // Show notification toast
    showToast: (message, type = 'success') => {
        const toast = document.createElement('div');
        const colors = {
            success: 'bg-eco-500',
            error: 'bg-rose-500',
            info: 'bg-cyan-500'
        };
        
        toast.className = `fixed bottom-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-xl shadow-lg z-50 animate-slide-up`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    },

    // Smooth scroll to element
    scrollTo: (elementId) => {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    },

    // Mobile menu toggle
    initMobileMenu: () => {
        const btn = document.getElementById('mobile-menu-btn');
        const menu = document.getElementById('mobile-menu');
        
        if (btn && menu) {
            btn.addEventListener('click', () => {
                menu.classList.toggle('hidden');
            });
        }
    },

    // Initialize all components
    init: () => {
        EcoJourney.initMobileMenu();
        console.log('🌿 EcoJourney initialized');
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', EcoJourney.init);

// Carbon Calculator Helper
const CarbonCalculator = {
    // Emission factors (kg CO2 per unit)
    factors: {
        transport: {
            flight: 0.255,
            train: 0.041,
            bus: 0.089,
            car: 0.171,
            electric_car: 0.053
        },
        accommodation: {
            luxury_hotel: 31.0,
            standard_hotel: 20.9,
            budget_hotel: 12.5,
            homestay: 6.0,
            eco_lodge: 4.5,
            camping: 2.0
        },
        food: {
            non_vegetarian: 7.2,
            mixed: 5.1,
            vegetarian: 3.8,
            vegan: 2.9,
            local_organic: 2.5
        }
    },

    // Quick calculate (client-side preview)
    quickCalc: (transport, distance, accommodation, nights, food) => {
        const transportEmissions = CarbonCalculator.factors.transport[transport] * distance;
        const accEmissions = CarbonCalculator.factors.accommodation[accommodation] * nights;
        const foodEmissions = CarbonCalculator.factors.food[food] * nights;
        
        return {
            transport: transportEmissions.toFixed(2),
            accommodation: accEmissions.toFixed(2),
            food: foodEmissions.toFixed(2),
            total: (transportEmissions + accEmissions + foodEmissions).toFixed(2)
        };
    }
};

// Eco Score Animation
const animateEcoScore = (element, targetScore) => {
    let current = 0;
    const increment = targetScore / 30;
    
    const animate = () => {
        current += increment;
        if (current < targetScore) {
            element.textContent = Math.round(current);
            requestAnimationFrame(animate);
        } else {
            element.textContent = targetScore;
        }
    };
    
    animate();
};

// Form validation helpers
const FormValidator = {
    isValidNumber: (value, min, max) => {
        const num = parseFloat(value);
        return !isNaN(num) && num >= min && num <= max;
    },

    isRequired: (value) => {
        return value && value.trim() !== '';
    }
};

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { EcoJourney, CarbonCalculator, FormValidator };
}
