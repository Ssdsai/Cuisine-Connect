# from pymongo import MongoClient
# import re
#
# # Simulate handle_orders function here
# # MongoDB connection setup
# client = MongoClient('mongodb://localhost:27017/')  # Connect to your MongoDB server
# db = client['CuisineConnect']
# orders_collection = db['Orders']
#
# def handle_orders(query):
#     try:
#         print(f"Received query: {query}")
#         order_id_match = re.search(r'\bORD-\d+\b', query)
#         if not order_id_match:
#             print("Order ID not found in query.")
#             return {"response": "Order ID not found in the query."}
#
#         order_id = order_id_match.group(0)
#         print(f"Extracted Order ID: {order_id}")
#
#         order = orders_collection.find_one({"order_id": order_id})
#         if not order:
#             print(f"No order found for Order ID: {order_id}")
#             return {"response": "No order found with the provided order ID."}
#
#         # Process order details
#         order_details = {
#             "orderId": order.get("order_id"),
#             "userId": order.get("user_ID"),
#             "foodItem": order.get("fooditem_name"),
#             "name": order.get("Name"),
#             "quantity": order.get("quantity"),
#             "deliveryAddress": order.get("delivery_address"),
#             "status": "Order found"
#         }
#         print(f"Order details: {order_details}")
#         return {
#             "response": order_details
#         }
#     except Exception as e:
#         print(f"Error in handle_orders: {e}")
#         return {"response": "An error occurred while processing the order query."}
#
# # Test the function
# test_query = "order status of ORD-123456"
# result = handle_orders(test_query)
# print(result)