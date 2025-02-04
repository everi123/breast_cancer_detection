# app/auth/routes.py
from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models.user import User
from flask_jwt_extended import create_access_token
import re

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    """Check if email format is valid"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ['username', 'password', 'email']):
        return jsonify({"error": "Missing required fields (username, password, email)"}), 400
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role', 'doctor')
    
    # Validate email format
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400
    
    # Validate role
    if role not in ['doctor', 'admin']:
        return jsonify({"error": "Invalid role"}), 400
    
    # Check if username or email already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
    
    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Registration failed", "details": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request data"}), 400

    # Allow login with either username or email
    identifier = data.get('username') or data.get('email')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        # Check if login is with email or username
        if '@' in identifier:
            user = User.query.filter_by(email=identifier).first()
        else:
            user = User.query.filter_by(username=identifier).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity={
                "username": user.username,
                "email": user.email,
                "role": user.role
            })
            return jsonify({
                "access_token": access_token,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }), 200
        
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": "Login failed", "details": str(e)}), 500
