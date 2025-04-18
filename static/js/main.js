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
});

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
function addToCart(productId, quantity) {
    // This would typically make an AJAX request to the server
    // For now, we'll just simulate with localStorage
    
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Check if product already exists in cart
    const existingProductIndex = cart.findIndex(item => item.id === productId);
    
    if (existingProductIndex >= 0) {
        // Update quantity if product already in cart
        cart[existingProductIndex].quantity += quantity;
    } else {
        // Add new product to cart
        cart.push({
            id: productId,
            quantity: quantity
        });
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
        const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
        
        cartCount.textContent = totalItems;
        cartCount.classList.toggle('hidden', totalItems === 0);
    }
}

/**
 * Show Notification
 */
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
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