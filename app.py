"""
AI-Powered Sustainable Tourism Platform
Flask Backend Application
Capstone Phase 2 Project

Features:
- Rule-based AI recommendations
- Carbon footprint calculator
- Dynamic pricing insights
- WebAR cultural engagement
- Local economy integration
- User Authentication with OTP
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, make_response
from datetime import datetime, timedelta
import os
import secrets

# Import custom modules
from modules.recommendation_engine import get_recommendations, generate_itinerary
from modules.carbon_calculator import calculate_total_footprint, get_destination_carbon_info
from modules.pricing_engine import (
    get_current_season, 
    calculate_price_level, 
    get_best_time_to_book,
    get_pricing_comparison
)
from modules.knowledge_base import DESTINATIONS, UNWTO_GOALS, ISO_14001_POINTS
from modules.auth_module import (
    create_user,
    verify_user_otp,
    authenticate_user,
    verify_login_otp,
    request_password_reset,
    reset_password,
    check_unique,
    resend_otp,
    validate_password_strength,
    login_required,
    get_current_user,
    set_remember_token,
    get_user_by_remember_token,
    clear_remember_token,
    init_database,
    get_user_details
)
from modules.user_module import get_user_history, add_user_history
from modules.geospatial_service import GeospatialService
from modules.ai_recommendation import AIRecommender

# Initialize AI Recommender
ai_recommender = None # Lazy init to ensure DESTINATIONS are loaded


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Initialize database on startup
try:
    init_database()
except Exception as e:
    print(f"Database initialization skipped: {e}")

# Initialize AI Model
try:
    ai_recommender = AIRecommender(DESTINATIONS)
    print("AI Recommendation Engine Initialized")
except Exception as e:
    print(f"AI Engine Init Failed: {e}")


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/welcome')
def welcome():
    """Landing page for unauthenticated users"""
    # If already logged in, redirect to home
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('welcome.html', current_year=datetime.now().year)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validate all fields are present
        if not all([first_name, last_name, username, email, phone, password]):
            flash('All fields are required.', 'error')
            return render_template('signup.html')
        
        # Validate password match
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')
        
        # Validate password strength
        is_valid, errors, _ = validate_password_strength(password)
        if not is_valid:
            flash(errors[0], 'error')
            return render_template('signup.html')
        
        # Create user
        success, message, user_id = create_user(first_name, last_name, username, email, phone, password)
        
        if success:
            # message contains the OTP for simulated verification
            session['pending_verification'] = {
                'identifier': email,
                'otp': message  # The OTP code
            }
            return render_template('verify_otp.html', 
                                 otp=message,  # Display OTP for testing
                                 identifier=email,
                                 verify_url='verify_signup',
                                 verification_type='signup')
        else:
            flash(message, 'error')
            return render_template('signup.html')
    
    return render_template('signup.html')


@app.route('/signup/verify', methods=['POST'])
def verify_signup():
    """Verify OTP for signup"""
    identifier = request.form.get('identifier', '')
    otp = request.form.get('otp', '')
    
    success, message = verify_user_otp(identifier, otp)
    
    if success:
        flash('Account verified successfully! Please sign in.', 'success')
        return redirect(url_for('signin'))
    else:
        flash(message, 'error')
        # Return to OTP page with error
        pending = session.get('pending_verification', {})
        return render_template('verify_otp.html',
                             identifier=identifier,
                             otp=pending.get('otp'),
                             verify_url='verify_signup',
                             verification_type='signup')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """User login"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    # Check for remember me cookie
    remembered_identifier = request.cookies.get('remember_identifier', '')
    
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me') == 'on'
        
        if not identifier or not password:
            flash('Please enter your credentials.', 'error')
            return render_template('SignIn.html', remembered_identifier=remembered_identifier)
        
        # Authenticate user
        success, message, user_data, otp = authenticate_user(identifier, password)
        
        if success and user_data:
            # Store pending login for MFA
            session['pending_login'] = {
                'user': user_data,
                'otp': otp,
                'remember_me': remember_me
            }
            return render_template('verify_otp.html',
                                 otp=otp,  # Display OTP for testing
                                 identifier=identifier,
                                 user_id=user_data['id'],
                                 verify_url='verify_signin',
                                 verification_type='login')
        else:
            flash(message, 'error')
            return render_template('SignIn.html', remembered_identifier=remembered_identifier)
    
    return render_template('SignIn.html', remembered_identifier=remembered_identifier)


