/*
 * =========================================================================
 * SilverTimes.ART - JavaScript
 * =========================================================================
 * 
 * Photography portfolio website with backend integration support
 * Features: Form handling, dynamic content loading, image modals, navigation
 * 
 * Author: SilverTimes.ART
 * Version: 2.0 Enhanced
 * Last Updated: August 2025
 * 
 * Dependencies:
 * - Bootstrap 5.3+ (for styling and components)
 * - baguetteBox.js (for image lightbox functionality)
 * 
 * Browser Support: Modern browsers (ES6+)
 * =========================================================================
 */

// =========================================================================
// MODAL FUNCTIONALITY
// =========================================================================

/**
 * Opens image modal for enlarged view
 * @param {string} imageSrc - Source URL of the image to display
 */
function openModal(imageSrc) {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    
    if (modal && modalImage) {
        modal.style.display = 'block';
        modalImage.src = imageSrc;
        
        // Prevent body scrolling when modal is open
        document.body.classList.add('modal-open');
    }
}

/**
 * Closes the image modal
 */
function closeModal() {
    const modal = document.getElementById('imageModal');
    
    if (modal) {
        modal.style.display = 'none';
        
        // Re-enable body scrolling
        document.body.classList.remove('modal-open');
    }
}

// =========================================================================
// MAIN INITIALIZATION & EVENT LISTENERS
// =========================================================================

/**
 * Initialize all form handlers and event listeners when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('SilverTimes.ART - Initializing enhanced JavaScript...');
    
    // Initialize form handlers
    initializeFormHandlers();
    
    // Initialize navigation
    setActiveNavigation();
    
    // Initialize dynamic content loading
    initializeDynamicContent();
    
    console.log('SilverTimes.ART - JavaScript initialization complete');
});

/**
 * Initialize all form event listeners
 */
function initializeFormHandlers() {
    // Registration form handler
    const registrationForm = document.getElementById('registrationForm');
    if (registrationForm) {
        registrationForm.addEventListener('submit', handleRegistrationSubmit);
        console.log('Registration form handler initialized');
    }

    // Contact form handler
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactSubmit);
        console.log('Contact form handler initialized');
    }

    // Order form handler
    const orderForm = document.getElementById('orderForm');
    if (orderForm) {
        orderForm.addEventListener('submit', handleOrderSubmit);
        console.log('Order form handler initialized');
    }

    // Password confirmation validation
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm-password');
    if (password && confirmPassword) {
        confirmPassword.addEventListener('input', validatePasswordConfirmation);
        password.addEventListener('input', validatePasswordConfirmation);
        console.log('Password validation initialized');
    }
}

// =========================================================================
// FORM SUBMISSION HANDLERS
// =========================================================================

/**
 * Handles registration form submission with validation and AJAX
 * @param {Event} event - The form submit event
 */
async function handleRegistrationSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Show loading state
    setButtonLoading(submitButton, true);
    
    // Client-side validation
    if (formData.get('password') !== formData.get('confirm_password')) {
        showMessage('Passwords do not match', 'error');
        setButtonLoading(submitButton, false);
        return;
    }

    try {
        console.log('Submitting registration form...');
        
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const result = await response.json();
        
        if (response.ok) {
            showMessage('Registration successful! Please check your email.', 'success');
            form.reset();
            console.log('Registration successful');
        } else {
            showMessage(result.message || 'Registration failed', 'error');
            console.error('Registration failed:', result);
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
        console.error('Registration network error:', error);
    } finally {
        setButtonLoading(submitButton, false);
    }
}

/**
 * Handles contact form submission with AJAX
 * @param {Event} event - The form submit event
 */
async function handleContactSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Show loading state
    setButtonLoading(submitButton, true);

    try {
        console.log('Submitting contact form...');
        
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const result = await response.json();
        
        if (response.ok) {
            showMessage('Message sent successfully!', 'success');
            form.reset();
            console.log('Contact message sent successfully');
        } else {
            showMessage(result.message || 'Failed to send message', 'error');
            console.error('Contact form submission failed:', result);
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
        console.error('Contact form network error:', error);
    } finally {
        setButtonLoading(submitButton, false);
    }
}

/**
 * Handles order form submission with AJAX
 * @param {Event} event - The form submit event
 */
async function handleOrderSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Show loading state
    setButtonLoading(submitButton, true);

    try {
        console.log('Submitting order form...');
        
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const result = await response.json();
        
        if (response.ok) {
            showMessage('Order submitted successfully! We will contact you soon.', 'success');
            form.reset();
            console.log('Order submitted successfully');
        } else {
            showMessage(result.message || 'Failed to submit order', 'error');
            console.error('Order submission failed:', result);
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
        console.error('Order form network error:', error);
    } finally {
        setButtonLoading(submitButton, false);
    }
}

