#!/usr/bin/env python3
"""
QuickCred Demo Data Script
Creates sample data for testing the platform
"""

import sys
from datetime import datetime, timedelta, timezone
import bcrypt

# Import collections from your app
from app import app, users, loans, transactions


def now_utc():
    """Return current UTC time (timezone-aware)"""
    return datetime.now(timezone.utc)


def create_demo_data():
    """Create demo data for testing"""

    with app.app_context():
        try:
            # Test connection
            from app import client
            client.admin.command('ping')
            print("✅ Database connection successful!")

            # Clear existing data
            print("🧹 Clearing existing data...")
            users.delete_many({})
            loans.delete_many({})
            transactions.delete_many({})
            print("✅ Existing data cleared")

            # Create demo users
            print("👥 Creating demo users...")

            borrowers = [
                {'name': 'Rajesh Kumar', 'email': 'rajesh@example.com',
                 'password': bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()),
                 'role': 'borrower', 'wallet_balance': 5000.0,
                 'created_at': now_utc(), 'updated_at': now_utc()},
                {'name': 'Priya Sharma', 'email': 'priya@example.com',
                 'password': bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()),
                 'role': 'borrower', 'wallet_balance': 3000.0,
                 'created_at': now_utc(), 'updated_at': now_utc()},
                {'name': 'Amit Singh', 'email': 'amit@example.com',
                 'password': bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()),
                 'role': 'borrower', 'wallet_balance': 2000.0,
                 'created_at': now_utc(), 'updated_at': now_utc()}
            ]

            lenders = [
                {'name': 'Dr. Sunita Patel', 'email': 'sunita@example.com',
                 'password': bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()),
                 'role': 'lender', 'wallet_balance': 50000.0,
                 'created_at': now_utc(), 'updated_at': now_utc()},
                {'name': 'Mr. Vikram Mehta', 'email': 'vikram@example.com',
                 'password': bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()),
                 'role': 'lender', 'wallet_balance': 75000.0,
                 'created_at': now_utc(), 'updated_at': now_utc()}
            ]

            user_ids = []
            for u in borrowers + lenders:
                res = users.insert_one(u)
                user_ids.append(res.inserted_id)

            borrower_ids = user_ids[:3]
            lender_ids = user_ids[3:]

            print(f"✅ Created {len(borrowers)} borrowers and {len(lenders)} lenders")

            # Create demo loans
            print("💰 Creating demo loans...")
            loan_docs = [
                {'borrower_id': borrower_ids[0], 'amount': 5000.0, 'term_months': 3, 'purpose': 'Education expenses',
                 'status': 'funded',
                 'interest_rate': 0.047, 'lender_return_rate': 0.02, 'platform_margin_rate': 0.027,
                 'lender_id': lender_ids[0],
                 'funded_at': now_utc() - timedelta(days=30), 'due_date': now_utc() + timedelta(days=60),
                 'created_at': now_utc() - timedelta(days=30), 'updated_at': now_utc() - timedelta(days=30)},

                {'borrower_id': borrower_ids[1], 'amount': 8000.0, 'term_months': 6, 'purpose': 'Medical emergency',
                 'status': 'funded',
                 'interest_rate': 0.047, 'lender_return_rate': 0.02, 'platform_margin_rate': 0.027,
                 'lender_id': lender_ids[1],
                 'funded_at': now_utc() - timedelta(days=15), 'due_date': now_utc() + timedelta(days=165),
                 'created_at': now_utc() - timedelta(days=15), 'updated_at': now_utc() - timedelta(days=15)},

                {'borrower_id': borrower_ids[2], 'amount': 3000.0, 'term_months': 1, 'purpose': 'Short-term cash flow',
                 'status': 'pending',
                 'interest_rate': 0.047, 'lender_return_rate': 0.02, 'platform_margin_rate': 0.027,
                 'lender_id': None, 'funded_at': None, 'due_date': None,
                 'created_at': now_utc() - timedelta(days=2), 'updated_at': now_utc() - timedelta(days=2)},

                {'borrower_id': borrower_ids[0], 'amount': 12000.0, 'term_months': 12, 'purpose': 'Business expansion',
                 'status': 'repaid',
                 'interest_rate': 0.047, 'lender_return_rate': 0.02, 'platform_margin_rate': 0.027,
                 'lender_id': lender_ids[1],
                 'funded_at': now_utc() - timedelta(days=365), 'due_date': now_utc() - timedelta(days=1),
                 'created_at': now_utc() - timedelta(days=365), 'updated_at': now_utc() - timedelta(days=1)}
            ]

            loan_ids = []
            for l in loan_docs:
                res = loans.insert_one(l)
                loan_ids.append(res.inserted_id)

            print(f"✅ Created {len(loan_docs)} demo loans")

            # Create demo transactions
            print("📊 Creating demo transactions...")
            transaction_docs = [
                {'loan_id': None, 'user_id': borrower_ids[0], 'amount': 10000.0, 'type': 'wallet_topup',
                 'description': 'Initial wallet top-up', 'timestamp': now_utc() - timedelta(days=60),
                 'status': 'completed'},
                {'loan_id': None, 'user_id': lender_ids[0], 'amount': 100000.0, 'type': 'wallet_topup',
                 'description': 'Initial wallet top-up', 'timestamp': now_utc() - timedelta(days=60),
                 'status': 'completed'},
                {'loan_id': loan_ids[0], 'user_id': lender_ids[0], 'amount': 5000.0, 'type': 'loan_funding',
                 'description': 'Funded loan for education expenses', 'timestamp': now_utc() - timedelta(days=30),
                 'status': 'completed'},
                {'loan_id': loan_ids[1], 'user_id': lender_ids[1], 'amount': 8000.0, 'type': 'loan_funding',
                 'description': 'Funded loan for medical emergency', 'timestamp': now_utc() - timedelta(days=15),
                 'status': 'completed'},
                {'loan_id': loan_ids[3], 'user_id': borrower_ids[0], 'amount': 12684.0, 'type': 'repayment',
                 'description': 'Loan repayment with interest', 'timestamp': now_utc() - timedelta(days=1),
                 'status': 'completed'},
                {'loan_id': loan_ids[3], 'user_id': lender_ids[1], 'amount': 2880.0, 'type': 'interest_payment',
                 'description': 'Lender return payment', 'timestamp': now_utc() - timedelta(days=1),
                 'status': 'completed'}
            ]

            for t in transaction_docs:
                transactions.insert_one(t)

            print(f"✅ Created {len(transaction_docs)} demo transactions")

            print("\n🎉 Demo data created successfully!")

        except Exception as e:
            print(f"\n❌ Error creating demo data: {e}")


if __name__ == "__main__":
    print("🚀 QuickCred Demo Data Creator")
    print("=" * 40)
    create_demo_data()
