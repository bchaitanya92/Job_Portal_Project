#!/usr/bin/env python3
"""
Test script for authentication system
"""

from app import app, db, User
from werkzeug.security import generate_password_hash

def test_auth():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin user exists, if not create one
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@jobportal.com',
                password='admin123',
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created: admin/admin123")
        
        # Check if test user exists, if not create one
        test_user = User.query.filter_by(username='testuser').first()
        if not test_user:
            test_user = User(
                username='testuser',
                email='test@jobportal.com',
                password='test123',
                role='user'
            )
            db.session.add(test_user)
            db.session.commit()
            print("Test user created: testuser/test123")
        
        # Test password verification
        if admin_user.check_password('admin123'):
            print("✓ Admin password verification works")
        else:
            print("✗ Admin password verification failed")
        
        if test_user.check_password('test123'):
            print("✓ Test user password verification works")
        else:
            print("✗ Test user password verification failed")
        
        print("\nTest accounts created:")
        print("Admin: admin@jobportal.com / admin123")
        print("User: test@jobportal.com / test123")

if __name__ == '__main__':
    test_auth() 