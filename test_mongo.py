#!/usr/bin/env python3
"""
Simple MongoDB Connection Test
Tests MongoDB connection without Flask decorators
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_mongodb():
    """Test MongoDB connection and create collections"""
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

            print("📁 Checking collections...")
            collections = db.list_collection_names()
            print(f"Existing collections: {collections}")

            # Create collections if they don't exist
            required_collections = ['users', 'loans', 'transactions']

            for collection_name in required_collections:
                if collection_name not in collections:
                    print(f"Creating collection: {collection_name}")
                    # Create collection by inserting a sample document
                    sample_doc = {
                        '_id': f'temp_{collection_name}',
                        'created_at': datetime.utcnow(),
                        'temp': True
                    }
                    db[collection_name].insert_one(sample_doc)
                    db[collection_name].delete_one({'_id': f'temp_{collection_name}'})
                    print(f"✅ Created collection: {collection_name}")
                else:
                    print(f"✅ Collection exists: {collection_name}")

            print("\n🎉 All collections ready!")
            print("📊 Final collections:")
            final_collections = db.list_collection_names()
            for collection in final_collections:
                count = db[collection].count_documents({})
                print(f"  - {collection}: {count} documents")

            return True

        finally:
            app_context.pop()

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Update MONGO_URI in app.py with your MongoDB Atlas connection string")
        print("2. Check your MongoDB Atlas cluster is running")
        print("3. Verify your IP is whitelisted")
        print("4. Ensure username/password are correct")
        return False


def main():
    print("🚀 QuickCred MongoDB Test")
    print("=" * 40)

    success = test_mongodb()

    if success:
        print("\n✅ MongoDB setup successful!")
        print("You can now run:")
        print("  python demo_data.py  # Create sample data")
        print("  python run.py        # Start the server")
    else:
        print("\n❌ MongoDB setup failed.")
        print("Please fix the connection issues and try again.")
        sys.exit(1)


if __name__ == '__main__':
    main()
