from flask import Blueprint, request, jsonify, session
from models.transaction import Transaction
from models.loan import Loan
from models.user import User

transaction_bp = Blueprint('transaction', __name__)

def get_db():
    from app import mongo
    return mongo.db

@transaction_bp.route('/history', methods=['GET'])
def get_transaction_history():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        current_user_id = session['user_id']
        db = get_db()
        transaction_model = Transaction(db)
        
        transactions = transaction_model.get_transactions_by_user(current_user_id)
        
        # Convert ObjectId to string for JSON serialization
        for transaction in transactions:
            transaction['id'] = str(transaction['_id'])
            transaction['loan_id'] = str(transaction['loan_id'])
            transaction['user_id'] = str(transaction['user_id'])
            transaction['timestamp'] = transaction['timestamp'].isoformat()
        
        return jsonify({'transactions': transactions}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transaction_bp.route('/analytics', methods=['GET'])
def get_analytics():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        current_user_id = session['user_id']
        db = get_db()
        
        user_model = User(db)
        loan_model = Loan(db)
        transaction_model = Transaction(db)
        
        # Get user details
        current_user = user_model.get_user_by_id(current_user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        analytics = {
            'user_role': current_user['role'],
            'wallet_balance': current_user['wallet_balance']
        }
        
        if current_user['role'] == 'lender':
            # Lender analytics
            loans = loan_model.get_loans_by_lender(current_user_id)
            returns_data = transaction_model.get_lender_returns(current_user_id)
            
            analytics.update({
                'total_loans_funded': len([l for l in loans if l['status'] == 'funded']),
                'total_loans_repaid': len([l for l in loans if l['status'] == 'repaid']),
                'total_returns': returns_data['total_returns'],
                'active_loans': len([l for l in loans if l['status'] == 'funded']),
                'total_invested': sum([l['amount'] for l in loans if l['status'] in ['funded', 'repaid']])
            })
        else:
            # Borrower analytics
            loans = loan_model.get_loans_by_borrower(current_user_id)
            
            analytics.update({
                'total_loans_requested': len(loans),
                'pending_loans': len([l for l in loans if l['status'] == 'pending']),
                'funded_loans': len([l for l in loans if l['status'] == 'funded']),
                'repaid_loans': len([l for l in loans if l['status'] == 'repaid']),
                'total_borrowed': sum([l['amount'] for l in loans if l['status'] in ['funded', 'repaid']])
            })
        
        return jsonify({'analytics': analytics}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transaction_bp.route('/update-wallet', methods=['POST'])
def update_wallet():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
            
        data = request.get_json()
        operation = data.get('operation')
        amount = float(data.get('amount', 0))
        
        if not amount or amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400
            
        if operation not in ['add', 'subtract']:
            return jsonify({'error': 'Invalid operation'}), 400
            
        from app import users
        user_model = User(users)
        user = user_model.get_user_by_id(session['user_id'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        current_balance = user['wallet_balance']
        if operation == 'add':
            new_balance = current_balance + amount
        else:
            if current_balance < amount:
                return jsonify({'error': 'Insufficient balance'}), 400
            new_balance = current_balance - amount
            
        # Update user's wallet balance
        users.update_one(
            {'_id': user['_id']},
            {'$set': {'wallet_balance': new_balance}}
        )
        
        # Update session
        session['wallet_balance'] = new_balance
        
        return jsonify({
            'message': 'Wallet updated successfully',
            'new_balance': new_balance
        }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transaction_bp.route('/platform-analytics', methods=['GET'])
def get_platform_analytics():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        db = get_db()
        
        # Check if user is admin (for now, allow all users to see platform analytics)
        user_model = User(db)
        loan_model = Loan(db)
        transaction_model = Transaction(db)
        
        # Get loan analytics
        loan_analytics = loan_model.get_loan_analytics()
        
        # Get transaction analytics
        transaction_analytics = transaction_model.get_platform_analytics()
        
        # Get user counts
        total_lenders = len(user_model.get_all_lenders())
        total_borrowers = len(user_model.get_all_borrowers())
        
        platform_data = {
            'total_users': total_lenders + total_borrowers,
            'total_lenders': total_lenders,
            'total_borrowers': total_borrowers,
            'loan_analytics': loan_analytics,
            'transaction_analytics': transaction_analytics
        }
        
        return jsonify({'platform_analytics': platform_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transaction_bp.route('/topup', methods=['POST'])
def topup_wallet():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        current_user_id = session['user_id']
        data = request.get_json()
        
        amount = data.get('amount')
        if not amount or amount <= 0:
            return jsonify({'error': 'Valid amount required'}), 400
        
        db = get_db()
        user_model = User(db)
        transaction_model = Transaction(db)
        
        # Update user's wallet balance
        user_model.update_wallet_balance(current_user_id, amount)
        
        # Create transaction record
        transaction_model.create_transaction(
            None,  # No loan_id for wallet topup
            current_user_id,
            amount,
            'wallet_topup',
            f'Wallet topup of {amount}'
        )
        
        # Get updated user data
        user = user_model.get_user_by_id(current_user_id)
        
        return jsonify({
            'message': 'Wallet topped up successfully',
            'new_balance': user['wallet_balance']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
