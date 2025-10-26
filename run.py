#!/usr/bin/env python3
"""
QuickCred - Micro-Lending Platform
Startup script for development server
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Check MongoDB connection
    print("🔗 Make sure to update the MONGO_URI in app.py with your MongoDB connection string")
    print("📝 Current configuration uses session-based authentication (no JWT)")
    
    # Run the Flask development server
    print("🚀 Starting QuickCred development server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
