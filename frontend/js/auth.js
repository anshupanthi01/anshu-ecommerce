const auth = {
    login: async (username, password) => {
        try {
            // FastAPI OAuth2PasswordRequestForm expects form data, not JSON
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Login failed');
            }

            localStorage.setItem('token', data.access_token);
            // Decode token to get user info if needed, or fetch profile
            // For now, just redirect
            return true;
        } catch (error) {
            throw error;
        }
    },

    register: async (userData) => {
        return await api.post('/api/auth/register', userData);
    },

    logout: () => {
        localStorage.removeItem('token');
        window.location.href = 'login.html';
    },

    isAuthenticated: () => {
        return !!localStorage.getItem('token');
    },

    checkAuth: () => {
        if (!auth.isAuthenticated()) {
            window.location.href = 'login.html';
        }
    }
};
