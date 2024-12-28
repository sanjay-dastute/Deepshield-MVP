import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.mongodb import get_database
from app.core.config import settings

def test_mongodb_connection():
    try:
        db = get_database()
        if db:
            print("MongoDB connection successful")
            return True
        else:
            print("MongoDB connection failed")
            return False
    except Exception as e:
        print(f"MongoDB connection error: {str(e)}")
        return False

def test_api_config():
    try:
        required_vars = [
            'MONGODB_URI',
            'INSTAGRAM_APP_ID',
            'INSTAGRAM_APP_SECRET',
            'INSTAGRAM_ACCESS_TOKEN'
        ]
        missing_vars = [var for var in required_vars if not getattr(settings, var, None)]
        if missing_vars:
            print(f"Missing environment variables: {', '.join(missing_vars)}")
            return False
        print("API configuration verified")
        return True
    except Exception as e:
        print(f"Configuration error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Running health checks...")
    mongodb_ok = test_mongodb_connection()
    config_ok = test_api_config()
    
    if mongodb_ok and config_ok:
        print("\nAll health checks passed!")
        sys.exit(0)
    else:
        print("\nSome health checks failed!")
        sys.exit(1)
