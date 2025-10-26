# QuickCred Setup Guide

## 🚨 **FIX: MongoDB Collections Issue**

The error `'NoneType' object has no attribute 'users'` happens because MongoDB collections don't exist yet.

## 🔧 **Step-by-Step Fix**

### **1. Update MongoDB URI in app.py**

Open `app.py` and update **line 15** with your actual MongoDB Atlas connection:

```python
# Replace this line in app.py (line 15):
app.config['MONGO_URI'] = 'mongodb+srv://your-username:your-password@your-cluster.mongodb.net/quickcred?retryWrites=true&w=majority'
```

**Example:**
```python
app.config['MONGO_URI'] = 'mongodb+srv://myuser:mypassword@cluster0.abc123.mongodb.net/quickcred?retryWrites=true&w=majority'
```

### **2. Create Collections**

Run this command to create the required collections:

```bash
python setup_collections.py
```

This will create:
- ✅ `users` collection
- ✅ `loans` collection  
- ✅ `transactions` collection

### **3. Create Sample Data**

```bash
python demo_data.py
```

### **4. Start the Application**

```bash
python run.py
```

## 🎯 **What Each Script Does**

| Script | Purpose |
|--------|---------|
| `setup_collections.py` | Creates empty MongoDB collections |
| `demo_data.py` | Adds sample users, loans, and transactions |
| `run.py` | Starts the Flask development server |

## 🔍 **Troubleshooting**

### **If setup_collections.py fails:**

1. **Check MongoDB URI format:**
   ```
   mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/DATABASE?retryWrites=true&w=majority
   ```

2. **Verify MongoDB Atlas:**
   - Cluster is running
   - User credentials are correct
   - IP is whitelisted (0.0.0.0/0 for all IPs)

3. **Common connection issues:**
   - Wrong username/password
   - Cluster name incorrect
   - Network access not configured

### **If you don't have MongoDB Atlas:**

1. **Sign up:** Go to [MongoDB Atlas](https://cloud.mongodb.com)
2. **Create cluster:** Choose M0 (free tier)
3. **Create user:** Add database user
4. **Whitelist IP:** Add 0.0.0.0/0
5. **Get connection string:** Click "Connect" → "Connect your application"

## ✅ **Success Indicators**

When everything works, you'll see:

```
✅ MongoDB connection successful!
✅ Created 'users' collection
✅ Created 'loans' collection  
✅ Created 'transactions' collection
🎉 All collections created successfully!
```

## 🚀 **Quick Start Commands**

```bash
# 1. Update MONGO_URI in app.py first!

# 2. Create collections
python setup_collections.py

# 3. Add sample data
python demo_data.py

# 4. Start server
python run.py

# 5. Open browser
# Go to: http://localhost:5000
```

## 🎯 **Demo Accounts (after demo_data.py)**

- **Borrowers:** rajesh@example.com, priya@example.com, amit@example.com
- **Lenders:** sunita@example.com, vikram@example.com  
- **Password:** password123 (for all)

---

**Need help?** The collections will be created automatically when you run the app, but running `setup_collections.py` first ensures everything is ready!
