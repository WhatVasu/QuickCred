# QuickCred Quick Start Guide

## 🚨 **IMPORTANT: Fix MongoDB Connection First**

The error `'NoneType' object has no attribute 'users'` means MongoDB connection failed.

## 🔧 **Step 1: Update MongoDB URI in app.py**

Open `app.py` and update **line 15** with your actual MongoDB Atlas connection string:

```python
# Replace this line in app.py (line 15):
app.config['MONGO_URI'] = 'mongodb+srv://your-username:your-password@your-cluster.mongodb.net/quickcred?retryWrites=true&w=majority'
```

### **Example:**
```python
app.config['MONGO_URI'] = 'mongodb+srv://myuser:mypassword@cluster0.abc123.mongodb.net/quickcred?retryWrites=true&w=majority'
```

## 🧪 **Step 2: Test Connection**

Run the connection test:
```bash
python test_connection.py
```

This will tell you if MongoDB is connected properly.

## 🚀 **Step 3: Start the Application**

```bash
# Install dependencies
pip install -r requirements.txt

# Create sample data
python demo_data.py

# Start server
python run.py
```

## 🔍 **Troubleshooting**

### **If connection test fails:**

1. **Check MongoDB Atlas:**
   - Go to [MongoDB Atlas](https://cloud.mongodb.com)
   - Make sure your cluster is running
   - Check your database user credentials
   - Whitelist your IP address (0.0.0.0/0 for all IPs)

2. **Verify connection string format:**
   ```
   mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/DATABASE?retryWrites=true&w=majority
   ```

3. **Common issues:**
   - Wrong username/password
   - Cluster not running
   - IP not whitelisted
   - Wrong cluster name

### **If you don't have MongoDB Atlas:**

1. **Create free account:** Go to [MongoDB Atlas](https://cloud.mongodb.com)
2. **Create cluster:** Choose M0 (free tier)
3. **Create user:** Add database user with username/password
4. **Whitelist IP:** Add 0.0.0.0/0 for all IPs
5. **Get connection string:** Click "Connect" → "Connect your application"

## ✅ **Success Indicators**

When everything works, you'll see:
- ✅ MongoDB connection successful!
- ✅ Database access successful
- ✅ Users collection accessible
- Server running on http://localhost:5000

## 🎯 **Demo Accounts (after running demo_data.py)**

- **Borrowers:** rajesh@example.com, priya@example.com, amit@example.com
- **Lenders:** sunita@example.com, vikram@example.com
- **Password:** password123 (for all)

---

**Need help?** Run `python test_connection.py` to diagnose the issue!
