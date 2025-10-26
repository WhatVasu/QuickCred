from datetime import datetime
from bson import ObjectId
import bcrypt

class User:
    def __init__(self, collection):
        self.collection = collection
    
    def create_user(self, name, email, password, role):
        """Create a new user"""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_data = {
            'name': name,
            'email': email,
            'password': hashed_password,
            'role': role,  # 'borrower' or 'lender'
            'wallet_balance': 0.0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    def get_user_by_email(self, email):
        """Get user by email"""
        return self.collection.find_one({'email': email})
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.collection.find_one({'_id': ObjectId(user_id)})
    
    def update_wallet_balance(self, user_id, amount):
        """Update user wallet balance"""
        self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$inc': {'wallet_balance': amount},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
    
    def verify_password(self, password, hashed_password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    
    def get_all_lenders(self):
        """Get all lenders"""
        return list(self.collection.find({'role': 'lender'}))
    
    def get_all_borrowers(self):
        """Get all borrowers"""
        return list(self.collection.find({'role': 'borrower'}))
