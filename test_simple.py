#!/usr/bin/env python3
"""
Simple MongoDB Test for QuickCred
Tests the new PyMongo approach
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_simple_connection():
    """Test the simple PyMongo connection"""
    try:
        print("🔗 Testing simple MongoDB connection...")

        # Import the app
        from app import client, db, users, loans, transactions

        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")

        # Test database
        print(f"✅ Database: {db.name}")

        # Test collections
        print(f"✅ Users collection: {users.name}")
        print(f"✅ Loans collection: {loans.name}")
        print(f"✅ Transactions collection: {transactions.name}")

        # Test collection operations
        print("\n📊 Testing collection operations...")

        # Test users collection
        user_count = users.count_documents({})
        print(f"✅ Users collection has {user_count} documents")

        # Test loans collection
        loan_count = loans.count_documents({})
        print(f"✅ Loans collection has {loan_count} documents")

        # Test transactions collection
        transaction_count = transactions.count_documents({})
        print(f"✅ Transactions collection has {transaction_count} documents")

        print("\n🎉 All tests passed! Your MongoDB setup is working perfectly!")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Update MONGODB_URI in app.py with your actual MongoDB Atlas connection string")
        print("2. Make sure to replace 'username', 'password', and 'cluster' with your real credentials")
        print("3. Check your MongoDB Atlas cluster is running")
        print("4. Verify your IP is whitelisted")
        return False


def main():
    print("🚀 QuickCred Simple Connection Test")
    print("=" * 50)

    success = test_simple_connection()

    if success:
        print("\n✅ Connection test successful!")
        print("You can now run:")
        print("  python demo_data.py  # Create sample data")
        print("  python run.py        # Start the server")
    else:
        print("\n❌ Connection test failed.")
        print("Please fix the MongoDB connection and try again.")
        sys.exit(1)


if __name__ == '__main__':
    main()
