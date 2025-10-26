from flask import Blueprint, request, jsonify, session
from models.loan import Loan
from models.user import User
from models.transaction import Transaction
from datetime import datetime

loan_bp = Blueprint('loan', __name__)


def get_collections():
    from app import users, loans, transactions
    return users, loans, transactions


@loan_bp.route('/create', methods=['POST'])
def create_loan():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401

        current_user_id = session['user_id']
        data = request.get_json()

        amount = data.get('amount')
        term_months = data.get('term_months')
        purpose = data.get('purpose', '')

        if not all([amount, term_months]):
            return jsonify({'error': 'Amount and term required'}), 400

        # Validate loan amount
        if amount < 500 or amount > 50000:
            return jsonify({'error': 'Loan amount must be between ₹500 and ₹50,000'}), 400

        if term_months < 1 or term_months > 12:
            return jsonify({'error': 'Loan term must be between 1 and 12 months'}), 400

        users_collection, loans_collection, transactions_collection = get_collections()
        loan_model = Loan(loans_collection)

        # Create loan
        loan_id = loan_model.create_loan(current_user_id, amount, term_months, purpose)

        return jsonify({
            'message': 'Loan request created successfully',
            'loan_id': loan_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@loan_bp.route('/pending', methods=['GET'])
def get_pending_loans():
    try:
        users_collection, loans_collection, transactions_collection = get_collections()
        loan_model = Loan(loans_collection)
        user_model = User(users_collection)

        pending_loans = loan_model.get_pending_loans()

        # Add borrower information to each loan
        for loan in pending_loans:
            borrower = user_model.get_user_by_id(loan['borrower_id'])
            loan['borrower_name'] = borrower['name'] if borrower else 'Unknown'
            loan['borrower_email'] = borrower['email'] if borrower else 'Unknown'
            loan['id'] = str(loan['_id'])
            loan['borrower_id'] = str(loan['borrower_id'])

        return jsonify({'loans': pending_loans}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@loan_bp.route('/fund/<loan_id>', methods=['POST'])
def fund_loan(loan_id):
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401

        current_user_id = session['user_id']
        users_collection, loans_collection, transactions_collection = get_collections()

        loan_model = Loan(loans_collection)
        user_model = User(users_collection)
        transaction_model = Transaction(transactions_collection)

        # Get loan details
        loan = loan_model.get_loan_by_id(loan_id)
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404

        if loan['status'] != 'pending':
            return jsonify({'error': 'Loan is not available for funding'}), 400

        # Check if user is a lender
        current_user = user_model.get_user_by_id(current_user_id)
        if current_user['role'] != 'lender':
            return jsonify({'error': 'Only lenders can fund loans'}), 403

        # Check lender's wallet balance
        if current_user['wallet_balance'] < loan['amount']:
            return jsonify({'error': 'Insufficient wallet balance'}), 400

        # Fund the loan
        success = loan_model.fund_loan(loan_id, current_user_id)
        if not success:
            return jsonify({'error': 'Failed to fund loan'}), 500

        # Update lender's wallet
        user_model.update_wallet_balance(current_user_id, -loan['amount'])

        # Create transaction record
        transaction_model.create_transaction(
            loan_id,
            current_user_id,
            loan['amount'],
            'loan_funding',
            f'Funded loan for {loan["amount"]}'
        )

        return jsonify({'message': 'Loan funded successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@loan_bp.route('/my-loans', methods=['GET'])
def get_my_loans():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401

        current_user_id = session['user_id']
        users_collection, loans_collection, transactions_collection = get_collections()
        loan_model = Loan(loans_collection)
        user_model = User(users_collection)

        # Get user to determine role
        current_user = user_model.get_user_by_id(current_user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        if current_user['role'] == 'borrower':
            loans = loan_model.get_loans_by_borrower(current_user_id)
        else:
            loans = loan_model.get_loans_by_lender(current_user_id)

        # Add additional information
        for loan in loans:
            loan['id'] = str(loan['_id'])
            loan['borrower_id'] = str(loan['borrower_id'])
            if loan.get('lender_id'):
                loan['lender_id'] = str(loan['lender_id'])

            # Calculate interest
            if loan['status'] == 'funded':
                interest = loan_model.calculate_interest(
                    loan['amount'],
                    loan['interest_rate'],
                    loan['term_months']
                )
                loan['total_interest'] = interest
                loan['total_amount'] = loan['amount'] + interest

        return jsonify({'loans': loans}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@loan_bp.route('/repay/<loan_id>', methods=['POST'])
def repay_loan(loan_id):
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401

        current_user_id = session['user_id']
        users_collection, loans_collection, transactions_collection = get_collections()

        loan_model = Loan(loans_collection)
        user_model = User(users_collection)
        transaction_model = Transaction(transactions_collection)

        # Get loan details
        loan = loan_model.get_loan_by_id(loan_id)
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404

        if loan['status'] != 'funded':
            return jsonify({'error': 'Loan is not in funded status'}), 400

        if str(loan['borrower_id']) != current_user_id:
            return jsonify({'error': 'Only the borrower can repay this loan'}), 403

        # Calculate repayment amount
        interest = loan_model.calculate_interest(
            loan['amount'],
            loan['interest_rate'],
            loan['term_months']
        )
        total_repayment = loan['amount'] + interest

        # Check borrower's wallet balance
        borrower = user_model.get_user_by_id(current_user_id)
        if borrower['wallet_balance'] < total_repayment:
            return jsonify({'error': 'Insufficient wallet balance for repayment'}), 400

        # Process repayment
        loan_model.repay_loan(loan_id)

        # Update borrower's wallet
        user_model.update_wallet_balance(current_user_id, -total_repayment)

        # Calculate lender return and platform margin
        lender_return = loan_model.calculate_interest(
            loan['amount'],
            loan['lender_return_rate'],
            loan['term_months']
        )
        platform_margin = interest - lender_return

        # Update lender's wallet with return
        user_model.update_wallet_balance(loan['lender_id'], loan['amount'] + lender_return)

        # Create transaction records
        transaction_model.create_transaction(
            loan_id,
            current_user_id,
            total_repayment,
            'repayment',
            f'Loan repayment of {total_repayment}'
        )

        transaction_model.create_transaction(
            loan_id,
            loan['lender_id'],
            lender_return,
            'interest_payment',
            f'Lender return of {lender_return}'
        )

        return jsonify({
            'message': 'Loan repaid successfully',
            'total_repayment': total_repayment,
            'lender_return': lender_return,
            'platform_margin': platform_margin
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500