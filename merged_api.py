"""
My Merged API - Combining Login and Database Features

I combined two different versions of code:
- Version A: Had login tokens and password security
- Version B: Had database to save users

My goal: Get both working together!
"""

# I need these to make my app work
from flask import Flask, request, jsonify
import jwt  # This makes login tokens
import bcrypt  # This scrambles passwords safely
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Start my app
app = Flask(__name__)

# Settings for my app
app.config['SECRET_KEY'] = 'your-secret-key'  # For making login tokens

# Set up my database
engine = create_engine('sqlite:///users.db')  # This creates a file to store users
Base = declarative_base()
Session = sessionmaker(bind=engine)


# This is my User table - it tells the database what to save
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # Each user gets a unique number
    username = Column(String(50), unique=True, nullable=False)  # Username (must be unique)
    password = Column(String(100), nullable=False)  # Scrambled password


# Create the table if it doesn't exist yet
Base.metadata.create_all(engine)


@app.route('/users', methods=['GET'])
def get_users():
    """
    Show all users (from Version B)
    When someone visits this page, I show them a list of all users
    """
    session = Session()  # Connect to database
    try:
        # Get all users from database
        users = session.query(User).all()
        
        # Make a list with just id and username (NOT password!)
        result = []
        for user in users:
            result.append({"id": user.id, "username": user.username})
        
        return jsonify({"users": result})
    finally:
        session.close()  # Always close the connection!


@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user (combined from both versions)
    
    I combined:
    - Checking if username/password are okay (from Version A)
    - Scrambling the password (from Version A)
    - Saving to database (from Version B)
    """
    # Get the data they sent me
    data = request.get_json()
    
    # Check if username is good
    if not data.get('username') or len(data.get('username', '')) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400
    
    # Check if password is good
    if not data.get('password') or len(data.get('password', '')) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    
    # Scramble the password so it's safe
    password_hash = bcrypt.hashpw(
        data['password'].encode('utf-8'),  # Turn password into bytes
        bcrypt.gensalt()  # Add random stuff to make it extra secure
    )
    
    # Save to database
    session = Session()  # Connect to database
    try:
        # Create a new user
        user = User(
            username=data.get('username'),
            password=password_hash.decode('utf-8')  # Save the scrambled password
        )
        
        # Add user to database and save it
        session.add(user)
        session.commit()
        
        # Tell them it worked!
        result = {
            "id": user.id, 
            "username": user.username,
            "message": "User created successfully"
        }
        return jsonify(result), 201
        
    except Exception as e:
        # Oops, something went wrong (probably username already exists)
        session.rollback()  # Undo the changes
        return jsonify({"error": "Username already exists or database error"}), 400
        
    finally:
        session.close()  # Always close the connection!


@app.route('/login', methods=['POST'])
def login():
    """
    Login page (combined from both versions)
    
    I combined:
    - Making login tokens (from Version A)
    - Checking database for user (from Version B)
    - Checking if password is correct with bcrypt (from Version A)
    """
    # Get the username and password they sent
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Make sure they gave me both
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    # Look up the user in my database
    session = Session()  # Connect to database
    try:
        # Find the user by username
        user = session.query(User).filter_by(username=username).first()
        
        # If user doesn't exist, they can't log in
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Check if the password is correct
        # bcrypt.checkpw compares what they typed to the scrambled password in database
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # Password is correct! Make them a login token
            token = jwt.encode({
                'username': username,
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
            }, app.config['SECRET_KEY'])
            
            # Send them the token so they can stay logged in
            return jsonify({
                "token": token, 
                "message": "Login successful",
                "user_id": user.id
            })
        else:
            # Password is wrong
            return jsonify({"error": "Invalid credentials"}), 401
            
    finally:
        session.close()  # Always close the connection!


# Run my app
if __name__ == '__main__':
    app.run(debug=True)

# Completed with the help of AI
