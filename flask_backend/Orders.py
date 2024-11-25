from flask import Blueprint, jsonify
from flask_cors import CORS
from Db import get_db

# Define Blueprint
orders_blueprint = Blueprint('orders', __name__)
CORS(orders_blueprint, origins=["http://localhost:3000"], supports_credentials=True)

# MongoDB connection
db = get_db()  # Get the database connection
orders_collection = db['Orders'] if db is not None else None  # Ensure the collection exists

@orders_blueprint.route('/orders', methods=['GET'])
def get_orders():
    if db is None or orders_collection is None:  # Explicit None check
        return jsonify({"status": "error", "message": "Database connection error"}), 500

    try:
        # Fetch all orders from the Orders collection
        orders = list(orders_collection.find())
        formatted_orders = []

        # Format the data for the response
        for order in orders:
            formatted_orders.append({
                "order_id": order.get("order_id"),
                "customer_name": order.get("Name"),
                "delivery_address": order.get("delivery_address"),
                "cart_items": [
                    {
                        "product_name": order.get("fooditem_name"),
                        "quantity": order.get("quantity")
                    }
                ]
            })

        return jsonify(formatted_orders), 200

    except Exception as e:
        print(f"Error fetching orders: {e}")
        return jsonify({"status": "error", "message": "An error occurred while fetching orders"}), 500