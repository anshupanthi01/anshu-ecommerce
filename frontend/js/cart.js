const cart = {
    get: async () => {
        try {
            return await api.get('/api/cart/');
        } catch (error) {
            console.error('Failed to fetch cart', error);
            return null;
        }
    },

    getSummary: async () => {
        try {
            return await api.get('/api/cart/summary');
        } catch (error) {
            return { total_items: 0, total_amount: 0 };
        }
    },

    add: async (productId, quantity = 1) => {
        try {
            await api.post('/api/cart/items', {
                product_id: productId,
                quantity: quantity
            });
            ui.showToast('Added to cart!', 'success');
            ui.updateCartCount();
        } catch (error) {
            ui.showToast(error.message, 'error');
        }
    },

    update: async (itemId, quantity) => {
        try {
            await api.put(`/api/cart/items/${itemId}`, {
                quantity: quantity
            });
            return true;
        } catch (error) {
            ui.showToast(error.message, 'error');
            return false;
        }
    },

    remove: async (itemId) => {
        try {
            await api.delete(`/api/cart/items/${itemId}`);
            ui.showToast('Item removed', 'success');
            return true;
        } catch (error) {
            ui.showToast(error.message, 'error');
            return false;
        }
    },

    clear: async () => {
        try {
            await api.delete('/api/cart/');
            return true;
        } catch (error) {
            ui.showToast(error.message, 'error');
            return false;
        }
    },
};

