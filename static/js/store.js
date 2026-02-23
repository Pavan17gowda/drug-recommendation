/**
 * State Management Store
 * Manages application state and user data
 */

class Store {
    constructor() {
        this.state = {
            user: null,
            isAuthenticated: false,
            recommendations: [],
            statistics: null,
            loading: false,
            error: null
        };
        this.listeners = [];
    }

    /**
     * Get current state
     */
    getState() {
        return { ...this.state };
    }

    /**
     * Update state
     */
    setState(updates) {
        this.state = {
            ...this.state,
            ...updates
        };
        this.notify();
    }

    /**
     * Subscribe to state changes
     */
    subscribe(listener) {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }

    /**
     * Notify all listeners of state change
     */
    notify() {
        this.listeners.forEach(listener => listener(this.state));
    }

    // ==================== USER METHODS ====================

    /**
     * Set user data
     */
    setUser(user) {
        this.setState({
            user,
            isAuthenticated: !!user
        });
        
        // Store in localStorage
        if (user) {
            localStorage.setItem('user', JSON.stringify(user));
        } else {
            localStorage.removeItem('user');
        }
    }

    /**
     * Get user from localStorage
     */
    loadUser() {
        const userStr = localStorage.getItem('user');
        if (userStr) {
            try {
                const user = JSON.parse(userStr);
                this.setUser(user);
                return user;
            } catch (e) {
                console.error('Error loading user:', e);
            }
        }
        return null;
    }

    /**
     * Clear user data
     */
    clearUser() {
        this.setUser(null);
    }

    // ==================== RECOMMENDATION METHODS ====================

    /**
     * Set recommendations
     */
    setRecommendations(recommendations) {
        this.setState({ recommendations });
    }

    /**
     * Add recommendation
     */
    addRecommendation(recommendation) {
        this.setState({
            recommendations: [...this.state.recommendations, recommendation]
        });
    }

    /**
     * Remove recommendation
     */
    removeRecommendation(id) {
        this.setState({
            recommendations: this.state.recommendations.filter(r => r.id !== id)
        });
    }

    // ==================== STATISTICS METHODS ====================

    /**
     * Set statistics
     */
    setStatistics(statistics) {
        this.setState({ statistics });
    }

    // ==================== LOADING & ERROR METHODS ====================

    /**
     * Set loading state
     */
    setLoading(loading) {
        this.setState({ loading });
    }

    /**
     * Set error
     */
    setError(error) {
        this.setState({ error });
    }

    /**
     * Clear error
     */
    clearError() {
        this.setState({ error: null });
    }
}

// Create singleton instance
const store = new Store();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = store;
}
