# config.py
# config.py
import os
from datetime import timedelta

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '1642aef0518da735bc33dadc1c9bce947bbbce00ebfc8b1670c9e02dd654e53f')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Security configurations
    SECRET_KEY = os.getenv('SECRET_KEY', '1642aef0518da735bc33dadc1c9bce947bbbce00ebfc8b1670c9e02dd654e53f')
    
    # Flask configuration
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']