@app.route('/signin/verify', methods=['POST'])
def verify_signin():
    """Verify MFA OTP for signin"""
    user_id = request.form.get('user_id', '')
    otp = request.form.get('otp', '')
    
    pending = session.get('pending_login', {})
    
    if not user_id or not pending:
        flash('Session expired. Please sign in again.', 'error')
        return redirect(url_for('signin'))
    
    success, message = verify_login_otp(int(user_id), otp)
    
    if success:
        user_data = pending.get('user', {})
        remember_me = pending.get('remember_me', False)
        
        # Set session
        session.permanent = True
        session['user_id'] = user_data.get('id')
        session['username'] = user_data.get('username')
        session['email'] = user_data.get('email')
        session['first_name'] = user_data.get('first_name')
        session['last_name'] = user_data.get('last_name')
        
        # Clear pending login
        session.pop('pending_login', None)
        
        # Handle remember me
        response = make_response(redirect(url_for('index')))
        if remember_me:
            # Set cookie for 30 days
            response.set_cookie('remember_identifier', 
                              user_data.get('email', ''), 
                              max_age=30*24*60*60,
                              httponly=True)
            # Also set a remember token
            token = secrets.token_urlsafe(32)
            set_remember_token(user_data.get('id'), token)
            response.set_cookie('remember_token', token, max_age=30*24*60*60, httponly=True)
        
        flash(f'Welcome back, {user_data.get("first_name")}!', 'success')
        return response
    else:
        flash(message, 'error')
        return render_template('verify_otp.html',
                             identifier=pending.get('user', {}).get('email'),
                             otp=pending.get('otp'),
                             user_id=user_id,
                             verify_url='verify_signin',
                             verification_type='login')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Request password reset"""
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        
        if not identifier:
            flash('Please enter your email or username.', 'error')
            return render_template('forgot_password.html')
        
        success, message, otp = request_password_reset(identifier)
        
        if success:
            session['reset_identifier'] = identifier
            return render_template('reset_password.html',
                                 identifier=identifier,
                                 otp=otp)  # Display OTP for testing
        else:
            flash(message, 'error')
            return render_template('forgot_password.html')
    
    return render_template('forgot_password.html')


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password_route():
    """Reset password with OTP"""
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        otp = request.form.get('otp', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if new_password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html', identifier=identifier)
        
        success, message = reset_password(identifier, otp, new_password)
        
        if success:
            flash('Password reset successfully! Please sign in with your new password.', 'success')
            return redirect(url_for('signin'))
        else:
            flash(message, 'error')
            return render_template('reset_password.html', identifier=identifier)
    
    # GET request - need identifier from session
    identifier = session.get('reset_identifier', '')
    if not identifier:
        return redirect(url_for('forgot_password'))
    
    return render_template('reset_password.html', identifier=identifier)


@app.route('/logout')
def logout():
    """User logout"""
    user_id = session.get('user_id')
    
    # Clear remember token
    if user_id:
        clear_remember_token(user_id)
    
    # Clear session
    session.clear()
    
    # Clear cookies
    response = make_response(redirect(url_for('welcome')))
    response.delete_cookie('remember_identifier')
    response.delete_cookie('remember_token')
    
    flash('You have been logged out successfully.', 'success')
    return response


@app.route('/profile')
@login_required
def profile():
    """User Profile Page"""
    user_id = session.get('user_id')
    user = get_user_details(user_id)
    history = get_user_history(user_id)
    
    return render_template('profile.html', user=user, history=history)


# ==================== API ENDPOINTS FOR AUTH ====================

@app.route('/api/check-unique', methods=['POST'])
def api_check_unique():
    """Check if a field value is unique"""
    data = request.get_json()
    field = data.get('field', '')
    value = data.get('value', '')
    
    is_unique, message = check_unique(field, value)
    
    return jsonify({
        'is_unique': is_unique,
        'message': message
    })


@app.route('/api/resend-otp', methods=['POST'])
def api_resend_otp():
    """Resend OTP code"""
    data = request.get_json()
    identifier = data.get('identifier', '')
    
    success, message, otp = resend_otp(identifier)
    
    return jsonify({
        'success': success,
        'message': message,
        'otp': otp if success else None  # For simulated testing
    })


# ==================== MIDDLEWARE ====================

@app.before_request
def check_authentication():
    """Check authentication for protected routes"""
    # Public routes that don't require authentication
    public_routes = [
        'welcome', 'signin', 'signup', 'verify_signup', 'verify_signin',
        'forgot_password', 'reset_password_route', 'logout',
        'api_check_unique', 'api_resend_otp', 'static'
    ]
    
    # Check if route requires auth
    if request.endpoint and request.endpoint not in public_routes:
        if 'user_id' not in session:
            # Check for remember token
            remember_token = request.cookies.get('remember_token')
            if remember_token:
                user = get_user_by_remember_token(remember_token)
                if user:
                    session.permanent = True
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['email'] = user['email']
                    session['first_name'] = user['first_name']
                    session['last_name'] = user['last_name']
                    return  # Allow access
            
            # Redirect to welcome page
            return redirect(url_for('welcome'))


@app.context_processor
def inject_user():
    """Inject current user into all templates"""
    return {
        'current_user': get_current_user(),
        'is_authenticated': 'user_id' in session
    }


# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Landing page with feature overview"""
    return render_template('index.html', 
                         destinations=list(DESTINATIONS.values())[:4],
                         current_year=datetime.now().year)


