import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/quickcred')
    
    # Loan configuration
    BORROWER_INTEREST_RATE = 0.047  # 4.7% per month
    LENDER_RETURN_RATE = 0.02       # 2% per month
    PLATFORM_MARGIN_RATE = 0.027    # 2.7% per month
    
    # Loan limits
    MIN_LOAN_AMOUNT = 500
    MAX_LOAN_AMOUNT = 50000
    MAX_LOAN_TERM_MONTHS = 12
