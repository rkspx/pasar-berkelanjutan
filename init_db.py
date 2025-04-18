"""
Database initialization script for Pasar Berkelanjutan Jakarta.
This script creates the necessary database tables and populates them with initial data.
"""

import os
from dotenv import load_dotenv
from flask import Flask
from models import db, User, Category, Listing
from werkzeug.security import generate_password_hash
import config
from datetime import datetime

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def init_db():
    """Initialize the database with tables and sample data."""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if we already have data
        if Category.query.count() > 0:
            print("Database already contains data. Skipping initialization.")
            return
        
        print("Initializing database with sample data...")
        
        # Create categories
        categories = [
            "Organic",
            "Handmade",
            "Eco-friendly",
            "Local Produce",
            "Zero Waste"
        ]
        
        category_objects = {}
        for category_name in categories:
            category = Category(name=category_name)
            db.session.add(category)
            category_objects[category_name] = category
        
        db.session.commit()
        print(f"Created {len(categories)} categories.")
        
        # Create sample users
        users = [
            {
                "username": "admin",
                "email": "admin@pasarberkelanjutan.id",
                "password": "admin123",
                "is_seller": True,
                "bio": "Administrator account"
            },
            {
                "username": "seller1",
                "email": "seller1@example.com",
                "password": "password123",
                "is_seller": True,
                "bio": "Organic vegetable seller from South Jakarta"
            },
            {
                "username": "buyer1",
                "email": "buyer1@example.com",
                "password": "password123",
                "is_seller": False,
                "bio": "Eco-conscious shopper"
            }
        ]
        
        user_objects = {}
        for user_data in users:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                is_seller=user_data["is_seller"],
                bio=user_data["bio"]
            )
            user.password_hash = generate_password_hash(user_data["password"])
            db.session.add(user)
            user_objects[user_data["username"]] = user
        
        db.session.commit()
        print(f"Created {len(users)} users.")
        
        # Create sample listings
        listings = [
            {
                "seller": "seller1",
                "category": "Organic",
                "title": "Fresh Organic Vegetables",
                "description": "A bundle of fresh, locally grown organic vegetables including carrots, spinach, and tomatoes.",
                "price": 25000,
                "quantity": 10,
                "image_urls": ["https://via.placeholder.com/300x200?text=Organic+Vegetables"],
                "latitude": -6.2641,
                "longitude": 106.8432
            },
            {
                "seller": "seller1",
                "category": "Handmade",
                "title": "Handmade Bamboo Utensils",
                "description": "Set of eco-friendly bamboo utensils, handcrafted by local artisans.",
                "price": 45000,
                "quantity": 5,
                "image_urls": ["https://via.placeholder.com/300x200?text=Bamboo+Utensils"],
                "latitude": -6.2641,
                "longitude": 106.8432
            },
            {
                "seller": "seller1",
                "category": "Zero Waste",
                "title": "Reusable Produce Bags",
                "description": "Set of 5 reusable mesh bags for fruits and vegetables. Reduce plastic waste while shopping.",
                "price": 35000,
                "quantity": 20,
                "image_urls": ["https://via.placeholder.com/300x200?text=Reusable+Bags"],
                "latitude": -6.2641,
                "longitude": 106.8432
            }
        ]
        
        for listing_data in listings:
            listing = Listing(
                seller_id=user_objects[listing_data["seller"]].user_id,
                category_id=category_objects[listing_data["category"]].category_id,
                title=listing_data["title"],
                description=listing_data["description"],
                price=listing_data["price"],
                quantity=listing_data["quantity"],
                image_urls=listing_data["image_urls"],
                latitude=listing_data["latitude"],
                longitude=listing_data["longitude"],
                location=f"POINT({listing_data['longitude']} {listing_data['latitude']})",
                creation_date=datetime.utcnow()
            )
            db.session.add(listing)
        
        db.session.commit()
        print(f"Created {len(listings)} listings.")
        
        print("Database initialization complete!")

if __name__ == "__main__":
    init_db()