@app.route('/planner', methods=['GET', 'POST'])
def planner():
    """Multi-step travel planner with rule-based recommendations"""
    if request.method == 'POST':
        # Get form data
        budget = request.form.get('budget', 'medium')
        travel_type = request.form.get('travel_type', 'nature')
        duration = int(request.form.get('duration', 5))
        sustainability = int(request.form.get('sustainability', 7))
        
        # Get recommendations using rule-based engine
        recommendations = get_recommendations(budget, travel_type, duration, sustainability)
        
        # Store in session for itinerary generation (no DB storage)
        session['last_search'] = {
            'budget': budget,
            'travel_type': travel_type,
            'duration': duration,
            'sustainability': sustainability
        }
        
        return render_template('planner.html', 
                             recommendations=recommendations,
                             search_params=session['last_search'],
                             step='results')
    
    return render_template('planner.html', step='form')


@app.route('/itinerary/<destination_id>')
def itinerary(destination_id):
    """Generate and display personalized itinerary"""
    # Get search params from session or use defaults
    params = session.get('last_search', {
        'budget': 'medium',
        'duration': 5,
        'sustainability': 7
    })
    
    # Generate itinerary using rule-based logic
    itinerary_data = generate_itinerary(
        destination_id,
        params['duration'],
        params['budget'],
        params['sustainability']
    )
    
    if itinerary_data:
        # Ensure origin is set for distance calc (Default to Delhi if unknown)
        itinerary_data['origin_lat'] = 28.6139
        itinerary_data['origin_lon'] = 77.2090
    
    if not itinerary_data:
        return render_template('error.html', message="Destination not found"), 404
    
    # Get carbon info for the destination
    carbon_info = get_destination_carbon_info(destination_id)
    
    # Get pricing info
    pricing_info = get_best_time_to_book(destination_id)
    
    # Record history if logged in
    if 'user_id' in session:
        dest_name = DESTINATIONS.get(destination_id, {}).get('name', 'Unknown Destination')
        add_user_history(session['user_id'], dest_name, destination_id)

    return render_template('itinerary.html',
                         itinerary=itinerary_data,
                         carbon_info=carbon_info,
                         pricing_info=pricing_info,
                         destination=DESTINATIONS.get(destination_id))


@app.route('/carbon', methods=['GET', 'POST'])
def carbon():
    """Environmental impact calculator"""
    result = None
    
    if request.method == 'POST':
        # Get calculator inputs
        transport = request.form.get('transport', 'train')
        distance = float(request.form.get('distance', 500))
        accommodation = request.form.get('accommodation', 'standard_hotel')
        nights = int(request.form.get('nights', 3))
        food = request.form.get('food', 'mixed')
        passengers = int(request.form.get('passengers', 1))
        
        # Calculate using fixed emission factors
        result = calculate_total_footprint(
            transport, distance, accommodation, nights, food, passengers
        )
    
    return render_template('carbon.html', 
                         result=result,
                         iso_points=ISO_14001_POINTS)


@app.route('/pricing')
def pricing():
    """Dynamic pricing insights page"""
    # Get current season info
    season = get_current_season()
    
    # Get pricing comparison for all destinations
    all_dest_ids = list(DESTINATIONS.keys())
    comparison = get_pricing_comparison(all_dest_ids)
    
    # Get detailed analysis for featured destinations
    featured_analyses = []
    for dest_id in list(DESTINATIONS.keys())[:4]:
        analysis = get_best_time_to_book(dest_id)
        if analysis:
            featured_analyses.append(analysis)
    
    return render_template('pricing.html',
                         season=season,
                         comparison=comparison,
                         analyses=featured_analyses)


