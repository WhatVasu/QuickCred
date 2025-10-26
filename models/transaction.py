from datetime import datetime
from bson import ObjectId

class Transaction:
    def __init__(self, collection):
        self.collection = collection
    
    def create_transaction(self, loan_id, user_id, amount, transaction_type, description=""):
        """Create a new transaction"""
        transaction_data = {
            'loan_id': ObjectId(loan_id),
            'user_id': ObjectId(user_id),
            'amount': float(amount),
            'type': transaction_type,  # 'loan_funding', 'repayment', 'interest_payment', 'platform_fee'
            'description': description,
            'timestamp': datetime.utcnow(),
            'status': 'completed'
        }
        
        result = self.collection.insert_one(transaction_data)
        return str(result.inserted_id)
    
    def get_transactions_by_user(self, user_id):
        """Get all transactions for a user"""
        return list(self.collection.find({'user_id': ObjectId(user_id)}).sort('timestamp', -1))
    
    def get_transactions_by_loan(self, loan_id):
        """Get all transactions for a loan"""
        return list(self.collection.find({'loan_id': ObjectId(loan_id)}).sort('timestamp', -1))
    
    def get_platform_analytics(self):
        """Get platform analytics"""
        pipeline = [
            {
                '$group': {
                    '_id': '$type',
                    'count': {'$sum': 1},
                    'total_amount': {'$sum': '$amount'}
                }
            }
        ]
        return list(self.collection.aggregate(pipeline))
    
    def get_lender_returns(self, lender_id):
        """Get lender return analytics"""
        pipeline = [
            {'$match': {'user_id': ObjectId(lender_id), 'type': 'interest_payment'}},
            {
                '$group': {
                    '_id': None,
                    'total_returns': {'$sum': '$amount'},
                    'transaction_count': {'$sum': 1}
                }
            }
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0] if result else {'total_returns': 0, 'transaction_count': 0}
