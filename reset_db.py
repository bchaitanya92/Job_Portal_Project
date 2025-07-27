#!/usr/bin/env python3
"""
Database Reset Script
This script will completely reset the database to ensure the schema matches the models.
Run this if you encounter database schema issues.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from app import app, db
from models.Job import User, JobPortal

def reset_database():
    """Reset the database completely"""
    with app.app_context():
        try:
            print("Dropping all tables...")
            db.drop_all()
            print("Creating all tables...")
            db.create_all()
            print("Database reset successful!")
            print("All tables have been recreated with the correct schema.")
            return True
        except Exception as e:
            print(f"Error resetting database: {e}")
            return False

if __name__ == "__main__":
    print("Database Reset Tool")
    print("=" * 50)
    
    # Check if database file exists
    db_path = Path("instance/job.db")
    if db_path.exists():
        print(f"Found existing database at: {db_path}")
        response = input("Do you want to reset the database? This will delete all data. (y/N): ")
        if response.lower() != 'y':
            print("Database reset cancelled.")
            sys.exit(0)
    
    if reset_database():
        print("\nDatabase has been successfully reset!")
        print("You can now run your Flask application.")
    else:
        print("\nFailed to reset database. Please check the error messages above.")
        sys.exit(1) 