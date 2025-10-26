#!/usr/bin/env python3
"""
QuickCred Diagnostic Script
Helps identify and fix common issues
"""

def main():
    print("🔍 QuickCred Diagnostic Tool")
    print("=" * 40)
    
    # Check Python version
    import sys
    print(f"Python version: {sys.version}")
    
    # Check if required packages are installed
    print("\n📦 Checking dependencies...")
    try:
        import flask
        print(f"✅ Flask: {flask.__version__}")
    except ImportError:
        print("❌ Flask not installed")
        return False
    
    try:
        import pymongo
        print(f"✅ PyMongo: {pymongo.__version__}")
    except ImportError:
        print("❌ PyMongo not installed")
        return False
    
    try:
        import bcrypt
        print(f"✅ bcrypt: {bcrypt.__version__}")
    except ImportError:
        print("❌ bcrypt not installed")
        return False
    
    # Check app.py configuration
    print("\n🔧 Checking app.py configuration...")
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            if 'mongodb+srv://username:password@cluster.mongodb.net' in content:
                print("❌ MongoDB URI still has placeholder values!")
                print("   Please update line 15 in app.py with your actual MongoDB credentials")
                return False
            else:
                print("✅ MongoDB URI appears to be configured")
    except FileNotFoundError:
        print("❌ app.py not found")
        return False
    
    print("\n🎯 Next Steps:")
    print("1. Update MongoDB URI in app.py (line 15)")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Test connection: python test_connection.py")
    print("4. Create data: python demo_data.py")
    print("5. Start server: python run.py")
    
    return True

if __name__ == '__main__':
    main()
