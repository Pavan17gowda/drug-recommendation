import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or '717730305d8ed3cdc3f37eedaf000abe29f377cdc7800607'
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # CORS settings
    CORS_HEADERS = 'Content-Type'
    
    # Data storage
    DATA_DIR = 'data'
    USERS_FILE = os.path.join(DATA_DIR, 'users.json')
    RECOMMENDATIONS_FILE = os.path.join(DATA_DIR, 'recommendations.json')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
