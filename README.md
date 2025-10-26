# QuickCred - Micro-Lending Platform

A modern micro-lending platform prototype for students and young professionals, built with Flask and MongoDB Atlas, featuring a Slice-inspired UI.

## 🚀 Features

### For Borrowers
- **Instant Loan Applications**: Apply for loans ranging from ₹500 to ₹50,000
- **Transparent Interest Rates**: 4.7% monthly interest rate
- **Secure Wallet System**: Simulated wallet for transactions
- **Loan Tracking**: Real-time loan status updates
- **Easy Repayments**: One-click repayment system

### For Lenders
- **Investment Opportunities**: Fund loans and earn 2% monthly returns
- **Loan Portfolio**: Track all funded loans
- **Analytics Dashboard**: Monitor returns and performance
- **Risk Management**: View borrower information before funding

### Platform Features
- **JWT Authentication**: Secure user authentication
- **Real-time Analytics**: Platform-wide statistics and insights
- **Mobile-First Design**: Responsive Slice-inspired UI
- **Interest Calculations**: Automated interest and margin calculations
- **Transaction History**: Complete audit trail

## 🛠️ Tech Stack

### Backend
- **Flask**: Python web framework
- **MongoDB Atlas**: Cloud database
- **JWT**: Authentication tokens
- **bcrypt**: Password hashing

### Frontend
- **TailwindCSS**: Utility-first CSS framework
- **Alpine.js**: Lightweight JavaScript framework
- **Chart.js**: Data visualization
- **Responsive Design**: Mobile-first approach

## 📦 Installation

### Prerequisites
- Python 3.8+
- MongoDB Atlas account
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd QuickCredPY
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-super-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/quickcred?retryWrites=true&w=majority
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🎯 Usage

### Getting Started

1. **Register**: Create an account as either a Borrower or Lender
2. **Top-up Wallet**: Add funds to your wallet (simulated)
3. **Apply/Fund Loans**: Start borrowing or lending
4. **Track Progress**: Monitor your loans and returns

### Key Calculations

- **Borrower Interest**: Principal × 4.7% × months
- **Lender Return**: Principal × 2% × months  
- **Platform Margin**: Borrower Interest - Lender Return

### API Endpoints

#### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/profile` - Get user profile

#### Loans
- `POST /loan/create` - Create loan application
- `GET /loan/pending` - Get pending loans
- `POST /loan/fund/<loan_id>` - Fund a loan
- `GET /loan/my-loans` - Get user's loans
- `POST /loan/repay/<loan_id>` - Repay a loan

#### Transactions
- `GET /transactions/history` - Transaction history
- `GET /transactions/analytics` - User analytics
- `GET /transactions/platform-analytics` - Platform statistics
- `POST /transactions/topup` - Wallet top-up

## 🎨 Design Philosophy

The UI is inspired by the Slice app with:
- **Rounded Cards**: Soft, friendly design elements
- **Gradient Backgrounds**: Purple-blue color palette
- **Glass Morphism**: Modern translucent effects
- **Bold Typography**: Clear, readable text hierarchy
- **Mobile-First**: Responsive design for all devices

## 📊 Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string",
  "password": "hashed_string",
  "role": "borrower|lender",
  "wallet_balance": "number",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Loans Collection
```json
{
  "_id": "ObjectId",
  "borrower_id": "ObjectId",
  "amount": "number",
  "term_months": "number",
  "purpose": "string",
  "status": "pending|funded|repaid|defaulted",
  "interest_rate": "number",
  "lender_return_rate": "number",
  "platform_margin_rate": "number",
  "lender_id": "ObjectId",
  "funded_at": "datetime",
  "due_date": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Transactions Collection
```json
{
  "_id": "ObjectId",
  "loan_id": "ObjectId",
  "user_id": "ObjectId",
  "amount": "number",
  "type": "loan_funding|repayment|interest_payment|platform_fee|wallet_topup",
  "description": "string",
  "timestamp": "datetime",
  "status": "completed|pending|failed"
}
```

## 🚀 Deployment

### Render Deployment
1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy with automatic builds

### Vercel Deployment
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel --prod`
3. Set environment variables in Vercel dashboard

## 🔧 Development

### Project Structure
```
QuickCredPY/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── controllers/          # API controllers
│   ├── auth_controller.py
│   ├── loan_controller.py
│   └── transaction_controller.py
├── models/               # Database models
│   ├── user.py
│   ├── loan.py
│   └── transaction.py
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   └── dashboard.html
└── static/               # Static assets
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

### Adding New Features
1. Create new controller in `controllers/`
2. Add corresponding model methods in `models/`
3. Update frontend templates and JavaScript
4. Test thoroughly before deployment

## 📈 Future Enhancements

- **AI Credit Scoring**: Machine learning-based borrower assessment
- **Automated Notifications**: Email/SMS alerts for loan updates
- **Advanced Analytics**: More detailed reporting and insights
- **Mobile App**: Native iOS/Android applications
- **Blockchain Integration**: Smart contracts for loan agreements
- **Multi-currency Support**: International lending capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation for common solutions

---

**QuickCred** - Empowering financial inclusion through technology 🚀
