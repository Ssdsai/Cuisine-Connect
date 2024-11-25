from flask import Blueprint, request, jsonify
from flask_cors import CORS
from Db import get_db

# Define Blueprint
checkout_blueprint = Blueprint('checkout', __name__)
CORS(checkout_blueprint, origins=["http://localhost:3000"], supports_credentials=True)

# MongoDB connection
db = get_db()  # Get the database connection
orders_collection = db['Orders'] if db is not None else None  # Explicit None check

@checkout_blueprint.route('/checkout', methods=['POST', 'OPTIONS'])
def checkout():
    if request.method == 'OPTIONS':
        # Respond to preflight request
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 200

    if db is None or orders_collection is None:
        return jsonify({"status": "error", "message": "Database connection error"}), 500

    try:
        # Parse JSON from the request
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "Invalid JSON format"}), 400

        # Extract data from the request
        user_id = data.get("user_id")
        customer_name = data.get("customer_name")
        phone_number = data.get("phone_number")
        email = data.get("email")
        delivery_address = data.get("delivery_address")
        order_id = data.get("order_id")
        cart_items = data.get("cart_items", [])

        if not all([user_id, customer_name, phone_number, email, delivery_address, order_id, cart_items]):
            return jsonify({"status": "error", "message": "All fields are required"}), 400

        # Insert each cart item as a separate order document in MongoDB
        for cart_item in cart_items:
            order = {
                "collecting_order": True,
                "user_ID": user_id,
                "fooditem_name": cart_item.get("product_name"),
                "Name": customer_name,
                "phone_number": phone_number,
                "email": email,
                "quantity": cart_item.get("quantity"),
                "delivery_address": delivery_address,
                "order_id": order_id
            }
            orders_collection.insert_one(order)

        # Respond with success
        response = jsonify({"status": "success"})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 200

    except Exception as e:
        print(f"Error during checkout: {e}")
        response = jsonify({"status": "error", "message": str(e)})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 500