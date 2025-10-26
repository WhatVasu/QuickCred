from flask import Blueprint, request, jsonify, session
from models.user import User
from models.loan import Loan
from models.transaction import Transaction
from datetime import datetime, timedelta
from bson import ObjectId

dashboard_bp = Blueprint('dashboard', __name__)


def get_collections():
    from app import users, loans, transactions
    return users, loans, transactions


def convert_objectids_to_strings(data):
    """Convert all ObjectId and datetime objects to strings for JSON serialization"""
    if isinstance(data, dict):
        return {key: convert_objectids_to_strings(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectids_to_strings(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, datetime):
        return data.isoformat()
    else:
        return data


@dashboard_bp.route('/borrower-data', methods=['GET'])
def get_borrower_data():
    """Get all data needed for borrower dashboard"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401

        current_user_id = session['user_id']
        users_collection, loans_collection, transactions_collection = get_collections()

        user_model = User(users_collection)
        loan_model = Loan(loans_collection)

        # Get user info
        user = user_model.get_user_by_id(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get user's loans
        user_loans = loan_model.get_loans_by_borrower(current_user_id)

        # Calculate analytics
        analytics = {
            'wallet_balance': user['wallet_balance'],
            'total_loans_requested': len(user_loans),
            'pending_loans': len([l for l in user_loans if l['status'] == 'pending']),
            'funded_loans': len([l for l in user_loans if l['status'] == 'funded']),
            'repaid_loans': len([l for l in user_loans if l['status'] == 'repaid']),
            'total_borrowed': sum([l['amount'] for l in user_loans if l['status'] in ['funded', 'repaid']])
        }

        # Add calculated fields to loans and convert ObjectIds to strings
        for loan in user_loans:
            loan['id'] = str(loan['_id'])
            loan['borrower_id'] = str(loan['borrower_id'])
            if loan.get('lender_id'):
                loan['lender_id'] = str(loan['lender_id'])

            # Convert dates to strings
            if loan.get('created_at'):
                loan['created_at'] = loan['created_at'].isoformat()
            if loan.get('updated_at'):
                loan['updated_at'] = loan['updated_at'].isoformat()
            if loan.get('funded_at'):
                loan['funded_at'] = loan['funded_at'].isoformat()
            if loan.get('due_date'):
                loan['due_date'] = loan['due_date'].isoformat()

            # Calculate interest for funded loans
            if loan['status'] == 'funded':
                interest = loan_model.calculate_interest(
                    loan['amount'],
                    loan['interest_rate'],
                    loan['term_months']
                )
                loan['total_interest'] = interest
                loan['total_amount'] = loan['amount'] + interest

        # Convert all ObjectIds and datetimes to strings
        response_data = {
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'wallet_balance': user['wallet_balance']
            },
            'analytics': analytics,
            'loans': convert_objectids_to_strings(user_loans)
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dashboard_bp.route('/lender-data', methods=['GET'])
def get_lender_data():
    """Get all data needed for lender dashboard"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401

        current_user_id = session['user_id']
        users_collection, loans_collection, transactions_collection = get_collections()

        user_model = User(users_collection)
        loan_model = Loan(loans_collection)

        # Get user info
        user = user_model.get_user_by_id(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get user's investments (loans they funded)
        my_loans = loan_model.get_loans_by_lender(current_user_id)

        # Get available loans to fund
        available_loans = loan_model.get_pending_loans()

        # Add borrower info to available loans and convert ObjectIds
        for loan in available_loans:
            borrower = user_model.get_user_by_id(loan['borrower_id'])
            loan['borrower_name'] = borrower['name'] if borrower else 'Unknown'
            loan['borrower_email'] = borrower['email'] if borrower else 'Unknown'
            loan['id'] = str(loan['_id'])
            loan['borrower_id'] = str(loan['borrower_id'])

            # Convert dates to strings
            if loan.get('created_at'):
                loan['created_at'] = loan['created_at'].isoformat()
            if loan.get('updated_at'):
                loan['updated_at'] = loan['updated_at'].isoformat()

        # Calculate analytics
        analytics = {
            'wallet_balance': user['wallet_balance'],
            'total_loans_funded': len([l for l in my_loans if l['status'] == 'funded']),
            'total_loans_repaid': len([l for l in my_loans if l['status'] == 'repaid']),
            'total_returns': 0,  # Will be calculated from transactions
            'active_loans': len([l for l in my_loans if l['status'] == 'funded']),
            'total_invested': sum([l['amount'] for l in my_loans if l['status'] in ['funded', 'repaid']])
        }

        # Add calculated fields to my loans and convert ObjectIds
        for loan in my_loans:
            loan['id'] = str(loan['_id'])
            loan['borrower_id'] = str(loan['borrower_id'])
            if loan.get('lender_id'):
                loan['lender_id'] = str(loan['lender_id'])

            # Convert dates to strings
            if loan.get('created_at'):
                loan['created_at'] = loan['created_at'].isoformat()
            if loan.get('updated_at'):
                loan['updated_at'] = loan['updated_at'].isoformat()
            if loan.get('funded_at'):
                loan['funded_at'] = loan['funded_at'].isoformat()
            if loan.get('due_date'):
                loan['due_date'] = loan['due_date'].isoformat()

            # Calculate returns for funded loans
            if loan['status'] == 'funded':
                interest = loan_model.calculate_interest(
                    loan['amount'],
                    loan['interest_rate'],
                    loan['term_months']
                )
                loan['total_interest'] = interest
                loan['total_amount'] = loan['amount'] + interest

                # Calculate lender return
                lender_return = loan_model.calculate_interest(
                    loan['amount'],
                    loan['lender_return_rate'],
                    loan['term_months']
                )
                loan['lender_return'] = lender_return

        # Convert all ObjectIds and datetimes to strings
        response_data = {
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'wallet_balance': user['wallet_balance']
            },
            'analytics': analytics,
            'my_loans': convert_objectids_to_strings(my_loans),
            'available_loans': convert_objectids_to_strings(available_loans)
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dashboard_bp.route('/platform-stats', methods=['GET'])
def get_platform_stats():
    """Get platform-wide statistics"""
    try:
        users_collection, loans_collection, transactions_collection = get_collections()

        # Get basic counts
        total_users = users_collection.count_documents({})
        total_loans = loans_collection.count_documents({})
        total_transactions = transactions_collection.count_documents({})

        return jsonify({
            'total_users': total_users,
            'total_loans': total_loans,
            'total_transactions': total_transactions
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500