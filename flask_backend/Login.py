from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

# Define Blueprint
auth_blueprint = Blueprint('auth', __name__)
CORS(auth_blueprint, origins=["http://localhost:3000"], supports_credentials=True)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['CuisineConnect']
users_collection = db['Logincredentials']

@auth_blueprint.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        # Handle preflight requests for CORS
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200

    # Log the incoming request
    print("Login endpoint hit")
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password are required"}), 400

    # Debug incoming credentials
    print(f"Received Email: {email}")
    print(f"Received Password: {password}")  # In production, don't log passwords

    try:
        # Directly match email and password in the database
        user = users_collection.find_one({"email": email, "password": password})
        print(f"Database query result: {user}")

        if user:
            print("User authenticated")
            return jsonify({"status": "success", "message": "Login successful!", "user_id": str(user['_id'])}), 200
        else:
            print("Authentication failed")
            return jsonify({"status": "error", "message": "Invalid email or password"}), 401
    except Exception as e:
        print(f"Error querying the database: {e}")
        return jsonify({"status": "error", "message": "An error occurred while processing the login"}), 500

@auth_blueprint.route('/create-account', methods=['POST', 'OPTIONS'])
def create_account():
    if request.method == 'OPTIONS':
        # Handle preflight requests for CORS
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200

    # Handle POST request
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    try:
        # Check if the email already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return jsonify({"status": "error", "message": "Email already registered"}), 400

        # Insert new user into database without hashing password
        new_user = {
            "name": name,
            "email": email,
            "password": password  # Store the password as-is
        }
        result = users_collection.insert_one(new_user)
        print(f"New user created with ID: {result.inserted_id}")

        return jsonify({
            "status": "success",
            "message": "Account created successfully!",
            "user_id": str(result.inserted_id)
        }), 201
    except Exception as e:
        print("Error during account creation:", e)
        return jsonify({"status": "error", "message": "An error occurred while creating the account"}), 500