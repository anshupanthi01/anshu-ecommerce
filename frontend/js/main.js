const ui = {
    init: () => {
        ui.renderNavbar();
        ui.updateCartCount();
    },

    renderNavbar: () => {
        const navbar = document.getElementById('navbar');
        if (!navbar) return;

        const isAuth = auth.isAuthenticated();

        navbar.innerHTML = `
            <div class="logo">
                <a href="index.html">🌸 GLAM</a>
            </div>
            <ul class="nav-links">
                <li><a href="index.html">Home</a></li>
                <li><a href="products.html">Products</a></li>
                ${isAuth ? `
                    <li><a href="orders.html">Orders</a></li>
                    <li><a href="profile.html">Profile</a></li>
                ` : ''}
            </ul>
            <div class="nav-icons">
                ${isAuth ? `
                    <div class="cart-icon" onclick="window.location.href='cart.html'">
                        🛒 <span class="cart-count" id="cart-count">0</span>
                    </div>
                    <button class="btn btn-secondary" onclick="auth.logout()">Logout</button>
                ` : `
                    <a href="login.html" class="btn btn-primary">Login</a>
                    <a href="register.html" class="btn btn-secondary">Register</a>
                `}
            </div>
        `;
    },

    updateCartCount: async () => {
        if (!auth.isAuthenticated()) return;

        const countEl = document.getElementById('cart-count');
        if (countEl) {
            const summary = await cart.getSummary();
            countEl.textContent = summary.total_items || 0;
        }
    },

    showToast: (message, type = 'success') => {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span>${type === 'success' ? '✅' : '❌'}</span>
            <span>${message}</span>
        `;
        document.body.appendChild(toast);

        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 10);

        // Remove after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    formatPrice: (price) => {
        return `NRs. ${Number(price).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }
};

// Initialize UI on load
document.addEventListener('DOMContentLoaded', ui.init);
