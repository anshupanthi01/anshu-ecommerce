const API_BASE_URL = 'http://localhost:8000';

const api = {
    // Helper to get headers with auth token
    getHeaders: () => {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json',
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    },

    // Generic fetch wrapper
    request: async (endpoint, options = {}) => {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = api.getHeaders();

        const config = {
            ...options,
            headers: {
                ...headers,
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, config);

            // Handle 401 Unauthorized (Token expired/invalid)
            if (response.status === 401) {
                localStorage.removeItem('token');
                window.location.href = 'login.html';
                return;
            }

            // Handle 204 No Content
            if (response.status === 204) {
                return null;
            }

            // Parse JSON if content exists
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.detail || 'Something went wrong');
                }
                return data;
            } else {
                if (!response.ok) {
                    throw new Error('Something went wrong');
                }
                return null; // No content
            }
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    },

    get: (endpoint) => api.request(endpoint, { method: 'GET' }),

    post: (endpoint, body) => api.request(endpoint, {
        method: 'POST',
        body: JSON.stringify(body)
    }),

    put: (endpoint, body) => api.request(endpoint, {
        method: 'PUT',
        body: JSON.stringify(body)
    }),

    delete: (endpoint) => api.request(endpoint, { method: 'DELETE' }),

    // File upload (multipart/form-data)
    upload: async (endpoint, formData) => {
        const token = localStorage.getItem('token');
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        // Note: Content-Type is set automatically by browser for FormData

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: headers,
                body: formData
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Upload failed');
            }
            return await response.json();
        } catch (error) {
            console.error('Upload Error:', error);
            throw error;
        }
    },

    // Specific API helpers
    getFilteredProducts: async (filters = {}) => {
        const params = new URLSearchParams();
        if (filters.category_id) params.append('category_id', filters.category_id);
        if (filters.search) params.append('search', filters.search);
        if (filters.min_price) params.append('min_price', filters.min_price);
        if (filters.max_price) params.append('max_price', filters.max_price);

        return api.get(`/api/products/?${params.toString()}`);
    },

    getCategories: async () => {
        return api.get('/api/categories/');
    }
};
