from datetime import datetime, timedelta
from bson import ObjectId

class Loan:
    def __init__(self, collection):
        self.collection = collection
    
    def create_loan(self, borrower_id, amount, term_months, purpose=""):
        """Create a new loan request"""
        loan_data = {
            'borrower_id': ObjectId(borrower_id),
            'amount': float(amount),
            'term_months': int(term_months),
            'purpose': purpose,
            'status': 'pending',  # pending, funded, repaid, defaulted
            'interest_rate': 0.047,  # 4.7% per month
            'lender_return_rate': 0.02,  # 2% per month
            'platform_margin_rate': 0.027,  # 2.7% per month
            'lender_id': None,
            'funded_at': None,
            'due_date': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(loan_data)
        return str(result.inserted_id)
    
    def get_loan_by_id(self, loan_id):
        """Get loan by ID"""
        return self.collection.find_one({'_id': ObjectId(loan_id)})
    
    def get_pending_loans(self):
        """Get all pending loans"""
        return list(self.collection.find({'status': 'pending'}))
    
    def get_loans_by_borrower(self, borrower_id):
        """Get all loans for a specific borrower"""
        return list(self.collection.find({'borrower_id': ObjectId(borrower_id)}))
    
    def get_loans_by_lender(self, lender_id):
        """Get all loans for a specific lender"""
        return list(self.collection.find({'lender_id': ObjectId(lender_id)}))
    
    def fund_loan(self, loan_id, lender_id):
        """Fund a loan"""
        loan = self.get_loan_by_id(loan_id)
        if not loan or loan['status'] != 'pending':
            return False
        
        due_date = datetime.utcnow() + timedelta(days=loan['term_months'] * 30)
        
        self.collection.update_one(
            {'_id': ObjectId(loan_id)},
            {
                '$set': {
                    'status': 'funded',
                    'lender_id': ObjectId(lender_id),
                    'funded_at': datetime.utcnow(),
                    'due_date': due_date,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        return True
    
    def repay_loan(self, loan_id):
        """Mark loan as repaid"""
        self.collection.update_one(
            {'_id': ObjectId(loan_id)},
            {
                '$set': {
                    'status': 'repaid',
                    'updated_at': datetime.utcnow()
                }
            }
        )
        return True
    
    def calculate_interest(self, principal, rate, months):
        """Calculate interest for a loan"""
        return principal * rate * months
    
    def get_loan_analytics(self):
        """Get loan analytics for dashboard"""
        pipeline = [
            {
                '$group': {
                    '_id': '$status',
                    'count': {'$sum': 1},
                    'total_amount': {'$sum': '$amount'}
                }
            }
        ]
        return list(self.collection.aggregate(pipeline))
