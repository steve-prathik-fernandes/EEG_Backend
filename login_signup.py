from pymongo import MongoClient
import bcrypt

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client["eeg_database"]  # Use your database name here
users_collection = db["users"]  # Collection name

# Helper function to hash passwords
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed

# Helper function to verify passwords
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode("utf-8"), stored_password)

# Function to register a new user
def register_user(username, password):
    if not username or not password:
        return {"error": "Username and password are required"}, 400

    # Check if the user already exists
    if users_collection.find_one({"username": username}):
        return {"error": "Username already exists"}, 400

    # Hash the password
    hashed_password = hash_password(password)

    # Insert the user into the database
    user_id = users_collection.insert_one({
        "username": username,
        "password": hashed_password
    }).inserted_id

    return {"message": "User registered successfully", "user_id": str(user_id)}, 201

# Function to login a user
def login_user(username, password):
    if not username or not password:
        return {"error": "Username and password are required"}, 400

    # Find the user in the database
    user = users_collection.find_one({"username": username})
    if not user:
        return {"error": "Invalid username or password"}, 401

    # Verify the password
    if not verify_password(user["password"], password):
        return {"error": "Invalid username or password"}, 401

    return {"message": "Login successful", "user_id": str(user["_id"])}, 200