@app.route('/local')
def local():
    """Local economy integration showcase"""
    # Aggregate local guides and homestays from all destinations
    local_data = {
        'guides': [],
        'homestays': [],
        'destinations': []
    }
    
    for dest_id, dest in DESTINATIONS.items():
        dest_summary = {
            'id': dest_id,
            'name': dest['name'],
            'eco_score': dest['eco_score'],
            'sustainability_features': dest['sustainability_features'],
            'local_guides': dest['local_guides'],
            'homestays': dest['homestays']
        }
        local_data['destinations'].append(dest_summary)
        
        for guide in dest['local_guides']:
            local_data['guides'].append({
                'name': guide,
                'destination': dest['name'],
                'eco_score': dest['eco_score']
            })
        
        for homestay in dest['homestays']:
            local_data['homestays'].append({
                'name': homestay,
                'destination': dest['name'],
                'eco_score': dest['eco_score']
            })
    
    return render_template('local.html',
                         local_data=local_data,
                         unwto_goals=UNWTO_GOALS)


@app.route('/ar')
def ar():
    """WebAR cultural engagement page"""
    # Prepare AR content from destinations
    ar_destinations = []
    for dest_id, dest in DESTINATIONS.items():
        ar_destinations.append({
            'id': dest_id,
            'name': dest['name'],
            'cultural_info': dest['ar_content']['cultural_info'],
            'eco_tips': dest['ar_content']['eco_tips']
        })
    
    return render_template('ar.html', destinations=ar_destinations)


# ==================== API ENDPOINTS ====================

@app.route('/api/recommendations', methods=['POST'])
def api_recommendations():
    """API endpoint for AJAX recommendations"""
    data = request.get_json()
    
    recommendations = get_recommendations(
        data.get('budget', 'medium'),
        data.get('travel_type', 'nature'),
        int(data.get('duration', 5)),
        int(data.get('sustainability', 7))
    )
    
    return jsonify({'recommendations': recommendations})


@app.route('/api/carbon', methods=['POST'])
def api_carbon():
    """API endpoint for carbon calculations"""
    data = request.get_json()
    
    result = calculate_total_footprint(
        data.get('transport', 'train'),
        float(data.get('distance', 500)),
        data.get('accommodation', 'standard_hotel'),
        int(data.get('nights', 3)),
        data.get('food', 'mixed'),
        int(data.get('passengers', 1))
    )
    
    return jsonify(result)


@app.route('/api/pricing/<destination_id>')
def api_pricing(destination_id):
    """API endpoint for pricing analysis"""
    analysis = get_best_time_to_book(destination_id)
    
    if not analysis:
        return jsonify({'error': 'Destination not found'}), 404
    
    return jsonify(analysis)


@app.route('/api/ai-recommend', methods=['POST'])
def api_ai_recommend():
    """API endpoint for AI-based recommendations"""
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify([])
        
    if ai_recommender:
        results = ai_recommender.recommend(query)
        return jsonify(results)
    
    return jsonify([])


@app.route('/api/destinations')
def api_destinations():
    """API endpoint to list all destinations"""
    destinations = []
    for dest_id, dest in DESTINATIONS.items():
        destinations.append({
            'id': dest_id,
            'name': dest['name'],
            'eco_score': dest['eco_score'],
            'types': dest['type'],
            'budget_level': dest['budget_level']
        })
    return jsonify({'destinations': destinations})


@app.route('/api/geocode', methods=['POST'])
def api_geocode():
    """Proxy for Nominatim geocoding"""
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify([])
        
    results = GeospatialService.geocode_place(query)
    return jsonify(results)


@app.route('/api/nearby-places', methods=['POST'])
def api_nearby_places():
    """Proxy for Overpass API nearby places"""
    data = request.get_json()
    lat = float(data.get('lat', 0))
    lon = float(data.get('lon', 0))
    radius = int(data.get('radius', 5000))
    place_type = data.get('type', 'all')
    
    places = GeospatialService.get_nearby_places(lat, lon, radius, place_type)
    return jsonify(places)


