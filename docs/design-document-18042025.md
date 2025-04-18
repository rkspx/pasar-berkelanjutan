# Design Document: Basic Geolocation-Based Online Marketplace

**Version:** 0.1
**Date:** April 18, 2025
**Author:** Gemini (AI Assistant)

## 1. Introduction

This document outlines the design for a basic online marketplace platform where buyers can find nearby sellers of goods and services. This is an initial Minimum Viable Product (MVP) focusing on core functionalities for sellers to list their offerings and for buyers to discover them based on their location.

## 2. Goals

* Enable sellers to easily list their goods or services online.
* Allow buyers to search for goods or services and find sellers located near them.
* Provide a basic platform for connecting buyers and sellers.
* Serve as a learning experience in building a web application with geolocation features.

## 3. Target Users

* **Sellers:** Individuals or small businesses looking to advertise and sell their goods or services to a local audience.
* **Buyers:** Individuals looking to purchase goods or services from sellers in their vicinity.

## 4. Core Functionalities

### 4.1. Seller Functionalities:

* **Registration:** Ability to create an account on the platform.
* **Login:** Ability to securely log in to their account.
* **Profile Creation (Basic):** Provide a username and potentially a short bio or business name.
* **Listing Creation:** Ability to add new listings with the following details:
    * Title
    * Description
    * Price
    * Category selection (predefined list)
    * At least one image upload
    * Quantity (if applicable for goods)
    * Location specification (via manual address input or map picker).
* **Listing Management:** Ability to view, edit, and delete their own listings.

### 4.2. Buyer Functionalities:

* **Registration:** Ability to create an account on the platform.
* **Login:** Ability to securely log in to their account.
* **Location Sharing:** Grant permission to share their current location via the browser's geolocation API.
* **Browse Listings:** View a list of all available listings or filter by category.
* **Searching Listings:** Search for listings using keywords.
* **Viewing Listing Details:** See all information about a specific listing, including seller information (username).
* **Distance-Based Filtering:** Automatically see the distance of each listing from their current location (if location is shared).
* **Map View:** View nearby sellers and their listings on an interactive map.

## 5. Technical Design

### 5.1. Tech Stack:

* **Backend:** Python Flask
* **Backend Geolocation:** Geopy
* **Database:** PostgreSQL with PostGIS extension
* **Frontend Map:** Leaflet with OpenStreetMap
* **Frontend:** HTML, CSS, JavaScript

### 5.2. Backend (Flask):

* Will handle user authentication (registration and login).
* Will provide API endpoints for:
    * Creating, reading, updating, and deleting listings.
    * Fetching listings based on search criteria and proximity to a given location.
    * Geocoding seller addresses using Geopy.
    * Storing and retrieving location data using PostgreSQL/PostGIS.

### 5.3. Database (PostgreSQL with PostGIS):

* **Data Model (Entities):**
    * **Users:**
        ```
        user_id (Primary Key)
        username (Unique)
        email (Unique)
        password_hash
        is_seller (Boolean)
        ```
    * **Listings:**
        ```
        listing_id (Primary Key)
        seller_id (Foreign Key referencing Users)
        category_id (Foreign Key referencing Categories)
        title
        description
        price
        quantity
        image_urls (Array of strings)
        latitude (Double Precision)
        longitude (Double Precision)
        creation_date
        ```
    * **Categories:**
        ```
        category_id (Primary Key)
        name (Unique)
        ```
* **Location Data:** Seller locations (latitude and longitude) will be stored directly in the `Listings` table. PostGIS extension will be used for efficient geospatial queries.

### 5.4. Frontend (Leaflet/OpenStreetMap):

* Will use Leaflet to display an interactive map.
* Will use OpenStreetMap tiles for the map background.
* Will use the browser's geolocation API to get the buyer's current location (with user permission).
* Will send the buyer's location to the backend to fetch nearby listings.
* Will display markers on the map for each nearby seller's listing, potentially with brief information on hover or click.
* Will provide a list view of the listings alongside the map.

### 5.5. Geolocation (Geopy):

* Will be used on the backend to convert seller-provided addresses into latitude and longitude coordinates for storage in the database. We will likely use OpenStreetMap's Nominatim service through Geopy.

## 6. Data Model (Entities)

* **User:** Represents both buyers and sellers. The `is_seller` flag can differentiate their roles.
* **Listing:** Represents a good or service offered for sale. Includes details like title, description, price, images, and the seller's location (latitude and longitude).
* **Category:** Organizes listings into different types of goods or services.

## 7. API Endpoints (Examples)

* `POST /api/register`: Register a new user.
* `POST /api/login`: Log in an existing user.
* `GET /api/listings`: Get all listings (potentially with filters like category).
* `POST /api/listings`: Create a new listing (requires seller authentication).
* `GET /api/listings/<listing_id>`: Get details for a specific listing.
* `PUT /api/listings/<listing_id>`: Update a listing (requires seller authentication).
* `DELETE /api/listings/<listing_id>`: Delete a listing (requires seller authentication).
* `GET /api/nearby_listings`: Get listings within a certain radius of the provided latitude and longitude (requires buyer's location).

## 8. Frontend Design Considerations

* **Clear Location Permission Request:** Prompt users for location access with a clear explanation of why it's needed.
* **Map Display:** Prominently display the map with markers for nearby listings.
* **List View:** Provide an alternative list view of the listings, showing distance from the buyer.
* **Filtering and Sorting:** Allow buyers to filter listings by category and potentially sort by distance or other criteria.
* **User-Friendly Listing Creation Form:** Make it easy for sellers to add all necessary information about their goods or services.

## 9. Future Considerations (Out of Scope for MVP)

* Direct messaging between buyers and sellers.
* Order management and payment processing.
* User reviews and ratings.
* More advanced search filters.
* Seller community features.
* Admin dashboard for managing users and listings.