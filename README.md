# Pasar Berkelanjutan Jakarta

A geolocation-based sustainable marketplace platform connecting local sellers and buyers within Jakarta.

## Project Overview

Pasar Berkelanjutan Jakarta is a web application designed to promote sustainable shopping practices by connecting eco-conscious consumers with local sellers offering sustainable products. The platform emphasizes accessibility, clean design, and a simple user experience with powerful geolocation features to help buyers find nearby sellers.

## Features

- **User Authentication**: Secure sign-in, sign-up, and password recovery
- **Geolocation-Based Discovery**: Find nearby sustainable markets using your current location
- **Interactive Map**: View sellers on an interactive map with custom markers and distance indicators
- **Distance-Based Filtering**: Filter listings based on proximity to your location
- **Product Browsing**: Browse and search for sustainable products with advanced filtering
- **Seller Dashboard**: Sellers can manage their listings with location information
- **Shopping Cart**: Add products to cart and manage quantities
- **Checkout Process**: Streamlined checkout with multiple delivery and payment options
- **Responsive Design**: Optimized for both desktop and mobile devices

## Design Principles

1. **Clarity First**: Prioritize readability, clear labeling, and natural information flow
2. **Visual Hierarchy**: Use consistent type scales and spacing to lead user attention
3. **Minimalism with Warmth**: Clean UI with purposeful use of color and soft visuals
4. **Consistency**: Repeat familiar visual patterns for user confidence
5. **Local Relevance**: Use illustrations, language, and tone that resonate with Jakarta communities

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python with Flask framework
- **Database**: PostgreSQL with PostGIS extension for geospatial data
- **ORM**: SQLAlchemy with GeoAlchemy2
- **Geolocation**: Geopy for geocoding addresses
- **Map Integration**: Leaflet.js with OpenStreetMap for interactive maps
- **Geocoding**: Nominatim service for address lookup
- **Icons**: Lucide icons
- **Animations**: Framer Motion for smooth transitions

## Color Palette

- **Primary Green**: `#335633` — For primary buttons, highlights
- **Terracotta**: `#D97D54` — Accent color (badges, alerts)
- **Off-White / Cream**: `#F5F5F5` — Backgrounds and sections

## Project Structure

```
pasar-berkelanjutan/
├── app.py                  # Main Flask application
├── config.py               # Configuration management
├── models.py               # Database models
├── app_config.json         # Persisted configuration (generated)
├── .env                    # Environment variables (create from .env.example)
├── .env.example            # Environment variables template
├── static/                 # Static assets
│   ├── css/                # CSS stylesheets
│   ├── js/                 # JavaScript files
│   └── images/             # Image assets
│       ├── marker-green.png  # Listing marker for maps
│       └── marker-user.png   # User location marker for maps
├── templates/              # HTML templates
│   ├── base.html           # Base template with common elements
│   ├── landing_page.html   # Homepage
│   ├── market_discovery_page.html  # Market discovery page
│   ├── product_detail_page.html    # Product details
│   ├── port_config_page.html       # Port configuration page
│   └── ...                 # Other page templates
└── docs/                   # Documentation
    ├── design-document.md          # Original design specifications
    ├── updated-design-document.md  # Updated design with geolocation features
    ├── design-document-18042025.md # Technical specifications
    ├── requirements.md             # Project requirements
    └── wireframes/                 # UI wireframes
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/pasar-berkelanjutan.git
   cd pasar-berkelanjutan
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL with PostGIS:
   - Install PostgreSQL and PostGIS extension
   - Create a database for the application:
     ```
     createdb pasar_berkelanjutan
     ```
   - Enable PostGIS extension:
     ```
     psql -d pasar_berkelanjutan -c "CREATE EXTENSION postgis;"
     ```

5. Configure environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your database credentials and other settings.

6. Run the application:
   ```
   python app.py
   ```

7. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Server Configuration

The application includes configuration systems for:

### Port Configuration

1. Specify a custom port number for the server
2. Validate that the port is within the valid range (0-65535)
3. Check if the port is already in use by another service
4. Reset to default port settings if needed

### Database Configuration

The application uses PostgreSQL with PostGIS extension for geospatial data storage and queries:

1. Database settings are configured through environment variables
2. The application supports connection to a local or remote PostgreSQL database
3. PostGIS extension is required for geolocation features

### Accessing Port Configuration

You can access the port configuration page by:

1. Clicking on the "Server Configuration" link in the footer
2. Directly navigating to `http://localhost:5000/port-config`

### Changing the Port

1. Enter your desired port number in the input field
2. Click "Save Configuration"
3. Restart the application for changes to take effect:
  ```
  python app.py
  ```

### Configuration Persistence

Port settings are stored in `app_config.json` in the project root directory and persist between application restarts.

### Default Port

The default port is 5000. You can reset to this default at any time by clicking the "Reset to Default" button on the port configuration page.

## Key Pages

- **Landing Page**: Introduction to the platform with featured markets and products
- **Market Discovery**: Find nearby markets using geolocation, filters, and an interactive map
- **Product Detail**: View product information, images, seller location, and purchasing options
- **Cart & Checkout**: Review cart items and complete the purchase process
- **Authentication**: Sign in, sign up, and password recovery
- **Seller Dashboard**: Manage listings with location information

## API Endpoints

The application provides the following API endpoints:

- `POST /api/register`: Register a new user
- `POST /api/login`: Log in an existing user
- `GET /api/listings`: Get all listings (with optional filters)
- `POST /api/listings`: Create a new listing (requires seller authentication)
- `GET /api/listings/<listing_id>`: Get details for a specific listing
- `PUT /api/listings/<listing_id>`: Update a listing (requires seller authentication)
- `DELETE /api/listings/<listing_id>`: Delete a listing (requires seller authentication)
- `GET /api/nearby_listings`: Get listings within a certain radius of the provided latitude and longitude

## Geolocation Features

- **User Location Detection**: Automatically detect the user's location using the browser's geolocation API
- **Distance Calculation**: Calculate and display the distance between the user and each listing
- **Proximity Search**: Find listings within a specified radius of the user's location
- **Interactive Map**: View listings on an interactive map with custom markers
- **Address Geocoding**: Convert addresses to latitude and longitude coordinates for storage and distance calculations

## Future Enhancements

- Direct messaging between buyers and sellers
- Order management and payment processing
- User reviews and ratings
- More advanced search filters
- Seller community features
- Admin dashboard for managing users and listings
- Enhanced analytics for sellers
- Sustainability metrics and badges

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.