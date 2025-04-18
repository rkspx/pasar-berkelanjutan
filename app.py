from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import config
from models import db, User, Category, Listing
from werkzeug.security import generate_password_hash, check_password_hash
from geopy.geocoders import Nominatim
import os
from datetime import datetime
from sqlalchemy import func
from geoalchemy2.functions import ST_DWithin, ST_Point, ST_Distance
import json

app = Flask(__name__)
app.secret_key = config.CONFIG["flask_secret_key"]  # Use the static config
app.config['SQLALCHEMY_DATABASE_URI'] = config.get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin_page'

# Initialize geocoder
geolocator = Nominatim(user_agent="pasar_berkelanjutan")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Function to initialize database
def init_db():
    """Initialize database tables and default data"""
    db.create_all()
    
    # Create default categories if they don't exist
    if Category.query.count() == 0:
        categories = [
            "Organic", "Handmade", "Eco-friendly",
            "Local Produce", "Zero Waste"
        ]
        for category_name in categories:
            category = Category(name=category_name)
            db.session.add(category)
        db.session.commit()

# Register the init_db function to run before first request
# For Flask 2.0+, we use before_app_first_request instead of before_first_request
with app.app_context():
    init_db()

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/index')
def index():
    return redirect(url_for('landing_page'))

@app.route('/market-discovery')
def market_discovery_page():
    return render_template('market_discovery_page.html')

@app.route('/product-detail')
def product_detail_page():
    return render_template('product_detail_page.html')

@app.route('/cart-review')
def cart_review_page():
    return render_template('cart_review_page.html')

@app.route('/checkout')
def checkout_page():
    return render_template('checkout_page.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('landing_page'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('signin_page.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_seller = request.form.get('is_seller') == 'on'
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            flash('Username or email already exists', 'error')
        else:
            new_user = User(
                username=username,
                email=email,
                is_seller=is_seller
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)
            flash('Account created successfully!', 'success')
            return redirect(url_for('landing_page'))
    
    return render_template('signup_page.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('landing_page'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password_page():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # In a real application, send a password reset email
            # For now, just show a success message
            flash('Password reset instructions have been sent to your email', 'success')
        else:
            flash('Email not found', 'error')
    
    return render_template('forgot_password_page.html')

@app.route('/empty-cart')
def empty_cart_message():
    return render_template('empty_cart_message.html')

@app.route('/no-results')
def no_results_message():
    return render_template('no_results_message.html')

@app.route('/404')
def page_not_found_route():
    return render_template('404_page.html')

@app.route('/order-confirmation')
def order_confirmation_page():
    return render_template('order_confirmation_page.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_page.html'), 404

# Port configuration routes removed as we're using static configuration

# API Endpoints
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if user already exists
    existing_user = User.query.filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()
    
    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 400
    
    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        is_seller=data.get('is_seller', False)
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully', 'user_id': new_user.user_id}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    
    # Validate required fields
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        session['user_id'] = user.user_id
        return jsonify({
            'message': 'Login successful',
            'user_id': user.user_id,
            'username': user.username,
            'is_seller': user.is_seller
        }), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/listings', methods=['GET'])
def api_get_listings():
    # Get query parameters
    category_id = request.args.get('category_id', type=int)
    search_query = request.args.get('q')
    
    # Start with base query
    query = Listing.query
    
    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search_query:
        query = query.filter(Listing.title.ilike(f'%{search_query}%') |
                            Listing.description.ilike(f'%{search_query}%'))
    
    # Get results
    listings = query.all()
    
    # Convert to dict
    result = [listing.to_dict() for listing in listings]
    
    return jsonify(result)

@app.route('/api/listings', methods=['POST'])
@login_required
def api_create_listing():
    if not current_user.is_seller:
        return jsonify({'error': 'Only sellers can create listings'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'price', 'category_id', 'image_urls', 'address']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Geocode the address
    try:
        location = geolocator.geocode(data['address'])
        if not location:
            return jsonify({'error': 'Could not geocode the provided address'}), 400
        
        latitude = location.latitude
        longitude = location.longitude
    except Exception as e:
        return jsonify({'error': f'Geocoding error: {str(e)}'}), 500
    
    # Create new listing
    new_listing = Listing(
        seller_id=current_user.user_id,
        category_id=data['category_id'],
        title=data['title'],
        description=data['description'],
        price=float(data['price']),
        quantity=data.get('quantity', 1),
        image_urls=data['image_urls'],
        latitude=latitude,
        longitude=longitude,
        location=f'POINT({longitude} {latitude})'
    )
    
    db.session.add(new_listing)
    db.session.commit()
    
    return jsonify({
        'message': 'Listing created successfully',
        'listing_id': new_listing.listing_id
    }), 201

@app.route('/api/listings/<int:listing_id>', methods=['GET'])
def api_get_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return jsonify(listing.to_dict())

@app.route('/api/listings/<int:listing_id>', methods=['PUT'])
@login_required
def api_update_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    
    # Check if user is the seller
    if listing.seller_id != current_user.user_id:
        return jsonify({'error': 'You can only update your own listings'}), 403
    
    data = request.get_json()
    
    # Update fields
    if 'title' in data:
        listing.title = data['title']
    if 'description' in data:
        listing.description = data['description']
    if 'price' in data:
        listing.price = float(data['price'])
    if 'quantity' in data:
        listing.quantity = int(data['quantity'])
    if 'category_id' in data:
        listing.category_id = data['category_id']
    if 'image_urls' in data:
        listing.image_urls = data['image_urls']
    if 'address' in data:
        # Geocode the new address
        try:
            location = geolocator.geocode(data['address'])
            if location:
                listing.latitude = location.latitude
                listing.longitude = location.longitude
                listing.location = f'POINT({location.longitude} {location.latitude})'
        except Exception as e:
            return jsonify({'error': f'Geocoding error: {str(e)}'}), 500
    
    db.session.commit()
    
    return jsonify({
        'message': 'Listing updated successfully',
        'listing': listing.to_dict()
    })

@app.route('/api/listings/<int:listing_id>', methods=['DELETE'])
@login_required
def api_delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    
    # Check if user is the seller
    if listing.seller_id != current_user.user_id:
        return jsonify({'error': 'You can only delete your own listings'}), 403
    
    db.session.delete(listing)
    db.session.commit()
    
    return jsonify({'message': 'Listing deleted successfully'})

@app.route('/api/nearby_listings', methods=['GET'])
def api_nearby_listings():
    # Get query parameters
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', default=5, type=float)  # Default 5km radius
    
    if not lat or not lng:
        return jsonify({'error': 'Latitude and longitude are required'}), 400
    
    # Create a point from the provided coordinates
    user_location = ST_Point(lng, lat, srid=4326)
    
    # Query listings within the radius
    nearby_listings = db.session.query(
        Listing,
        func.ST_Distance(Listing.location, user_location).label('distance')
    ).filter(
        ST_DWithin(Listing.location, user_location, radius * 1000)  # Convert km to meters
    ).order_by('distance').all()
    
    # Convert to dict with distance
    result = []
    for listing, distance in nearby_listings:
        listing_dict = listing.to_dict()
        listing_dict['distance_km'] = round(distance / 1000, 2)  # Convert meters to km
        result.append(listing_dict)
    
    return jsonify(result)

if __name__ == '__main__':
    port = config.get_port()
    
    # Use debug mode in development environment
    debug_mode = config.FLASK_ENV == "development"
    app.run(host='0.0.0.0', port=port, debug=debug_mode)