// =========================================================================
// FORM VALIDATION & UI HELPERS
// =========================================================================

/**
 * Validates password confirmation in real-time
 * Shows visual feedback to user about password match status
 */
function validatePasswordConfirmation() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm-password');
    
    if (!password || !confirmPassword) return;
    
    const passwordValue = password.value;
    const confirmPasswordValue = confirmPassword.value;
    
    // Only validate if confirm password has content
    if (confirmPasswordValue) {
        if (passwordValue !== confirmPasswordValue) {
            confirmPassword.setCustomValidity('Passwords do not match');
            confirmPassword.classList.add('is-invalid');
            confirmPassword.classList.remove('is-valid');
        } else {
            confirmPassword.setCustomValidity('');
            confirmPassword.classList.remove('is-invalid');
            confirmPassword.classList.add('is-valid');
        }
    } else {
        // Clear validation state when field is empty
        confirmPassword.setCustomValidity('');
        confirmPassword.classList.remove('is-invalid', 'is-valid');
    }
}

/**
 * Sets loading state for submit buttons
 * @param {HTMLElement} button - The button element
 * @param {boolean} isLoading - Whether to show loading state
 */
function setButtonLoading(button, isLoading) {
    if (!button) return;
    
    if (isLoading) {
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Processing...';
    } else {
        button.disabled = false;
        
        // Restore original button text based on button context
        if (button.closest('#registrationForm')) {
            button.innerHTML = '<i class="fas fa-user-plus me-2"></i> Register';
        } else if (button.closest('#contactForm')) {
            button.innerHTML = '<i class="fas fa-paper-plane"></i> Send';
        } else if (button.closest('#orderForm')) {
            button.innerHTML = '<i class="fas fa-paper-plane"></i> Order';
        }
    }
}

/**
 * Displays user feedback messages with Bootstrap styling
 * @param {string} message - The message to display
 * @param {string} type - Message type: 'success', 'error', 'warning', 'info'
 */
