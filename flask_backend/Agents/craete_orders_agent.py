from langchain.tools import tool
from langchain_openai import ChatOpenAI
import os
import random

# Initialize OpenAI model for natural language processing
llm = ChatOpenAI(
    temperature=0.7,
    model="GPT-4o mini",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Mock database for storing orders
orders_db = {
    "12345": {"status": "Shipped", "delivery_date": "2024-11-25"},
    "67890": {"status": "Processing", "delivery_date": "2024-11-28"},
}

# Mock food item data
food_item = {
    "foodId": "1",
    "name": "Spaghetti Carbonara",
    "description": "Classic Italian pasta with creamy egg sauce, pancetta, and Parmesan cheese.",
    "price": 12.99,
    "imageUrl": "/images/Spaghetti_Carbonara.jpg",
    "cuisine": "Italian",
    "spiceLevel": "Mild"
}

def generate_order_id():
    """Generate a random 6-digit order ID."""
    return str(random.randint(100000, 999999))

@tool("handle_order_status", return_direct=True)
def handle_order_status(query: str) -> str:
    """
    Handle customer queries about order status.
    """
    try:
        # Extract order ID from query
        order_id = query.split()[-1]  # Assume the order ID is the last word
        order = orders_db.get(order_id)
        if order:
        # if True:
            return f"Order ID 12345"
        else:
            return "Sorry, I couldn't find an order with that ID."
    except Exception as e:
        return f"Error retrieving order status: {e}"

# @tool("place_order", return_direct=True)
# def handle_place_order(query: str, additional_input: dict) -> str:
    """
    Handle customer requests to place a new order.
    """
    try:
        # Simulate storing order details in the database
        order_id = generate_order_id()
        orders_db[order_id] = {
            "userDetails": additional_input["userDetails"],
            "foodItem": additional_input["foodItem"],
            "quantity": additional_input["quantity"]
        }
        return f"Order placed successfully! Your Order ID is {order_id}."
    except Exception as e:
        return f"Error placing order: {e}"

# @tool("place_order", return_direct=True)
# def handle_place_order(query: str, additional_input: dict) -> str:
    """
    Handle customer requests to place a new order.
    """
    try:
        # Generate a unique order ID
        order_id = generate_order_id()

        # Store the order in the mock database
        orders_db[order_id] = {
            "userDetails": additional_input["userDetails"],
            "foodItem": additional_input["foodItem"],
            "quantity": additional_input["quantity"]
        }

        # Return a success message with the order ID
        return f"Order placed successfully! Your Order ID is {order_id}. Thank you for ordering!"
    except Exception as e:
        return f"Error placing order: {e}"
    
@tool("place_order", return_direct=True)
def handle_place_order(query: str, additional_input: dict) -> str:
    """
    Handle customer requests to place a new order.
    """
    try:
        # Generate a unique order ID
        order_id = generate_order_id()

        print("Query received:", query)
        print("Additional Input:", additional_input)


        # Store the order in the mock database
        orders_db[order_id] = {
            "userDetails": additional_input["userDetails"],
            "foodItem": additional_input["foodItem"],
            "quantity": additional_input["quantity"],
        }

        # Return a success message with the order ID
        return f"Order placed successfully! Your Order ID is {order_id}. Thank you for ordering!"
    except Exception as e:
        return f"Error placing order: {e}"

def handle_order_creation(query: str, additional_input=None) -> dict:
    """
    Determines whether the query is about order status or placing a new order.
    """
    if "status" or "track my order" in query.lower():
        return {"response": handle_order_status(query)}
    elif "place order" in query.lower():
        if additional_input:  # Check if additional input is provided
            return {"response": handle_place_order(query, additional_input)}
        else:
            # Confirm ordering and show product card with quantity controls
            return {
                "response": "Would you like to place an order for this item?",
                "foodItem": food_item,
            }
    else:
        return {"response": "I'm sorry, I couldn't understand your order-related query. Please provide more details."}


# def handle_orders(query: str, additional_input=None) -> dict:
    """
    Determines whether the query is about order status or placing a new order.
    """
    if "status" in query.lower():
        return {"response": handle_order_status(query)}
    elif "place order" in query.lower():
        if additional_input:
            return {"response": handle_place_order(query, additional_input)}
        else:
            # Confirm ordering and show product card with quantity controls
            return {
                "response": "Would you like to place an order for this item?",
                "foodItem": food_item,
            }
        
    else:
        return {"response": "I'm sorry, I couldn't understand your order-related query. Please provide more details."}