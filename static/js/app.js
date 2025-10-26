// Global variables
let currentUser = null;

// Authentication functions
function showLogin() {
    document.getElementById('loginModal').classList.remove('hidden');
}

function hideLogin() {
    document.getElementById('loginModal').classList.add('hidden');
}

function showRegister() {
    document.getElementById('registerModal').classList.remove('hidden');
}

function hideRegister() {
    document.getElementById('registerModal').classList.add('hidden');
}

function updateAuthUI() {
    loadUserProfile();
}

let authCheckInProgress = false;

// Initialize app with auth check
document.addEventListener('DOMContentLoaded', function() {
    // Only check auth in specific situations
    const shouldCheckAuth = 
        window.location.pathname !== '/' || // Not on index page
        localStorage.getItem('hasSession') || // Have stored session
        sessionStorage.getItem('justLoggedIn'); // Just logged in
    
    if (shouldCheckAuth) {
        loadUserProfile();
    }
});

async function loadUserProfile() {
    // Prevent multiple simultaneous auth checks
    if (authCheckInProgress) return;
    authCheckInProgress = true;

    try {
        const response = await apiCall('/auth/profile');
        const data = await response.json();

        if (response.ok) {
            currentUser = data.user;
            localStorage.setItem('hasSession', 'true');
            
            // Update UI elements if they exist
            const authButtons = document.getElementById('auth-buttons');
            const authButtonsMobile = document.getElementById('auth-buttons-mobile');
            const userMenu = document.getElementById('user-menu');
            const userMenuMobile = document.getElementById('user-menu-mobile');
            const userName = document.getElementById('user-name');
            const userNameMobile = document.getElementById('user-name-mobile');
            
            // Hide auth buttons and show user menu
            [authButtons, authButtonsMobile].forEach(el => {
                if (el) el.classList.add('hidden');
            });
            
            // Show user menus with appropriate display styles
            if (userMenu) {
                userMenu.classList.remove('hidden');
                userMenu.style.display = 'flex';
            }
            if (userMenuMobile) {
                userMenuMobile.classList.remove('hidden');
            }
            
            // Update usernames
            [userName, userNameMobile].forEach(el => {
                if (el) el.textContent = data.user.name;
            });

            // Handle different pages
            if (window.location.pathname === '/dashboard') {
                initializeDashboardView(data.user.role);
                // Hide auth buttons in dashboard
                [authButtons, authButtonsMobile].forEach(el => {
                    if (el) el.style.display = 'none';
                });
            }
            else if (window.location.pathname === '/' && !sessionStorage.getItem('preventRedirect')) {
                window.location.href = '/dashboard';
            }
        } else {
            handleAuthFailure(data);
        }
    } catch (error) {
        console.error('Error loading user profile:', error);
        handleAuthFailure();
    } finally {
        authCheckInProgress = false;
    }
}

function handleAuthFailure(data = {}) {
    // Clear auth state
    currentUser = null;
    localStorage.removeItem('hasSession');
    sessionStorage.removeItem('justLoggedIn');
    
    // Update UI if elements exist
    const authButtons = document.getElementById('auth-buttons');
    const userMenu = document.getElementById('user-menu');
    
    if (authButtons) authButtons.classList.remove('hidden');
    if (userMenu) userMenu.classList.add('hidden');

    // Redirect to index if on protected route
    if (data.code === 'AUTH_REQUIRED' || data.code === 'SESSION_EXPIRED') {
        if (window.location.pathname !== '/') {
            sessionStorage.setItem('preventRedirect', 'true');
            window.location.href = '/';
            return;
        }
    }
}

// Dashboard view management
function initializeDashboardView(userRole) {
    const lastView = localStorage.getItem('dashboardView') || userRole;
    
    // Check if user has dual role access (currently all users can switch views)
    const borrowerBtn = document.getElementById('borrower-btn');
    const lenderBtn = document.getElementById('lender-btn');
    
    if (borrowerBtn) borrowerBtn.classList.remove('hidden');
    if (lenderBtn) lenderBtn.classList.remove('hidden');
    
    // Set the welcome message based on role
    const welcomeName = document.getElementById('welcome-name');
    const welcomeRole = document.getElementById('welcome-role');
    if (welcomeName) welcomeName.textContent = currentUser.name;
    if (welcomeRole) {
        welcomeRole.textContent = userRole === 'borrower' ? 'loan applications' : 'investments';
    }
    
    // Switch to the last used view or default to user's role
    if (lastView === 'borrower') {
        switchToBorrower();
    } else {
        switchToLender();
    }
}

function switchToBorrower() {
    document.getElementById('borrower-dashboard').classList.remove('hidden');
    document.getElementById('lender-dashboard').classList.add('hidden');
    document.getElementById('borrower-btn').classList.add('bg-purple-500', 'text-white');
    document.getElementById('borrower-btn').classList.remove('bg-gray-200', 'text-gray-700');
    document.getElementById('lender-btn').classList.remove('bg-blue-500', 'text-white');
    document.getElementById('lender-btn').classList.add('bg-gray-200', 'text-gray-700');
    localStorage.setItem('dashboardView', 'borrower');
    loadBorrowerData(); // Make sure this function exists to load borrower-specific data
}

