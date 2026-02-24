from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import subprocess
import os
import bcrypt
from dotenv import load_dotenv
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = '717730305d8ed3cdc3f37eedaf000abe29f377cdc7800607'

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

# In-memory user storage for testing (replace with database in production)
users_db = load_users()
# Store user recommendations history
recommendations_history = load_recommendations()

# Database connection (commented out for Vercel deployment)
# For production, use a cloud database like MongoDB Atlas, PostgreSQL on Railway, etc.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Validation
    if not username or not email or not password:
        return jsonify({"message": "All fields are required"}), 400
    
    # Check if user already exists
    if email in users_db:
        return jsonify({"message": "Email already registered"}), 400
    
    # Hash the password with fewer rounds for faster processing (4 rounds = 16 iterations)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=4)).decode('utf-8')
    
    # Store user in memory
    users_db[email] = {
        'username': username,
        'email': email,
        'password': hashed_password
    }
    
    # Save to file
    save_users(users_db)
    
    return jsonify({"message": "User registered successfully"}), 200



@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Validation
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    
    # Check if user exists
    if email not in users_db:
        return jsonify({"message": "Invalid email or password"}), 401
    
    # Verify password
    stored_password = users_db[email]['password']
    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
        session['user'] = email
        return jsonify({
            "message": "Login successful", 
            "username": users_db[email]['username'],
            "email": email
        }), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@app.route('/save-recommendation', methods=['POST'])
def save_recommendation():
    data = request.json
    email = session.get('user')
    
    if not email:
        return jsonify({"message": "Not authenticated"}), 401
    
    if email not in recommendations_history:
        recommendations_history[email] = []
    
    recommendations_history[email].append({
        'date': data.get('date'),
        'symptoms': data.get('symptoms'),
        'diseases': data.get('diseases'),
        'medications': data.get('medications'),
        'patientInfo': data.get('patientInfo')
    })
    
    # Save to file
    save_recommendations(recommendations_history)
    
    return jsonify({"message": "Recommendation saved"}), 200

@app.route('/get-recommendations', methods=['GET'])
def get_recommendations():
    email = session.get('user')
    
    if not email:
        return jsonify({"message": "Not authenticated"}), 401
    
    history = recommendations_history.get(email, [])
    return jsonify({"history": history}), 200



if __name__ == '__main__':
    app.run(debug=True)

# Vercel serverless function handler
def handler(request):
    return app(request.environ, lambda *args: None)

