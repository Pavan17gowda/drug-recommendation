/**
 * Authentication Service
 * Handles user authentication logic
 */

class AuthService {
    constructor(apiService, storeService) {
        this.api = apiService;
        this.store = storeService;
    }

    /**
     * Register a new user
     */
    async register(username, email, password, confirmPassword) {
        try {
            // Validate passwords match
            if (password !== confirmPassword) {
                throw new Error('Passwords do not match');
            }

            // Validate password strength
            if (password.length < 6) {
                throw new Error('Password must be at least 6 characters');
            }

            this.store.setLoading(true);
            this.store.clearError();

            const response = await this.api.register(username, email, password);

            if (response.success) {
                return {
                    success: true,
                    message: response.message,
                    user: response.user
                };
            }

            throw new Error(response.message);
        } catch (error) {
            this.store.setError(error.message);
            return {
                success: false,
                message: error.message
            };
        } finally {
            this.store.setLoading(false);
        }
    }

    /**
     * Login user
     */
    async login(email, password) {
        try {
            // Validate inputs
            if (!email || !password) {
                throw new Error('Email and password are required');
            }

            this.store.setLoading(true);
            this.store.clearError();

            const response = await this.api.login(email, password);

            if (response.success) {
                this.store.setUser(response.user);
                return {
                    success: true,
                    message: response.message,
                    user: response.user
                };
            }

            throw new Error(response.message);
        } catch (error) {
            this.store.setError(error.message);
            return {
                success: false,
                message: error.message
            };
        } finally {
            this.store.setLoading(false);
        }
    }

    /**
     * Logout user
     */
    async logout() {
        try {
            this.store.setLoading(true);
            await this.api.logout();
            this.store.clearUser();
            this.store.setRecommendations([]);
            this.store.setStatistics(null);
            return { success: true };
        } catch (error) {
            console.error('Logout error:', error);
            // Clear local data even if API call fails
            this.store.clearUser();
            return { success: false, message: error.message };
        } finally {
            this.store.setLoading(false);
        }
    }

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        return this.store.getState().isAuthenticated;
    }

    /**
     * Get current user
     */
    getCurrentUser() {
        return this.store.getState().user;
    }

    /**
     * Verify session with backend
     */
    async verifySession() {
        try {
            const response = await this.api.getCurrentUser();
            if (response.success) {
                this.store.setUser(response.user);
                return true;
            }
            return false;
        } catch (error) {
            this.store.clearUser();
            return false;
        }
    }

    /**
     * Initialize auth state from localStorage
     */
    init() {
        const user = this.store.loadUser();
        if (user) {
            // Verify session is still valid
            this.verifySession();
        }
    }
}

// Create singleton instance
const authService = new AuthService(api, store);

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = authService;
}
