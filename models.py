from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import config

# Determine if we're using SQLite
IS_SQLITE = config.CONFIG["db_engine"] == "sqlite"

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    is_seller = Column(Boolean, default=False)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    listings = relationship("Listing", back_populates="seller", cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    __tablename__ = 'categories'
    
    category_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    listings = relationship("Listing", back_populates="category")
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Listing(db.Model):
    __tablename__ = 'listings'
    
    listing_id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    # For SQLite, we'll just use the latitude and longitude columns directly
    # For other databases, we'll use the Geometry column
    if not IS_SQLITE:
        location = Column(Geometry('POINT', srid=4326))
    creation_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    seller = relationship("User", back_populates="listings")
    category = relationship("Category", back_populates="listings")
    images = relationship("ListingImage", back_populates="listing", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Listing {self.title}>'
    
    def to_dict(self):
        return {
            'listing_id': self.listing_id,
            'seller_id': self.seller_id,
            'seller_name': self.seller.username,
            'category_id': self.category_id,
            'category_name': self.category.name,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
            'image_urls': [image.url for image in self.images],
            'latitude': self.latitude,
            'longitude': self.longitude,
            'creation_date': self.creation_date.isoformat()
        }

class ListingImage(db.Model):
    __tablename__ = 'listing_images'
    
    image_id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.listing_id'), nullable=False)
    url = Column(String(255), nullable=False)
    
    # Relationship
    listing = relationship("Listing", back_populates="images")
    
    def __repr__(self):
        return f'<ListingImage {self.url}>'