#!/usr/bin/env python3
"""
QuickCred Connection Test
Tests MongoDB connection and basic operations
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        from app import mongo
        print("🔗 Testing MongoDB connection...")
        
        # Test basic connection
        result = mongo.db.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Test database access
        db = mongo.db
        print(f"✅ Database access successful: {db.name}")
        
        # Test collection access
        users_collection = db.users
        print(f"✅ Users collection accessible: {users_collection.name}")
        
        # Test a simple operation
        count = users_collection.count_documents({})
        print(f"✅ Users collection has {count} documents")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your MONGO_URI in app.py")
        print("2. Make sure to replace 'username', 'password', and 'cluster'")
        print("3. Ensure your IP is whitelisted in MongoDB Atlas")
        print("4. Check if your MongoDB Atlas cluster is running")
        return False

def test_app_imports():
    """Test if all app imports work"""
    try:
        print("📦 Testing imports...")
        from app import app, mongo
        from controllers.auth_controller import auth_bp
        from controllers.loan_controller import loan_bp
        from controllers.transaction_controller import transaction_bp
        from models.user import User
        from models.loan import Loan
        from models.transaction import Transaction
        print("✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def main():
    print("🚀 QuickCred Connection Test")
    print("=" * 40)
    
    # Test imports first
    if not test_app_imports():
        print("\n❌ Import test failed. Please check your Python environment.")
        return False
    
    # Test MongoDB connection
    if not test_mongodb_connection():
        print("\n❌ Connection test failed. Please fix MongoDB configuration.")
        return False
    
    print("\n🎉 All tests passed! Your QuickCred setup is ready.")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
