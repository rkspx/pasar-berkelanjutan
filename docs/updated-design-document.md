# **Pasar Berkelanjutan Jakarta: Geolocation-Based Sustainable Marketplace**

**Version:** 1.0
**Date:** April 18, 2025
**Updated By:** Roo (Technical Consultant)

## 1. Project Overview

**Pasar Berkelanjutan Jakarta** is a community-driven sustainable marketplace platform connecting local sellers and buyers within Jakarta. The platform is designed to be accessible, clean, and centered around a simple user experience. It empowers small businesses and eco-conscious users with easy navigation, meaningful visuals, and an inclusive design system.

This updated design document integrates geolocation-based features to enhance the marketplace experience, allowing buyers to find nearby sellers of sustainable goods and services.

## 2. Goals

* Enable sellers to easily list their sustainable goods or services online
* Allow buyers to search for goods or services and find sellers located near them
* Provide a platform for connecting eco-conscious buyers and sellers
* Promote sustainable and local commerce within Jakarta communities
* Create an intuitive, accessible user experience with geolocation features

## 3. Target Users

* **Sellers:** Individuals or small businesses looking to advertise and sell their sustainable goods or services to a local audience
* **Buyers:** Individuals looking to purchase sustainable goods or services from sellers in their vicinity

## 4. Design Principles

1. **Clarity First**: Prioritize readability, clear labeling, and natural information flow
2. **Visual Hierarchy**: Use consistent type scales and spacing to lead user attention
3. **Minimalism with Warmth**: Clean UI with purposeful use of color and soft visuals
4. **Consistency**: Repeat familiar visual patterns for user confidence
5. **Local Relevance**: Use illustrations, language, and tone that resonate with Jakarta communities

## 5. Color Palette

* **Primary Green**: `#335633` — For primary buttons, highlights
* **Terracotta**: `#D97D54` — Accent color (badges, alerts)
* **Off-White / Cream**: `#F5F5F5` — Backgrounds and sections
* **Text Dark**: `#333333` — Primary text color
* **Text Light**: `#666666` — Secondary text color
* **Border Light**: `#E0E0E0` — Subtle borders
* **White**: `#FFFFFF` — Card backgrounds, contrast elements

## 6. Typography

* **Font Family**: Plus Jakarta Sans or Manrope
* **Heading**: Bold, 32–48px
* **Body Text**: Regular, 16–18px
* **Caption**: Regular, 12–14px

## 7. Core UI Elements

* **Buttons**:
  * Rounded corners (8px)
  * Primary = filled green, white text
  * Secondary = outline or soft fill
* **Inputs**:
  * Border: 1px subtle gray, rounded
  * Label outside input field
* **Cards**:
  * Borderless or light border/shadow
  * Compact, minimal text blocks
* **Icons**:
  * Feather / Lucide style
  * Light outline, consistent sizing
* **Map Elements**:
  * Custom markers with brand colors
  * Consistent info windows
  * Distance indicators

## 8. Core Functionalities

### 8.1. Seller Functionalities:

* **Registration:** Ability to create an account on the platform
* **Login:** Ability to securely log in to their account
* **Profile Creation:** Provide a username, bio, and business details
* **Listing Creation:** Ability to add new listings with the following details:
    * Title
    * Description
    * Price
    * Category selection (from predefined list)
    * Image upload (at least one)
    * Quantity (if applicable for goods)
    * Location specification (via manual address input or map picker)
* **Listing Management:** Ability to view, edit, and delete their own listings

### 8.2. Buyer Functionalities:

* **Registration:** Ability to create an account on the platform
* **Login:** Ability to securely log in to their account
* **Location Sharing:** Grant permission to share their current location via the browser's geolocation API
* **Browse Listings:** View a list of all available listings or filter by category
* **Searching Listings:** Search for listings using keywords
* **Viewing Listing Details:** See all information about a specific listing, including seller information
* **Distance-Based Filtering:** Automatically see the distance of each listing from their current location
* **Map View:** View nearby sellers and their listings on an interactive map

## 9. Technical Architecture

### 9.1. Tech Stack:

* **Backend:** Python Flask
* **Backend Geolocation:** Geopy
* **Database:** PostgreSQL with PostGIS extension
* **Frontend Map:** Leaflet with OpenStreetMap
* **Frontend:** HTML, CSS, JavaScript
* **UI Framework:** Custom CSS with design system variables

### 9.2. Backend (Flask):

