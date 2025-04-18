/**
 * Pasar Berkelanjutan Jakarta
 * Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initializeNavigation();
    initializeQuantityControls();
    initializeCarousels();
    initializeFilters();
    updateAuthUI();
});

/**
 * Update UI based on authentication status
 */
function updateAuthUI() {
    const isLoggedIn = window.api.isUserLoggedIn();
    const currentUser = window.api.getCurrentUser();
    
    // Update navigation links
    const navLinks = document.querySelector('.main-nav ul');
    if (navLinks) {
        // Get the sign in link
        const signInLink = navLinks.querySelector('a[href="/signin"]');
        
        if (signInLink && isLoggedIn && currentUser) {
            // Replace sign in link with user menu
            const li = signInLink.parentElement;
            li.innerHTML = `
                <a href="#" class="user-menu-toggle">${currentUser.username} ${currentUser.is_seller ? '(Seller)' : ''}</a>
                <ul class="user-dropdown">
                    <li><a href="/profile">My Profile</a></li>
                    ${currentUser.is_seller ? '<li><a href="/my-listings">My Listings</a></li>' : ''}
                    ${currentUser.is_seller ? '<li><a href="/create-listing">Buat Daftar Produk</a></li>' : ''}
                    <li><a href="#" id="logout-link">Logout</a></li>
                </ul>
            `;
            
            // Add event listener for logout
            document.getElementById('logout-link').addEventListener('click', function(e) {
                e.preventDefault();
                logoutUser();
            });
        }
    }
}

/**
 * Handle user logout
 */
async function logoutUser() {
    try {
        await window.api.logoutUser();
        // Redirect to home page after logout
        window.location.href = '/';
    } catch (error) {
        showNotification('Logout failed: ' + error.message, 'error');
    }
}

/**
 * Mobile Navigation Toggle
 */
function initializeNavigation() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            const mainNav = document.querySelector('.main-nav');
            mainNav.classList.toggle('active');
            this.setAttribute('aria-expanded',
                this.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
            );
        });
    }
    
    // Initialize user dropdown menu
    const userMenuToggle = document.querySelector('.user-menu-toggle');
    if (userMenuToggle) {
        userMenuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdown = this.nextElementSibling;
            if (dropdown && dropdown.classList.contains('user-dropdown')) {
                dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
            }
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.user-menu-toggle') && !e.target.closest('.user-dropdown')) {
                const dropdown = document.querySelector('.user-dropdown');
                if (dropdown) {
                    dropdown.style.display = 'none';
                }
            }
        });
    }
}

/**
 * Quantity Controls for Product Pages
 */
function initializeQuantityControls() {
    const quantityInputs = document.querySelectorAll('.quantity-control');
    
    quantityInputs.forEach(control => {
        const input = control.querySelector('input');
        const decreaseBtn = control.querySelector('.decrease');
        const increaseBtn = control.querySelector('.increase');
        
        if (input && decreaseBtn && increaseBtn) {
            decreaseBtn.addEventListener('click', () => {
                const currentValue = parseInt(input.value);
                if (currentValue > parseInt(input.min)) {
                    input.value = currentValue - 1;
                    // Trigger change event for any listeners
                    input.dispatchEvent(new Event('change'));
                }
            });
            
            increaseBtn.addEventListener('click', () => {
                const currentValue = parseInt(input.value);
                if (currentValue < parseInt(input.max)) {
                    input.value = currentValue + 1;
                    // Trigger change event for any listeners
                    input.dispatchEvent(new Event('change'));
                }
            });
        }
    });
}

/**
 * Product and Featured Markets Carousels
 */
function initializeCarousels() {
    const carousels = document.querySelectorAll('.carousel');
    
    carousels.forEach(carousel => {
        const container = carousel.querySelector('.carousel-container');
        const prevBtn = carousel.querySelector('.carousel-prev');
        const nextBtn = carousel.querySelector('.carousel-next');
        
        if (container && prevBtn && nextBtn) {
            let scrollAmount = container.offsetWidth * 0.8;
            
            prevBtn.addEventListener('click', () => {
                container.scrollBy({
                    left: -scrollAmount,
                    behavior: 'smooth'
                });
            });
            
            nextBtn.addEventListener('click', () => {
                container.scrollBy({
                    left: scrollAmount,
                    behavior: 'smooth'
                });
            });
        }
    });
}

/**
 * Filter Toggles for Market Discovery Page
 */
function initializeFilters() {
    const filterToggles = document.querySelectorAll('.filter-toggle');
    
    filterToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const filterContent = this.nextElementSibling;
            
            // Toggle visibility
            if (filterContent) {
                filterContent.classList.toggle('active');
                this.setAttribute('aria-expanded', 
                    this.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
                );
            }
        });
    });
    
    // Mobile filter toggle
    const mobileFilterToggle = document.querySelector('.mobile-filter-toggle');
    
    if (mobileFilterToggle) {
        mobileFilterToggle.addEventListener('click', function() {
            const filterSidebar = document.querySelector('.filter-sidebar');
            
            if (filterSidebar) {
                filterSidebar.classList.toggle('active');
                document.body.classList.toggle('filter-open');
            }
        });
    }
}

/**
 * Add to Cart Functionality
 */
function addToCart(productId, quantity, productData = null) {
    // Get current cart
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const currentUser = window.api.getCurrentUser();
    const userId = currentUser ? currentUser.user_id : 'guest';
    
    // Check if product already exists in cart
    const existingProductIndex = cart.findIndex(item =>
        item.id === productId && item.userId === userId
    );
    
    if (existingProductIndex >= 0) {
        // Update quantity if product already in cart
        cart[existingProductIndex].quantity += quantity;
    } else {
        // Add new product to cart
        const cartItem = {
            id: productId,
            userId: userId,
            quantity: quantity,
            dateAdded: new Date().toISOString()
        };
        
        // If product data was provided, store it for offline access
        if (productData) {
            cartItem.product = productData;
        }
        
        cart.push(cartItem);
    }
    
    // Save updated cart
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Update cart count in UI
    updateCartCount();
    
    // Show confirmation message
    showNotification('Product added to cart!');
}

/**
 * Update Cart Count in Navigation
 */
function updateCartCount() {
    const cartCount = document.querySelector('.cart-count');
    
    if (cartCount) {
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        const currentUser = window.api.getCurrentUser();
        const userId = currentUser ? currentUser.user_id : 'guest';
        
        // Filter cart items by current user
        const userCart = cart.filter(item => item.userId === userId);
        const totalItems = userCart.reduce((total, item) => total + item.quantity, 0);
        
        cartCount.textContent = totalItems;
        cartCount.classList.toggle('hidden', totalItems === 0);
    }
}

/**
 * Show Notification
 */
function showNotification(message, type = 'success') {
    // Sanitize the message to prevent XSS
    const sanitizedMessage = typeof message === 'string' ?
        document.createTextNode(message).textContent : 'Notification';
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = sanitizedMessage;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('active');
    }, 10);
    
    // Remove after delay
    setTimeout(() => {
        notification.classList.remove('active');
        
        // Remove from DOM after animation completes
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Initialize cart count on page load
updateCartCount();