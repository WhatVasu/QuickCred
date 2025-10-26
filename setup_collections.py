#!/usr/bin/env python3
"""
QuickCred Collection Setup
Creates required MongoDB collections for QuickCred
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def setup_collections():
    """Create required collections in MongoDB"""
    try:
        from app import app, mongo

        # Create app context
        app_context = app.app_context()
        app_context.push()

        try:
            db = mongo.db

            print("🔗 Testing MongoDB connection...")
            # Test connection
            db.command('ping')
            print("✅ MongoDB connection successful!")

            print("📁 Creating required collections...")

            # Create users collection
            if 'users' not in db.list_collection_names():
                # Create users collection with sample document
                sample_user = {
                    'name': 'Sample User',
                    'email': 'sample@example.com',
                    'password': 'sample_password',
                    'role': 'borrower',
                    'wallet_balance': 0.0,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
                db.users.insert_one(sample_user)
                db.users.delete_one({'email': 'sample@example.com'})
                print("✅ Created 'users' collection")
            else:
                print("✅ 'users' collection already exists")

            # Create loans collection
            if 'loans' not in db.list_collection_names():
                # Create loans collection with sample document
                sample_loan = {
                    'borrower_id': 'sample_id',
                    'amount': 1000.0,
                    'term_months': 3,
                    'purpose': 'Sample loan',
                    'status': 'pending',
                    'interest_rate': 0.047,
                    'lender_return_rate': 0.02,
                    'platform_margin_rate': 0.027,
                    'lender_id': None,
                    'funded_at': None,
                    'due_date': None,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
                db.loans.insert_one(sample_loan)
                db.loans.delete_one({'purpose': 'Sample loan'})
                print("✅ Created 'loans' collection")
            else:
                print("✅ 'loans' collection already exists")

            # Create transactions collection
            if 'transactions' not in db.list_collection_names():
                # Create transactions collection with sample document
                sample_transaction = {
                    'loan_id': 'sample_id',
                    'user_id': 'sample_id',
                    'amount': 100.0,
                    'type': 'sample',
                    'description': 'Sample transaction',
                    'timestamp': datetime.utcnow(),
                    'status': 'completed'
                }
                db.transactions.insert_one(sample_transaction)
                db.transactions.delete_one({'description': 'Sample transaction'})
                print("✅ Created 'transactions' collection")
            else:
                print("✅ 'transactions' collection already exists")

            print("\n🎉 All collections created successfully!")
            print("📊 Collections in your database:")
            collections = db.list_collection_names()
            for collection in collections:
                count = db[collection].count_documents({})
                print(f"  - {collection}: {count} documents")
            mongo.cx.close()  # close the client cleanly

            return True

        finally:
            app_context.pop()

    except Exception as e:
        print(f"❌ Error setting up collections: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure your MONGO_URI in app.py is correct")
        print("2. Check your MongoDB Atlas connection")
        print("3. Ensure your IP is whitelisted")
        return False


def main():
    print("🚀 QuickCred Collection Setup")
    print("=" * 40)

    success = setup_collections()

    if success:
        print("\n✅ Setup completed successfully!")
        print("You can now run:")
        print("  python demo_data.py  # Create sample data")
        print("  python run.py        # Start the server")
    else:
        print("\n❌ Setup failed. Please check your MongoDB configuration.")
        sys.exit(1)


if __name__ == '__main__':
    main()

