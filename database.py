"""
Database module for MongoDB Atlas integration
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import os
from datetime import datetime

class Database:
    def __init__(self):
        """Initialize MongoDB connection"""
        self.client = None
        self.db = None
        self.users = None
        self.recommendations = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB Atlas"""
        try:
            mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
            self.client = MongoClient(mongodb_uri)
            
            # Test connection
            self.client.admin.command('ping')
            
            # Get database
            self.db = self.client['druggenius']
            
            # Get collections
            self.users = self.db['users']
            self.recommendations = self.db['recommendations']
            
            # Create indexes
            self.users.create_index('email', unique=True)
            self.recommendations.create_index([('user_email', 1), ('date', -1)])
            
            print("✅ Connected to MongoDB Atlas successfully")
            return True
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
    
    # ==================== USER METHODS ====================
    
    def get_user(self, email):
        """Get user by email"""
        try:
            user = self.users.find_one({'email': email})
            if user:
                user.pop('_id', None)  # Remove MongoDB _id
            return user
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_all_users(self):
        """Get all users"""
        try:
            users = {}
            for user in self.users.find():
                email = user['email']
                user.pop('_id', None)
                users[email] = user
            return users
        except Exception as e:
            print(f"Error getting all users: {e}")
            return {}
    
    def create_user(self, email, username, password):
        """Create a new user"""
        try:
            user_data = {
                'email': email,
                'username': username,
                'password': password,
                'created_at': datetime.now().isoformat()
            }
            self.users.insert_one(user_data)
            return True
        except DuplicateKeyError:
            print(f"User with email {email} already exists")
            return False
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def update_user(self, email, updates):
        """Update user data"""
        try:
            result = self.users.update_one(
                {'email': email},
                {'$set': updates}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def delete_user(self, email):
        """Delete a user"""
        try:
            result = self.users.delete_one({'email': email})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    # ==================== RECOMMENDATION METHODS ====================
    
    def get_recommendations(self, email):
        """Get all recommendations for a user"""
        try:
            recs = list(self.recommendations.find(
                {'user_email': email}
            ).sort('date', -1))
            
            # Remove MongoDB _id and format
            for rec in recs:
                rec.pop('_id', None)
                rec['id'] = rec.get('recommendation_id', 0)
            
            return recs
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []
    
    def get_recommendation(self, email, rec_id):
        """Get a specific recommendation"""
        try:
            rec = self.recommendations.find_one({
                'user_email': email,
                'recommendation_id': rec_id
            })
            if rec:
                rec.pop('_id', None)
                rec['id'] = rec.get('recommendation_id', 0)
            return rec
        except Exception as e:
            print(f"Error getting recommendation: {e}")
            return None
    
    def create_recommendation(self, email, data):
        """Create a new recommendation"""
        try:
            # Get next ID
            last_rec = self.recommendations.find_one(
                {'user_email': email},
                sort=[('recommendation_id', -1)]
            )
            next_id = (last_rec['recommendation_id'] + 1) if last_rec else 1
            
            rec_data = {
                'user_email': email,
                'recommendation_id': next_id,
                'date': data.get('date', datetime.now().isoformat()),
                'symptoms': data.get('symptoms', []),
                'diseases': data.get('diseases', []),
                'medications': data.get('medications', []),
                'patientInfo': data.get('patientInfo', {})
            }
            
            self.recommendations.insert_one(rec_data)
            rec_data.pop('_id', None)
            rec_data['id'] = next_id
            return rec_data
        except Exception as e:
            print(f"Error creating recommendation: {e}")
            return None
    
    def delete_recommendation(self, email, rec_id):
        """Delete a recommendation"""
        try:
            result = self.recommendations.delete_one({
                'user_email': email,
                'recommendation_id': rec_id
            })
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting recommendation: {e}")
            return False
    
    def get_user_statistics(self, email):
        """Get statistics for a user"""
        try:
            recs = self.get_recommendations(email)
            
            all_symptoms = []
            all_diseases = set()
            all_medications = set()
            
            for rec in recs:
                all_symptoms.extend(rec.get('symptoms', []))
                all_diseases.update(rec.get('diseases', []))
                all_medications.update(rec.get('medications', []))
            
            return {
                'total_recommendations': len(recs),
                'total_symptoms': len(all_symptoms),
                'unique_diseases': len(all_diseases),
                'unique_medications': len(all_medications),
                'last_visit': recs[0]['date'] if recs else None
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                'total_recommendations': 0,
                'total_symptoms': 0,
                'unique_diseases': 0,
                'unique_medications': 0,
                'last_visit': None
            }
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("✅ MongoDB connection closed")

# Create singleton instance
db = Database()
