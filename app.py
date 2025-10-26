from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from datetime import datetime, timedelta
import bcrypt
import pymongo
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'quickcred-dev-secret-key-change-in-production'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# MongoDB configuration - Update this with your MongoDB Atlas connection string
MONGODB_URI = 'mongodb+srv://whatvasu_db_user:y7sYdG7uc5nZc5FR@cluster0.unsoig4.mongodb.net/?appName=Cluster0'

# Initialize MongoDB connection with a short server selection timeout so failures surface quickly
client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
db = client['quickcred']

# Create collections
users = db["users"]
loans = db["loans"]
transactions = db["transactions"]


# Test MongoDB connection
def test_mongo_connection():
    try:
        # Test the connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")

        # Test collections access
        print(f"✅ Database: {db.name}")
        print(f"✅ Users collection: {users.name}")
        print(f"✅ Loans collection: {loans.name}")
        print(f"✅ Transactions collection: {transactions.name}")

    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("Please check your MONGODB_URI in app.py")
        print("Make sure to replace 'username', 'password', and 'cluster' with your actual MongoDB Atlas credentials")


# Run a quick connectivity check at startup so the app fails fast when MongoDB is unreachable
try:
    test_mongo_connection()
except Exception:
    # test_mongo_connection already prints details; continue starting the app so developer can still run UI pages
    pass


# Return JSON 503 when MongoDB server selection times out so frontend sees a clear error
@app.errorhandler(ServerSelectionTimeoutError)
def handle_mongo_timeout(error):
    return jsonify({'error': 'Database unavailable', 'details': str(error)}), 503


# Import controllers
from controllers.auth_controller import auth_bp
from controllers.loan_controller import loan_bp
from controllers.transaction_controller import transaction_bp
from controllers.dashboard_controller import dashboard_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(loan_bp, url_prefix='/loan')
app.register_blueprint(transaction_bp, url_prefix='/transactions')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')


@app.route('/')
def index():
    return render_template('index.html')


from decorators import login_required

@app.route('/dashboard')
@login_required
def dashboard():
    # Redirect to index if not logged in (handled by decorator)
    return render_template('dashboard.html')


@app.route('/borrower')
@login_required
def borrower_dashboard():
    return render_template('borrower.html')


@app.route('/lender')
@login_required
def lender_dashboard():
    return render_template('lender.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
