from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from datetime import datetime, timedelta
import bcrypt
import pymongo
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

app = Flask(__name__)
CORS(app)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

MONGODB_URI = os.getenv('MONGODB_URI')

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
db = client['quickcred']

# Create collections
users = db["users"]
loans = db["loans"]
transactions = db["transactions"]



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


try:
    test_mongo_connection()
except Exception:
    pass



@app.errorhandler(ServerSelectionTimeoutError)
def handle_mongo_timeout(error):
    return jsonify({'error': 'Database unavailable', 'details': str(error)}), 503


from controllers.auth_controller import auth_bp
from controllers.loan_controller import loan_bp
from controllers.transaction_controller import transaction_bp
from controllers.dashboard_controller import dashboard_bp

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