function showMessage(message, type) {
    console.log(`Showing ${type} message:`, message);
    
    // Remove any existing messages
    const existingMessages = document.querySelectorAll('.alert-message');
    existingMessages.forEach(msg => msg.remove());

    // Create new message element
    const alertDiv = document.createElement('div');
    const alertType = type === 'error' ? 'danger' : type;
    alertDiv.className = `alert alert-${alertType} alert-dismissible fade show alert-message`;
    alertDiv.style.cssText = 'position: relative; z-index: 1050; margin-bottom: 1rem;';
    
    alertDiv.innerHTML = `
        <i class="fas fa-${getMessageIcon(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    // Find the best location to insert the message
    const targetContainer = document.querySelector('main') || 
                           document.querySelector('.container') || 
                           document.body;
    
    if (targetContainer) {
        targetContainer.insertBefore(alertDiv, targetContainer.firstChild);
        
        // Scroll to message if it's not visible
        alertDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.classList.remove('show');
                setTimeout(() => alertDiv.remove(), 150);
            }
        }, 5000);
    }
}

/**
 * Returns appropriate icon for message type
 * @param {string} type - Message type
 * @returns {string} Font Awesome icon class
 */
function getMessageIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-triangle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// =========================================================================
// DYNAMIC CONTENT LOADING
// =========================================================================

/**
 * ContentLoader object - Handles dynamic loading of content from backend API
 * Provides methods for loading galleries, blog posts, and printshop items
 */
const ContentLoader = {
    /**
     * Loads gallery images from API and displays them
     * @param {string|number} galleryId - The gallery ID to load
     * @param {string} containerId - Target container element ID
     */
    loadGalleryImages: async function(galleryId, containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with ID '${containerId}' not found`);
            return;
        }

        try {
            console.log(`Loading gallery images for gallery ID: ${galleryId}`);
            
            // Show loading state
            container.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x"></i><p>Loading gallery...</p></div>';
            
            const response = await fetch(`/api/galleries/${galleryId}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const gallery = await response.json();
            
            if (container && gallery.images && gallery.images.length > 0) {
                container.innerHTML = gallery.images.map(image => `
                    <div class="col-md-6 text-center">
                        <a class="lightbox" href="${image.full_path}" title="${image.title}">
                            <img src="${image.thumbnail_path}" 
                                 alt="${image.title}" 
                                 class="img-fluid rounded"
                                 loading="lazy">
                        </a>
                        <h3 class="gallery-page mt-2">${image.title}</h3>
                        ${image.description ? `<p class="text-muted">${image.description}</p>` : ''}
                    </div>
                `).join('');
                
                // Reinitialize lightbox if available
                if (typeof baguetteBox !== 'undefined') {
                    baguetteBox.run('.tz-gallery');
                    console.log('Gallery lightbox reinitialized');
                }
                
                console.log(`Successfully loaded ${gallery.images.length} images`);
            } else {
                container.innerHTML = '<div class="text-center text-muted"><p>No images found in this gallery.</p></div>';
            }
        } catch (error) {
            console.error('Failed to load gallery images:', error);
            container.innerHTML = '<div class="text-center text-danger"><i class="fas fa-exclamation-triangle"></i><p>Failed to load gallery. Please try again later.</p></div>';
        }
    },

    /**
     * Loads blog posts from API and displays them
     * @param {string} containerId - Target container element ID
     * @param {number|null} limit - Optional limit for number of posts
     */
    loadBlogPosts: async function(containerId, limit = null) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with ID '${containerId}' not found`);
            return;
        }

        try {
            console.log(`Loading blog posts${limit ? ` (limit: ${limit})` : ''}`);
            
            // Show loading state
            container.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x"></i><p>Loading blog posts...</p></div>';
            
            const url = limit ? `/api/blog?limit=${limit}` : '/api/blog';
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const posts = await response.json();
            
            if (container && posts && posts.length > 0) {
                container.innerHTML = posts.map(post => `
                    <div class="col-md-4">
                        <div class="card border-0 shadow-none">
                            <img src="${post.featured_image}" 
                                 class="card-img-top" 
                                 alt="${post.title}"
                                 loading="lazy">
                            <div class="card-body text-start px-0">
                                <h5 class="card-title">${post.title}</h5>
                                <p class="card-text text-muted small">${this.formatDate(post.created_at)}</p>
                                <p class="card-text">${post.excerpt}</p>
                                <a href="blog-single.html?slug=${post.slug}" class="btn btn-outline-dark">Read More</a>
                            </div>
                        </div>
                    </div>
                `).join('');
                
                console.log(`Successfully loaded ${posts.length} blog posts`);
            } else {
                container.innerHTML = '<div class="text-center text-muted"><p>No blog posts found.</p></div>';
            }
        } catch (error) {
            console.error('Failed to load blog posts:', error);
            container.innerHTML = '<div class="text-center text-danger"><i class="fas fa-exclamation-triangle"></i><p>Failed to load blog posts. Please try again later.</p></div>';
        }
    },

    /**
     * Loads printshop items from API and displays them
     * @param {string} containerId - Target container element ID
     */
    loadPrintshopItems: async function(containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with ID '${containerId}' not found`);
            return;
        }

        try {
            console.log('Loading printshop items');
            
            // Show loading state
            container.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x"></i><p>Loading items...</p></div>';
            
            const response = await fetch('/api/printshop');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const items = await response.json();
            
            if (container && items && items.length > 0) {
                container.innerHTML = items.map(item => `
                    <div class="col-md-4">
                        <div class="card border-0 shadow-none">
                            <img src="${item.image_path}" 
                                 class="card-img-top" 
                                 alt="${item.title}"
                                 loading="lazy">
                            <div class="card-body text-start px-0">
                                <h5 class="card-title">${item.title}</h5>
                                <p class="card-text">${item.description}</p>
                                <p class="card-text">
                                    <strong class="text-success">$${item.price}</strong>
                                    ${item.is_available ? 
                                        '<span class="badge bg-success ms-2">Available</span>' : 
                                        '<span class="badge bg-warning ms-2">Out of Stock</span>'}
                                </p>
                                <a href="printshop-single.html?id=${item.id}" class="btn btn-outline-dark">View Details</a>
                            </div>
                        </div>
                    </div>
                `).join('');
                
                console.log(`Successfully loaded ${items.length} printshop items`);
            } else {
                container.innerHTML = '<div class="text-center text-muted"><p>No items available at the moment.</p></div>';
            }
        } catch (error) {
            console.error('Failed to load printshop items:', error);
            container.innerHTML = '<div class="text-center text-danger"><i class="fas fa-exclamation-triangle"></i><p>Failed to load items. Please try again later.</p></div>';
        }
    },

    /**
     * Formats date for display
     * @param {string} dateString - ISO date string
     * @returns {string} Formatted date
     */
    formatDate: function(dateString) {
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
        } catch (error) {
            return dateString;
        }
    }
};

// =========================================================================
// NAVIGATION & UI ENHANCEMENT
// =========================================================================

/**
 * Sets active navigation state based on current page
 * Highlights the current page in the navigation menu
 */
function setActiveNavigation() {
  try {
    const nav = document.querySelector('.navbar');
    if (!nav) return;

    // If the template already marked something active, respect it and exit.
    if (nav.querySelector('.nav-link.active,[aria-current="page"]')) {
      return;
    }

    const norm = (path) => {
      try {
        // keep "/" as "/", strip trailing slash for others
        return path === '/' ? '/' : path.replace(/\/+$/, '');
      } catch {
        return path || '/';
      }
    };

    const here = norm(window.location.pathname || '/');

    nav.querySelectorAll('.nav-link[href]').forEach(link => {
      const url = new URL(link.getAttribute('href'), window.location.origin);
      const linkPath = norm(url.pathname);

      // Clear only what JS might have set previously
      if (link.dataset.jsActive === '1') {
        link.classList.remove('active');
        link.removeAttribute('aria-current');
        delete link.dataset.jsActive;
      }

      // Home matches only home
      if (linkPath === '/') {
        if (here === '/') {
          link.classList.add('active');
          link.setAttribute('aria-current', 'page');
          link.dataset.jsActive = '1';
        }
        return;
      }

      // Exact match or section prefix (/galleries and /galleries/child)
      if (here === linkPath || here.startsWith(linkPath + '/')) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
        link.dataset.jsActive = '1';
      }
    });
  } catch (error) {
    console.error('Error setting active navigation:', error);
  }
}

/**
 * Initialize dynamic content loading based on data attributes
 * Automatically loads content if containers have the appropriate data attributes
 */
function initializeDynamicContent() {
    try {
        // Auto-load gallery images if container has data-gallery-id
        const galleryContainer = document.querySelector('[data-gallery-id]');
        if (galleryContainer) {
            const galleryId = galleryContainer.getAttribute('data-gallery-id');
            const containerId = galleryContainer.id;
            
            if (galleryId && containerId) {
                console.log(`Auto-loading gallery content for gallery ID: ${galleryId}`);
                ContentLoader.loadGalleryImages(galleryId, containerId);
            }
        }
        
        // Auto-load blog posts if container has data-blog-posts
        const blogContainer = document.querySelector('[data-blog-posts]');
        if (blogContainer) {
            const limit = blogContainer.getAttribute('data-limit');
            const containerId = blogContainer.id;
            
            if (containerId) {
                console.log(`Auto-loading blog posts${limit ? ` with limit: ${limit}` : ''}`);
                ContentLoader.loadBlogPosts(containerId, limit);
            }
        }
        
        // Auto-load printshop items if container has data-printshop-items
        const printshopContainer = document.querySelector('[data-printshop-items]');
        if (printshopContainer) {
            const containerId = printshopContainer.id;
            
            if (containerId) {
                console.log('Auto-loading printshop items');
                ContentLoader.loadPrintshopItems(containerId);
            }
        }
    } catch (error) {
        console.error('Error initializing dynamic content:', error);
    }
}

// =========================================================================
// UTILITY FUNCTIONS
// =========================================================================

/**
 * Debounce function to limit how often a function can be called
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Check if user is online
 * @returns {boolean} Online status
 */
function isOnline() {
    return navigator.onLine;
}

/**
 * Handle offline/online events
 */
function initializeConnectionHandling() {
    window.addEventListener('online', () => {
        console.log('Connection restored');
        showMessage('Connection restored', 'success');
    });
    
    window.addEventListener('offline', () => {
        console.log('Connection lost');
        showMessage('No internet connection. Some features may not work.', 'warning');
    });
}

// =========================================================================
// ENHANCED MODAL FUNCTIONALITY
// =========================================================================

/**
 * Initialize modal event listeners
 */
function initializeModals() {
    // Close modal when clicking outside the image
    document.addEventListener('click', function(event) {
        const modal = document.getElementById('imageModal');
        if (modal && event.target === modal) {
            closeModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    });
}

// =========================================================================
// FINAL INITIALIZATION
// =========================================================================

/**
 * Initialize additional features after DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize modal functionality
    initializeModals();
    
    // Initialize connection handling
    initializeConnectionHandling();
    
    // Initialize smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// =========================================================================
// CONSOLE INFORMATION
// =========================================================================

console.log(`
╔══════════════════════════════════════════════════════════════════════╗
║                        SilverTimes.ART                              ║
║                    Enhanced JavaScript v2.0                         ║
║                                                                      ║
║  Features:                                                           ║
║  ✓ Form handling with AJAX                                          ║
║  ✓ Dynamic content loading                                          ║
║  ✓ Image modal functionality                                        ║
║  ✓ Navigation management                                            ║
║  ✓ User feedback system                                             ║
║  ✓ Connection status handling                                       ║
║  ✓ Enhanced accessibility                                           ║
║                                                                      ║
║  Backend Integration Ready: ✅                                      ║
╚══════════════════════════════════════════════════════════════════════╝
`);
