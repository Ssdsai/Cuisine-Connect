from flask import Blueprint, request, jsonify
from decision_agent import decide_agent

agent_routes = Blueprint('agent_routes', __name__)

@agent_routes.route('/api/query', methods=['POST'])
def process_query():
    """
    Handles queries and routes them to the appropriate agent.
    """
    try:
        data = request.get_json()
        query = data.get("query", "")
        additional_input = data.get("additional_input", None)
        if not query:
            return jsonify({"error": "Query field is required"}), 400

        response = decide_agent(query, additional_input)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500