@app.route('/api/calculate-distance', methods=['POST'])
def api_calculate_distance():
    """Calculate distance and provide feedback"""
    data = request.get_json()
    lat1 = float(data.get('lat1', 0))
    lon1 = float(data.get('lon1', 0))
    lat2 = float(data.get('lat2', 0))
    lon2 = float(data.get('lon2', 0))
    
    from modules.geospatial_service import haversine_distance
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    recommendation = GeospatialService.get_trip_recommendation(distance)
    
    return jsonify({
        'distance_km': round(distance, 2),
        'recommendation': recommendation
    })


@app.route('/map')
def map_page():
    """Interactive Map Selection Page"""
    return render_template('map.html')


@app.route('/plan-custom')
def plan_custom():
    """Generate itinerary from map coordinates"""
    destination_name = request.args.get('destination', 'Selected Location')
    dest_lat = float(request.args.get('lat', 0))
    dest_lon = float(request.args.get('lon', 0))
    origin_lat = request.args.get('origin_lat')
    origin_lon = request.args.get('origin_lon')
    distance = request.args.get('distance')
    
    # Safe conversion of origin coordinates
    try:
        origin_lat = float(origin_lat) if origin_lat else 28.6139 # Default to Delhi
        origin_lon = float(origin_lon) if origin_lon else 77.2090
    except (ValueError, TypeError):
        origin_lat = 28.6139
        origin_lon = 77.2090

    # Calculate distance if not provided
    if not distance:
        from modules.geospatial_service import haversine_distance
        distance = haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon)
    
    distance = float(distance) if distance else 500
    
    # Generate dynamic itinerary using nearby places
    nearby = GeospatialService.get_nearby_places(dest_lat, dest_lon, radius=10000, place_type='all')
    
    # Create simple structure
    itinerary_data = {
        'destination_name': destination_name,
        'dest_lat': dest_lat,
        'dest_lon': dest_lon,
        'origin_lat': origin_lat,
        'origin_lon': origin_lon,
        'duration': 3, # Default
        'eco_score': 8, # Optimistic default
        'overview': f"Sustainable trip to {destination_name}. Explore {len(nearby)} nearby eco-spots.",
        'days': []
    }
    
    # Fill days with nearby places
    current_day = 1
    day_activities = []
    
    # Group places for variety
    temples = [p for p in nearby if p['category'] == 'temple']
    nature = [p for p in nearby if p['category'] == 'park' or p['category'] == 'mountain']
    culture = [p for p in nearby if p['category'] == 'cultural']
    beaches = [p for p in nearby if p['category'] == 'beach']
    
    all_places = temples + nature + culture + beaches
    
    # Simple distribution logic
    for i in range(3):
        activities = []
        if i == 0:
            activities.append({'time': 'Morning', 'activity': 'Arrival & Check-in', 'type': 'relax'})
            if nature: activities.append({'time': 'Afternoon', 'activity': f"Visit {nature[0]['name']}", 'type': 'nature'})
            elif all_places: activities.append({'time': 'Afternoon', 'activity': f"Visit {all_places[0]['name']}", 'type': 'explore'})
        elif i == 1:
            if temples: activities.append({'time': 'Morning', 'activity': f"Visit {temples[0]['name']}", 'type': 'spiritual'})
            if culture: activities.append({'time': 'Afternoon', 'activity': f"Explore {culture[0]['name']}", 'type': 'culture'})
            elif len(all_places) > 1: activities.append({'time': 'Afternoon', 'activity': f"Visit {all_places[1]['name']}", 'type': 'explore'})
        else:
            if beaches: activities.append({'time': 'Morning', 'activity': f"Relax at {beaches[0]['name']}", 'type': 'beach'})
            activities.append({'time': 'Evening', 'activity': 'Departure', 'type': 'travel'})
            
        itinerary_data['days'].append({
            'day': i + 1,
            'activities': activities
        })
        
    # Carbon info (mock for now based on distance)
    carbon_info = {
        'total': int(distance * 0.15), # approx kg co2
        'breakdown': {'transport': int(distance * 0.1), 'accommodation': 20, 'food': 10},
        'comparison': '30% lower than average'
    }
    
    pricing = {
        'avg_cost': '₹5000 - ₹8000',
        'season_status': 'Good time to visit'
    }

    # Hack: Inject into request context or template so it looks like a real destination
    dest_obj = {
        'name': destination_name,
        'eco_score': 8,
        'budget_level': 'Variable',
        'best_season': []
    }
    
    return render_template('itinerary.html',
                         itinerary=itinerary_data,
                         carbon_info=carbon_info,
                         pricing_info=pricing,
                         destination=dest_obj)


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', message="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', message="Server error occurred"), 500


# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
