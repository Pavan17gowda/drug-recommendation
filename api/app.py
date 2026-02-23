from flask import Flask, request, jsonify, session
from flask_cors import CORS
import bcrypt
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = '717730305d8ed3cdc3f37eedaf000abe29f377cdc7800607'
CORS(app, supports_credentials=True)

# File paths for data persistence
USERS_FILE = 'data/users.json'
RECOMMENDATIONS_FILE = 'data/recommendations.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Load data from files
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_recommendations():
    if os.path.exists(RECOMMENDATIONS_FILE):
        try:
            with open(RECOMMENDATIONS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_recommendations(recommendations):
    with open(RECOMMENDATIONS_FILE, 'w') as f:
        json.dump(recommendations, f, indent=2)

# In-memory storage
users_db = load_users()
recommendations_history = load_recommendations()

# ==================== AUTH ROUTES ====================

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Validation
    if not username or not email or not password:
        return jsonify({"success": False, "message": "All fields are required"}), 400
    
    # Check if user already exists
    if email in users_db:
        return jsonify({"success": False, "message": "Email already registered"}), 400
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=4)).decode('utf-8')
    
    # Store user
    users_db[email] = {
        'username': username,
        'email': email,
        'password': hashed_password,
        'created_at': datetime.now().isoformat()
    }
    
    save_users(users_db)
    
    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "user": {
            "username": username,
            "email": email
        }
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Validation
    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required"}), 400
    
    # Check if user exists
    if email not in users_db:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401
    
    # Verify password
    stored_password = users_db[email]['password']
    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
        session['user'] = email
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "username": users_db[email]['username'],
                "email": email
            }
        }), 200
    else:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.pop('user', None)
    return jsonify({"success": True, "message": "Logged out successfully"}), 200

@app.route('/api/user', methods=['GET'])
def get_user():
    """Get current user info"""
    email = session.get('user')
    if not email:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
    
    user = users_db.get(email)
    if user:
        return jsonify({
            "success": True,
            "user": {
                "username": user['username'],
                "email": user['email']
            }
        }), 200
    return jsonify({"success": False, "message": "User not found"}), 404

# ==================== RECOMMENDATION ROUTES ====================

@app.route('/api/recommendations', methods=['POST'])
def save_recommendation():
    """Save a new recommendation"""
    email = session.get('user')
    
    if not email:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
    
    data = request.json
    
    if email not in recommendations_history:
        recommendations_history[email] = []
    
    recommendation = {
        'id': len(recommendations_history[email]) + 1,
        'date': data.get('date', datetime.now().isoformat()),
        'symptoms': data.get('symptoms', []),
        'diseases': data.get('diseases', []),
        'medications': data.get('medications', []),
        'patientInfo': data.get('patientInfo', {})
    }
    
    recommendations_history[email].append(recommendation)
    save_recommendations(recommendations_history)
    
    return jsonify({
        "success": True,
        "message": "Recommendation saved",
        "recommendation": recommendation
    }), 201

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get all recommendations for current user"""
    email = session.get('user')
    
    if not email:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
    
    history = recommendations_history.get(email, [])
    return jsonify({
        "success": True,
        "history": history,
        "count": len(history)
    }), 200

@app.route('/api/recommendations/<int:rec_id>', methods=['GET'])
def get_recommendation(rec_id):
    """Get a specific recommendation"""
    email = session.get('user')
    
    if not email:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
    
    history = recommendations_history.get(email, [])
    recommendation = next((r for r in history if r['id'] == rec_id), None)
    
    if recommendation:
        return jsonify({
            "success": True,
            "recommendation": recommendation
        }), 200
    return jsonify({"success": False, "message": "Recommendation not found"}), 404

@app.route('/api/recommendations/<int:rec_id>', methods=['DELETE'])
def delete_recommendation(rec_id):
    """Delete a specific recommendation"""
    email = session.get('user')
    
    if not email:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
    
    if email in recommendations_history:
        recommendations_history[email] = [
            r for r in recommendations_history[email] if r['id'] != rec_id
        ]
        save_recommendations(recommendations_history)
        return jsonify({
            "success": True,
            "message": "Recommendation deleted"
        }), 200
    
    return jsonify({"success": False, "message": "Recommendation not found"}), 404

# ==================== STATISTICS ROUTES ====================

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get user statistics"""
    email = session.get('user')
    
    if not email:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
    
    history = recommendations_history.get(email, [])
    
    # Calculate statistics
    total_recommendations = len(history)
    all_symptoms = []
    all_diseases = set()
    all_medications = set()
    
    for rec in history:
        all_symptoms.extend(rec.get('symptoms', []))
        all_diseases.update(rec.get('diseases', []))
        all_medications.update(rec.get('medications', []))
    
    stats = {
        "total_recommendations": total_recommendations,
        "total_symptoms": len(all_symptoms),
        "unique_diseases": len(all_diseases),
        "unique_medications": len(all_medications),
        "last_visit": history[-1]['date'] if history else None
    }
    
    return jsonify({
        "success": True,
        "statistics": stats
    }), 200

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "message": "API is running",
        "version": "1.0.0"
    }), 200

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
