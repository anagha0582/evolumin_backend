// Initialize AOS (Animate on Scroll)
document.addEventListener('DOMContentLoaded', function () {
    AOS.init({
        duration: 800,
        offset: 100,
        once: true
    });

    // Create a map centered at a specific latitude and longitude
    var map = L.map('map').setView([51.505, -0.09], 13);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Add a marker to the map at the same coordinates
    var marker = L.marker([51.505, -0.09]).addTo(map);
    marker.bindPopup('<b>Hello!</b><br>This is a waste collection point.').openPopup();

    // Add a circle around the marker
    var circle = L.circle([51.505, -0.09], {
        color: 'green',
        fillColor: '#32a852',
        fillOpacity: 0.5,
        radius: 500
    }).addTo(map);

    // Add an event listener to the map for clicks
    map.on('click', function (e) {
        var latlng = e.latlng;
        L.marker([latlng.lat, latlng.lng]).addTo(map)
            .bindPopup('New waste collection point: ' + latlng.lat.toFixed(2) + ', ' + latlng.lng.toFixed(2))
            .openPopup();
    });
});

// Modal Functions
function showModal(type) {
    const modal = document.getElementById('authModal');
    const title = document.getElementById('modalTitle');
    title.textContent = type === 'pickup' ? 'Schedule Pickup' : 'Track Collection';
    modal.style.display = 'block';

    // Reset forms
    document.getElementById('loginForm').reset();
    document.getElementById('registerForm').reset();

    // Show login form by default
    switchAuth('login');
}

function closeModal() {
    const modal = document.getElementById('authModal');
    modal.style.display = 'none';
}

function switchAuth(type) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const buttons = document.querySelectorAll('.auth-btn');

    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    if (type === 'login') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    }
}

// Close modal when clicking outside
window.onclick = function (event) {
    const modal = document.getElementById('authModal');
    if (event.target === modal) {
        closeModal();
    }
}

// Form validation functions
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 8;
}

// Form Submissions
document.getElementById('loginForm')?.addEventListener('submit', function (e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Validate email
    if (!validateEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }

    console.log('Login attempt:', { email, password });

    const submitBtn = this.querySelector('button[type="submit"]');
    submitBtn.innerHTML = '<span class="loading-spinner"></span> Logging in...';
    submitBtn.disabled = true;

    // Simulate login process
    setTimeout(() => {
        // Hide the login form
        document.getElementById('loginForm').style.display = 'none';

        // Show welcome message
        const welcomeMessage = document.getElementById('welcomeMessage');
        welcomeMessage.style.display = 'block';

        // Redirect to dashboard after a short delay
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 2000); // Show welcome message for 2 seconds
    }, 1500); // Simulate a delay of 1.5 seconds before showing the welcome message
});

// Dummy email validation function
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

// Dummy function to show notifications (can be customized as needed)
function showNotification(message, type) {
    alert(message);
}


//Example validation functions (implement according to your needs)
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

function validatePassword(password) {
    return password.length >= 8; // Check for minimum length
}

function showNotification(message, type) {
    // Implement notification display logic here
    console.log(type + ": " + message); // For now, log it to the console
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

function validatePassword(password) {
    return password.length >= 8; // Check for minimum length
}

function showNotification(message, type) {
    // Implement notification display logic here
    console.log(type + ": " + message); // For now, log it to the console
}

document.getElementById('registerForm')?.addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.getElementById('regName').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('regConfirmPassword').value;

    // Basic form validation
    if (!name) {
        alert('Please enter your name.');
        return;
    }
    if (!validateEmail(email)) {
        alert('Please enter a valid email address.');
        return;
    }
    if (password.length < 8) {
        alert('Password must be at least 8 characters long.');
        return;
    }
    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return;
    }

    // Simulate loading
    const submitBtn = this.querySelector('button[type="submit"]');
    submitBtn.innerHTML = '<span class="loading-spinner"></span> Creating account...';
    submitBtn.disabled = true;

    setTimeout(() => {
        // Redirect to the dashboard page
        window.location.href = 'dashboard.html';
    }, 1500);
});

function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;

    document.body.appendChild(notification);

    setTimeout(() => notification.classList.add('show'), 100);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 5000);

    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    });
}

// Dashboard specific functions
if (document.querySelector('.dashboard-body')) {
    const today = new Date().toISOString().split('T')[0];
    document.querySelector('.date-input').value = today;

    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', function () {
            document.querySelectorAll('.menu-item').forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });

    document.querySelector('.date-input').addEventListener('change', function () {
        console.log('Fetching data for:', this.value);
        showNotification('Loading data...', 'info');
    });

    function initializeDashboardData() {
        setInterval(() => {
            const stats = document.querySelectorAll('.stat-info p');
            stats.forEach(stat => {
                const currentValue = parseInt(stat.textContent);
                const change = Math.random() > 0.5 ? 1 : -1;
                stat.textContent = currentValue + change;
            });
        }, 5000);
    }

    initializeDashboardData();
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

const menuButton = document.querySelector('.menu-button');
if (menuButton) {
    menuButton.addEventListener('click', function () {
        const sidebar = document.querySelector('.dashboard-sidebar');
        sidebar.classList.toggle('show');
    });
}

document.querySelector('.logout')?.addEventListener('click', function (e) {
    e.preventDefault();
    const confirmLogout = confirm('Are you sure you want to logout?');
    if (confirmLogout) {
        window.location.href = 'index.html';
    }
});

