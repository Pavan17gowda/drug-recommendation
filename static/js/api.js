/**
 * API Service Layer
 * Handles all HTTP requests to the backend API
 */

const API_BASE_URL = 'http://localhost:5000/api';

class APIService {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    /**
     * Make HTTP request
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            credentials: 'include', // Include cookies for session
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // ==================== AUTH METHODS ====================

    /**
     * Register a new user
     */
    async register(username, email, password) {
        return this.request('/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password }),
        });
    }

    /**
     * Login user
     */
    async login(email, password) {
        return this.request('/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
    }

    /**
     * Logout user
     */
    async logout() {
        return this.request('/logout', {
            method: 'POST',
        });
    }

    /**
     * Get current user
     */
    async getCurrentUser() {
        return this.request('/user');
    }

    // ==================== RECOMMENDATION METHODS ====================

    /**
     * Save a new recommendation
     */
    async saveRecommendation(data) {
        return this.request('/recommendations', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    /**
     * Get all recommendations
     */
    async getRecommendations() {
        return this.request('/recommendations');
    }

    /**
     * Get a specific recommendation
     */
    async getRecommendation(id) {
        return this.request(`/recommendations/${id}`);
    }

    /**
     * Delete a recommendation
     */
    async deleteRecommendation(id) {
        return this.request(`/recommendations/${id}`, {
            method: 'DELETE',
        });
    }

    // ==================== STATISTICS METHODS ====================

    /**
     * Get user statistics
     */
    async getStatistics() {
        return this.request('/statistics');
    }

    // ==================== HEALTH CHECK ====================

    /**
     * Check API health
     */
    async healthCheck() {
        return this.request('/health');
    }
}

// Create singleton instance
const api = new APIService();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
}
