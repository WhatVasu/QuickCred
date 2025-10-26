# QuickCred Configuration Example
# Copy this file to config.py and update with your MongoDB details

import os

# Flask Configuration
SECRET_KEY = 'your-super-secret-key-here'
JWT_SECRET_KEY = 'your-jwt-secret-key-here'

# MongoDB Configuration
# Option 1: MongoDB Atlas (Cloud) - Recommended
MONGO_URI = 'mongodb+srv://username:password@cluster.mongodb.net/quickcred?retryWrites=true&w=majority'

# Option 2: Local MongoDB (if you have MongoDB installed locally)
# MONGO_URI = 'mongodb://localhost:27017/quickcred'

# Option 3: MongoDB Atlas with specific database
# MONGO_URI = 'mongodb+srv://your-username:your-password@your-cluster.mongodb.net/quickcred?retryWrites=true&w=majority'

# Instructions:
# 1. Copy this file to config.py
# 2. Replace 'username' and 'password' with your MongoDB Atlas credentials
# 3. Replace 'cluster' with your actual cluster name
# 4. Make sure your IP is whitelisted in MongoDB Atlas
