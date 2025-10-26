#!/usr/bin/env python3
"""
QuickCred Setup Script
Automated setup for development environment
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    if os.path.exists('venv'):
        print("✅ Virtual environment already exists")
        return True
    
    return run_command('python -m venv venv', 'Creating virtual environment')

def activate_virtual_environment():
    """Get activation command for virtual environment"""
    if platform.system() == 'Windows':
        return 'venv\\Scripts\\activate'
    else:
        return 'source venv/bin/activate'

def install_dependencies():
    """Install required dependencies"""
    if platform.system() == 'Windows':
        pip_cmd = 'venv\\Scripts\\pip'
    else:
        pip_cmd = 'venv/bin/pip'
    
    return run_command(f'{pip_cmd} install -r requirements.txt', 'Installing dependencies')

def create_env_file():
    """Create .env file with default values"""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    env_content = """# QuickCred Environment Variables
SECRET_KEY=quickcred-dev-secret-key-change-in-production
JWT_SECRET_KEY=quickcred-jwt-secret-key-change-in-production
MONGO_URI=mongodb://localhost:27017/quickcred

# For MongoDB Atlas, replace with your connection string:
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/quickcred?retryWrites=true&w=majority
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default values")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['static/css', 'static/js', 'templates', 'controllers', 'models']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def main():
    """Main setup function"""
    print("🚀 QuickCred Setup Script")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    print("\n📁 Creating project directories...")
    create_directories()
    
    # Create virtual environment
    print("\n🐍 Setting up Python environment...")
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    print("\n⚙️ Creating configuration...")
    if not create_env_file():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Update the .env file with your MongoDB connection string")
    print("2. Run: python demo_data.py (to create sample data)")
    print("3. Run: python run.py (to start the server)")
    print("4. Open: http://localhost:5000")
    
    print(f"\nTo activate the virtual environment, run:")
    print(f"  {activate_virtual_environment()}")

if __name__ == '__main__':
    main()
