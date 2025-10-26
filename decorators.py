from functools import wraps
from flask import session, redirect, url_for, jsonify, request
import time

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Not logged in', 'code': 'AUTH_REQUIRED'}), 401
            return redirect(url_for('index'))
        
        # Check session expiry (if set)
        if '_permanent' in session and not session.permanent:
            session.clear()
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Session expired', 'code': 'SESSION_EXPIRED'}), 401
            return redirect(url_for('index'))
            
        return f(*args, **kwargs)
    return decorated_function