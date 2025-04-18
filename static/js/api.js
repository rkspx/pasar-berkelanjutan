/**
 * Pasar Berkelanjutan Jakarta
 * API Integration Module
 */

// API Base URL - automatically detects the current host
const API_BASE_URL = window.location.origin;

/**
 * Authentication API Functions
 */

// Login user
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
            credentials: 'include' // Include cookies for session management
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Login failed');
        }
        
        // Store user data in localStorage for client-side access
        localStorage.setItem('user', JSON.stringify({
            user_id: data.user_id,
            username: data.username,
            is_seller: data.is_seller
        }));
        
        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

// Register new user
async function registerUser(userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
            credentials: 'include'
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Registration failed');
        }
        
        return data;
    } catch (error) {
        console.error('Registration error:', error);
        throw error;
    }
}

// Logout user
async function logoutUser() {
    try {
        // Clear local storage
        localStorage.removeItem('user');
        
        // Call logout endpoint
        const response = await fetch(`${API_BASE_URL}/logout`, {
            method: 'GET',
            credentials: 'include'
        });
        
        return response.ok;
    } catch (error) {
        console.error('Logout error:', error);
        throw error;
    }
}

// Check if user is logged in
function isUserLoggedIn() {
    const user = localStorage.getItem('user');
    return !!user;
}

// Get current user data
function getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

/**
 * Listings API Functions
 */

// Get all listings with optional filters
async function getListings(filters = {}) {
    try {
        // Build query string from filters
        const queryParams = new URLSearchParams();
        
        if (filters.category_id) {
            queryParams.append('category_id', filters.category_id);
        }
        
        if (filters.search) {
            queryParams.append('q', filters.search);
        }
        
        const url = `${API_BASE_URL}/api/listings?${queryParams.toString()}`;
        
        const response = await fetch(url, {
            method: 'GET',
            credentials: 'include'
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error('Failed to fetch listings');
        }
        
        return data;
    } catch (error) {
        console.error('Error fetching listings:', error);
        throw error;
    }
}

// Get a single listing by ID
async function getListingById(listingId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/listings/${listingId}`, {
            method: 'GET',
            credentials: 'include'
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error('Failed to fetch listing details');
        }
        
        return data;
    } catch (error) {
        console.error(`Error fetching listing ${listingId}:`, error);
        throw error;
    }
}

// Get nearby listings based on coordinates
async function getNearbyListings(lat, lng, radius = 5) {
    try {
        const url = `${API_BASE_URL}/api/nearby_listings?lat=${lat}&lng=${lng}&radius=${radius}`;
        
        const response = await fetch(url, {
            method: 'GET',
            credentials: 'include'
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error('Failed to fetch nearby listings');
        }
        
        return data;
    } catch (error) {
        console.error('Error fetching nearby listings:', error);
        throw error;
    }
}

// Create a new listing (for sellers only)
async function createListing(listingData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/listings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(listingData),
            credentials: 'include'
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to create listing');
        }
        
        return data;
    } catch (error) {
        console.error('Error creating listing:', error);
        throw error;
    }
}

// Update an existing listing
async function updateListing(listingId, listingData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/listings/${listingId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(listingData),
            credentials: 'include'
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to update listing');
        }
        
        return data;
    } catch (error) {
        console.error(`Error updating listing ${listingId}:`, error);
        throw error;
    }
}

// Delete a listing
async function deleteListing(listingId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/listings/${listingId}`, {
            method: 'DELETE',
            credentials: 'include'
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to delete listing');
        }
        
        return data;
    } catch (error) {
        console.error(`Error deleting listing ${listingId}:`, error);
        throw error;
    }
}

// Export all functions
window.api = {
    // Auth functions
    loginUser,
    registerUser,
    logoutUser,
    isUserLoggedIn,
    getCurrentUser,
    
    // Listing functions
    getListings,
    getListingById,
    getNearbyListings,
    createListing,
    updateListing,
    deleteListing
};