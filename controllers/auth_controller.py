from flask import Blueprint, request, jsonify, session, redirect, url_for
from models.user import User
import bcrypt

auth_bp = Blueprint('auth', __name__)

def get_collections():
    from app import users, loans, transactions
    return users, loans, transactions

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'borrower')  # Default to borrower
        
        if not all([name, email, password]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        users_collection, _, _ = get_collections()
        user_model = User(users_collection)
        
        # Check if user already exists
        existing_user = user_model.get_user_by_email(email)
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400
        
        # Create new user
        user_id = user_model.create_user(name, email, password, role)
        
        return jsonify({
            'message': 'User created successfully',
            'user_id': user_id,
            'role': role
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'error': 'Email and password required'}), 400
        
        users_collection, _, _ = get_collections()
        user_model = User(users_collection)
        
        # Get user by email
        user = user_model.get_user_by_email(email)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not user_model.verify_password(password, user['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create session
        session['user_id'] = str(user['_id'])
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        session['user_role'] = user['role']
        session['wallet_balance'] = user['wallet_balance']
        session.permanent = True
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'wallet_balance': user['wallet_balance']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        current_user_id = session['user_id']
        users_collection, _, _ = get_collections()
        user_model = User(users_collection)
        
        user = user_model.get_user_by_id(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'wallet_balance': user['wallet_balance']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500