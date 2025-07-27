#!/usr/bin/env python3
"""
Database Test Script
This script tests if the database schema is correct and can perform basic operations.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from app import app, db
from models.Job import User, JobPortal

def test_database():
    """Test the database schema and basic operations"""
    with app.app_context():
        try:
            print("Testing database schema...")
            
            # Test if tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Found tables: {tables}")
            
            # Test User table schema
            if 'users' in tables:
                user_columns = [col['name'] for col in inspector.get_columns('users')]
                print(f"User table columns: {user_columns}")
                
                # Check for required columns
                required_columns = ['id', 'username', 'email', 'password_hash', 'role', 'created_at', 'is_active']
                missing_columns = [col for col in required_columns if col not in user_columns]
                
                if missing_columns:
                    print(f"Missing columns in users table: {missing_columns}")
                    return False
                else:
                    print("✓ User table schema is correct")
            
            # Test creating a user
            print("\nTesting user creation...")
            test_user = User(
                username='test_user',
                email='test@example.com',
                password='testpassword123',
                role='user'
            )
            
            db.session.add(test_user)
            db.session.commit()
            print("✓ User creation successful")
            
            # Test user retrieval
            retrieved_user = User.query.filter_by(username='test_user').first()
            if retrieved_user and retrieved_user.check_password('testpassword123'):
                print("✓ User retrieval and password verification successful")
            else:
                print("✗ User retrieval or password verification failed")
                return False
            
            # Clean up test user
            db.session.delete(retrieved_user)
            db.session.commit()
            print("✓ Test user cleaned up")
            
            print("\n✓ All database tests passed!")
            return True
            
        except Exception as e:
            print(f"✗ Database test failed: {e}")
            return False

if __name__ == "__main__":
    print("Database Test Tool")
    print("=" * 50)
    
    if test_database():
        print("\nDatabase is working correctly!")
    else:
        print("\nDatabase has issues. Consider running reset_db.py")
        sys.exit(1) 