function switchToLender() {
    document.getElementById('lender-dashboard').classList.remove('hidden');
    document.getElementById('borrower-dashboard').classList.add('hidden');
    document.getElementById('lender-btn').classList.add('bg-blue-500', 'text-white');
    document.getElementById('lender-btn').classList.remove('bg-gray-200', 'text-gray-700');
    document.getElementById('borrower-btn').classList.remove('bg-purple-500', 'text-white');
    document.getElementById('borrower-btn').classList.add('bg-gray-200', 'text-gray-700');
    localStorage.setItem('dashboardView', 'lender');
    loadLenderData(); // Make sure this function exists to load lender-specific data
}

// Login form submission
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await apiCall('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        if (!response) throw new Error('No response from server');
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.user;
            localStorage.setItem('hasSession', 'true');
            sessionStorage.setItem('justLoggedIn', 'true');
            sessionStorage.removeItem('preventRedirect');
            hideLogin();

            // Clean redirect to dashboard
            window.location.replace('/dashboard');
        } else {
            alert('Login failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please try again.');
    }
});

// Register form submission
document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const role = document.getElementById('registerRole').value;

    try {
        const response = await apiCall('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, password, role })
        });
        if (!response) throw new Error('No response from server');
        const data = await response.json();
        if (response.ok) {
            alert('Registration successful! Please login.');
            hideRegister();
            showLogin();
        } else {
            alert('Registration failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed. Please try again.');
    }
});

// Logout function
async function logout() {
    try {
        // Show loading state
        const logoutBtn = document.querySelector('button[onclick="logout()"]');
        if (logoutBtn) {
            logoutBtn.disabled = true;
            logoutBtn.innerHTML = `
                <svg class="animate-spin h-4 w-4 text-white inline mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Logging out...</span>
            `;
        }

        const response = await apiCall('/auth/logout', { method: 'POST' });
        
        if (response.ok) {
            // Clear auth state
            currentUser = null;
            localStorage.removeItem('hasSession');
            sessionStorage.removeItem('justLoggedIn');
            
            // Show success message using existing notification system if available
            if (typeof showNotification === 'function') {
                showNotification('Logged out successfully', 'success');
            }
            
            // Redirect to home page
            window.location.href = '/';
        } else {
            throw new Error('Logout failed');
        }
    } catch (error) {
        console.error('Logout error:', error);
        
        // Show error message using existing notification system if available
        if (typeof showNotification === 'function') {
            showNotification('Failed to logout. Please try again.', 'error');
        }
        
        // Reset button state
        if (logoutBtn) {
            logoutBtn.disabled = false;
            logoutBtn.innerHTML = `
                <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                </svg>
                <span>Logout</span>
            `;
        }
    }
}

// Wallet top-up function
async function topupWallet(amount) {
    if (!currentUser) {
        alert('Please login first');
        return;
    }
    
    try {
        const response = await apiCall('/transactions/topup', {
            method: 'POST',
            body: JSON.stringify({ amount: parseFloat(amount) })
        });

        if (!response) throw new Error('No response from server');
        const data = await response.json();

        if (response.ok) {
            alert('Wallet topped up successfully!');
            // Refresh dashboard if on dashboard page
            if (window.location.pathname === '/dashboard') {
                location.reload();
            }
        } else {
            alert('Top-up failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Top-up error:', error);
        alert('Top-up failed. Please try again.');
    }
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// API helper function
async function apiCall(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    // Use fetchWithTimeout if available (added by dashboard UI); fallback to native fetch
    const fetchFn = window.fetchWithTimeout || fetch;

    const response = await fetchFn(endpoint, { ...defaultOptions, ...options }, 8000);

    if (response && response.status === 401) {
        // Session expired or invalid
        logout();
        return null;
    }

    return response;
}

// Small utility: fetch with a timeout (ms)
function fetchWithTimeout(url, options = {}, timeout = 8000) {
    return Promise.race([
        fetch(url, options),
        new Promise((_, reject) => setTimeout(() => reject(new Error('Request timed out')), timeout))
    ]);
}

// Expose globally so templates can use it
window.fetchWithTimeout = fetchWithTimeout;

// Chart helper functions
function createLineChart(ctx, data, label, color) {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: label,
                data: data.values,
                borderColor: color,
                backgroundColor: color + '20',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '₹' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

function createDoughnutChart(ctx, data, colors) {
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: colors,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            }
        }
    });
}

// Export functions for global use
window.showLogin = showLogin;
window.hideLogin = hideLogin;
window.showRegister = showRegister;
window.hideRegister = hideRegister;
window.logout = logout;
window.topupWallet = topupWallet;
