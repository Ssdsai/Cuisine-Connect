from flask import Flask, request, jsonify
from pymongo import MongoClient
import re

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Connect to your MongoDB server
db = client['CuisineConnect']  # Use the 'Foodservices' database
orders_collection = db['Orders']  # Use the 'Orders' collection

def handle_orders(query):
    try:
        order_id_match = re.search(r'\bORD-\d+\b', query)

        if order_id_match:
            order_id = order_id_match.group(0)
            order = orders_collection.find_one({"order_id": order_id})

            if order:
                order_details = {
                    "orderId": order.get("order_id"),
                    "userId": order.get("user_ID"),
                    "foodItem": order.get("fooditem_name"),
                    "name": order.get("Name"),
                    "phoneNumber": order.get("phone_number"),
                    "email": order.get("email"),
                    "quantity": order.get("quantity"),
                    "deliveryAddress": order.get("delivery_address"),
                    "collectingOrder": order.get("collecting_order", False),
                    "status": order.get("status")
                }
                return {"response": order_details}
            else:
                return {"response": "No order found with the provided order ID."}
        else:
            return {"response": "Order ID not found in the query."}
    except Exception as e:
        print(f"Error in handle_orders: {e}")
        return {"response": "An error occurred while processing the order query."}