* Will handle user authentication (registration and login)
* Will provide API endpoints for:
    * Creating, reading, updating, and deleting listings
    * Fetching listings based on search criteria and proximity to a given location
    * Geocoding seller addresses using Geopy
    * Storing and retrieving location data using PostgreSQL/PostGIS

### 9.3. Database (PostgreSQL with PostGIS):

* **Data Model (Entities):**
    * **Users:**
        ```
        user_id (Primary Key)
        username (Unique)
        email (Unique)
        password_hash
        is_seller (Boolean)
        bio (Text, optional)
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

### 9.4. Frontend (Leaflet/OpenStreetMap):

* Will use Leaflet to display an interactive map with custom styled markers
* Will use OpenStreetMap tiles for the map background
* Will use the browser's geolocation API to get the buyer's current location (with user permission)
* Will send the buyer's location to the backend to fetch nearby listings
* Will display markers on the map for each nearby seller's listing, with custom popups showing listing details
* Will provide a list view of the listings alongside the map

### 9.5. Geolocation (Geopy):

* Will be used on the backend to convert seller-provided addresses into latitude and longitude coordinates for storage in the database
* Will use OpenStreetMap's Nominatim service through Geopy for geocoding

## 10. Key Screens & Layouts

### 10.1. Landing Page

* Hero with search bar by *kelurahan*
* Carousel of featured products or markets
* Section: Produk Terbaru (Latest Products)
* Call-to-action for sellers and buyers

### 10.2. Market Discovery Page

* Split view: Left filter sidebar, right interactive Jakarta map
* Filter by category, delivery method, distance, and payment options
* List of results with cards showing distance from user
* Map markers for all visible listings

### 10.3. Product Detail Page

* Image gallery, description, seller badge
* Price, stock, quantity selector
* Delivery & payment options
* Seller widget with location information
* Map showing seller location
* Related products

### 10.4. Cart & Checkout Flow

* Cart Review: List items, quantity control, promo code, order summary
* Checkout:
  * Alamat & Pickup method (Pasar, Kurir Lokal, COD)
  * Payment selection (GoPay, OVO, Bank Transfer)
  * Order recap

### 10.5. Authentication Screens

* Sign In: Email + Password, followed by OTP
* Sign Up: Name, Email, Phone, Password + Terms
* Forgot Password: Email/Phone + OTP reset

### 10.6. Seller Dashboard

* Listing management (add, edit, delete)
* Order management
* Profile settings with location management

### 10.7. System Feedback Screens

* Empty Cart: "Keranjang Anda Kosong"
* No Results: "Tidak ada pasar ditemukan"
* 404 Page: Local illustration + search + return links
* Order Confirmation:
  * Summary, order number, pickup slot or delivery estimate
  * CTA to view order status or return to homepage

## 11. API Endpoints

* `POST /api/register`: Register a new user
* `POST /api/login`: Log in an existing user
* `GET /api/listings`: Get all listings (with optional filters)
* `POST /api/listings`: Create a new listing (requires seller authentication)
* `GET /api/listings/<listing_id>`: Get details for a specific listing
* `PUT /api/listings/<listing_id>`: Update a listing (requires seller authentication)
* `DELETE /api/listings/<listing_id>`: Delete a listing (requires seller authentication)
* `GET /api/nearby_listings`: Get listings within a certain radius of the provided latitude and longitude

## 12. Interaction Guidelines

* **Animations**: Use Framer Motion for smooth transitions (e.g. cart open, filter toggle)
* **Responsive Behavior**:
  * Cards collapse into list view
  * Filter becomes modal
  * Fixed bottom CTAs on mobile
  * Map resizes appropriately on different devices
* **Accessibility**:
  * All buttons have labels
  * Color contrast AA+ compliant
  * Focus rings and screen-reader support
  * Alternative text for map interactions

## 13. Future Considerations (Post-MVP)

* Direct messaging between buyers and sellers
* Order management and payment processing
* User reviews and ratings
* More advanced search filters
* Seller community features
* Admin dashboard for managing users and listings
* Enhanced analytics for sellers
* Sustainability metrics and badges

## 14. Implementation Plan

1. Set up PostgreSQL with PostGIS extension
2. Implement user authentication system
3. Create database models and migrations
4. Develop API endpoints for listings and geolocation
5. Enhance frontend with Leaflet map integration
6. Implement geolocation features for buyers
7. Create seller dashboard for listing management
8. Integrate address geocoding with Geopy
9. Test and optimize geolocation performance
10. Deploy and monitor

---

End of document.