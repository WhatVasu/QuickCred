# QuickCred Configuration Guide

## 🔧 MongoDB Setup

### Option 1: MongoDB Atlas (Recommended)
1. Go to [MongoDB Atlas](https://cloud.mongodb.com)
2. Create a free account and cluster
3. Create a database user
4. Whitelist your IP (0.0.0.0/0 for all IPs)
5. Get your connection string

### Option 2: Local MongoDB
Install MongoDB locally and use: `mongodb://localhost:27017/quickcred`

## 📝 Configuration Steps

### 1. Update MongoDB URI in app.py
Open `app.py` and update line 15:
```python
app.config['MONGO_URI'] = 'mongodb+srv://your-username:your-password@your-cluster.mongodb.net/quickcred?retryWrites=true&w=majority'
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Sample Data
```bash
python demo_data.py
```

### 4. Start the Server
```bash
python run.py
```

## 🎯 Demo Accounts
After running `demo_data.py`, you can use these accounts:

**Borrowers:**
- rajesh@example.com (Password: password123)
- priya@example.com (Password: password123)
- amit@example.com (Password: password123)

**Lenders:**
- sunita@example.com (Password: password123)
- vikram@example.com (Password: password123)

## 🔐 Authentication
- Uses Flask sessions (no JWT)
- Session expires after 24 hours
- No environment variables needed
- All configuration in app.py

## 🚀 Ready to Go!
1. Update MongoDB URI in app.py
2. Run: `python demo_data.py`
3. Run: `python run.py`
4. Open: http://localhost:5000
