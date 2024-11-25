from flask import Flask, request, jsonify
from flask_cors import CORS
from Login import auth_blueprint
from Checkout import checkout_blueprint
from Orders import orders_blueprint
from Agents.decision_agent import decide_agent
from Agents.fraud_detection_agent import handle_fraud_detection


# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# Register blueprints for modular routes
app.register_blueprint(auth_blueprint, url_prefix='/api')
app.register_blueprint(checkout_blueprint, url_prefix='/api')
app.register_blueprint(orders_blueprint, url_prefix='/api')

@app.route('/api/query', methods=['POST'])
def query_route():
    try:
        if request.content_type.startswith('multipart/form-data'):
            # Handle form-data requests (e.g., fraud detection with image uploads)
            query = request.form.get("query", "").strip()
            description = request.form.get("description", "").strip()
            order_id = request.form.get("order_id", "").strip()
            image_file = request.files.get("image")

            if not query:
                return jsonify({"error": "Query cannot be empty"}), 400

            # Check for fraud-related keywords
            fraud_keywords = ["fraud", "issue", "problem", "damage", "broken"]
            if any(keyword in query.lower() for keyword in fraud_keywords):
                if not description or not order_id or not image_file:
                    return jsonify({
                        "response": "Please provide additional details (description, order ID, and attach an image) to proceed with your request."
                    }), 200

                # Handle fraud detection
                fraud_response = handle_fraud_detection(description, image_file, order_id)
                if "error" in fraud_response:
                    return jsonify(fraud_response), 400
                return jsonify(fraud_response), 200

            # If no fraud keyword, return invalid request for multipart form-data
            return jsonify({"error": "Invalid form-data query."}), 400

        elif request.content_type == 'application/json':
            # Handle JSON requests (e.g., order status or general queries)
            data = request.get_json()
            query = data.get("query", "").strip()
            chat_history = data.get("chat_history", [])

            if not query:
                return jsonify({"response": "Query cannot be empty"}), 400

            # Directly handle fraud-related keywords in JSON requests
            fraud_keywords = ["fraud", "issue", "problem", "damage", "broken"]
            if any(keyword in query.lower() for keyword in fraud_keywords):
                return jsonify({
                    "response": "Please provide additional details (description, order ID, and attach an image) to proceed with your request."
                }), 200

            # Use decision agent for query handling (includes order status logic)
            agent_response = decide_agent(query, chat_history)

            if isinstance(agent_response, dict) and "response" in agent_response:
                return jsonify(agent_response), 200
            elif isinstance(agent_response, dict):
                return jsonify({"response": "Unexpected response format"}), 500
            else:
                return jsonify({"response": agent_response}), 200

        else:
            return jsonify({"error": "Unsupported Media Type"}), 415

    except Exception as e:
        print(f"Error in /api/query: {e}")
        return jsonify({"response": "Internal server error"}), 500

# @app.route('/api/query', methods=['POST'])
# def query_route():
#     try:
#         if request.content_type.startswith('multipart/form-data'):
#             # Extract form-data inputs
#             query = request.form.get("query", "").strip()
#             description = request.form.get("description", "").strip()
#             order_id = request.form.get("order_id", "").strip()
#             image_file = request.files.get("image")
#
#             if not query:
#                 return jsonify({"error": "Query cannot be empty"}), 400
#
#             # Check for fraud-related keywords
#             fraud_keywords = ["fraud", "issue", "problem", "damage", "broken"]
#             if any(keyword in query.lower() for keyword in fraud_keywords):
#                 if not description or not order_id or not image_file:
#                     # Prompt for additional details
#                     return jsonify({
#                         "response": "Please provide additional details (description, order ID, and attach an image) to proceed with your request."
#                     }), 200
#
#                 # Handle fraud detection
#                 fraud_response = handle_fraud_detection(description, image_file, order_id)
#                 if "error" in fraud_response:
#                     return jsonify(fraud_response), 400
#                 return jsonify(fraud_response), 200
#
#         elif request.content_type == 'application/json':
#             # Extract JSON inputs
#             data = request.get_json()
#             query = data.get("query", "").strip()
#             chat_history = data.get("chat_history", [])
#
#             if not query:
#                 return jsonify({"response": "Query cannot be empty"}), 400
#
#             # Check for fraud-related keywords
#             fraud_keywords = ["fraud", "issue", "problem", "damage", "broken"]
#             if any(keyword in query.lower() for keyword in fraud_keywords):
#                 # Prompt for additional details
#                 return jsonify({
#                     "response": "Please provide additional details (description, order ID, and attach an image) to proceed with your request."
#                 }), 200
#
#             # Handle general queries
#             agent_response = decide_agent(query, chat_history)
#             if isinstance(agent_response, dict):
#                 return jsonify({"response": "Unexpected response format"}), 500
#             return jsonify({"response": agent_response}), 200
#
#         else:
#             return jsonify({"error": "Unsupported Media Type"}), 415
#
#     except Exception as e:
#         print(f"Error in /api/query: {e}")
#         return jsonify({"response": "Internal server error"}), 500

@app.route('/api/fraud-detection', methods=['POST'])
def fraud_detection_route():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image_file = request.files['image']
        description = request.form.get("description", "").strip()
        order_id = request.form.get("order_id", "").strip()

        if not description or not order_id:
            return jsonify({"error": "Description and order ID are required"}), 400

        # Debugging logs
        print(f"Image file received: {image_file.filename}")
        print(f"Description: {description}, Order ID: {order_id}")

        # Call fraud detection handler
        response = handle_fraud_detection(description, image_file, order_id)
        print(f"Response from handle_fraud_detection: {response}")

        return jsonify(response), 200

    except Exception as e:
        print(f"Error in /api/fraud-detection: {e}")
        return jsonify({"error": "Internal server error"}), 500


# Main entry point
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting the Flask app: {e}")