import uuid

from werkzeug.datastructures import FileStorage

from .food_recommendation_agent import get_food_recommendations
from .query_agent import handle_food_query
from .fraud_detection_agent import handle_fraud_detection
from .fetch_orders import handle_orders
from .craete_orders_agent import handle_order_creation
import os

# Initialize OpenAI model for dynamic responses
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def save_image(image_file):
    """Saves the uploaded image to the uploads directory."""
    uploads_dir = os.path.join(os.getcwd(), "uploads")
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    image_filename = f"{uuid.uuid4()}-{image_file.filename}"
    image_path = os.path.join(uploads_dir, image_filename)
    image_file.save(image_path)
    return image_path

def generate_dynamic_response(query: str) -> dict:
    """
    Generates a fallback response using GPT-4 for unrecognized queries.
    :param query: The user's unrecognized query.
    :return: A dictionary containing the dynamically generated response.
    """
    try:
        system_prompt = (
            "You are a helpful and friendly assistant specialized in food and cuisines. "
            "You can answer questions about food recommendations, allergens, ingredients, cooking methods, and health benefits. "
            "If someone asks 'What can you do?', explain your capabilities conversationally."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        response = llm.invoke(messages)
        content = response.content.strip() if hasattr(response, "content") else response["content"]
        return {"response": content}
    except Exception as e:
        print(f"Error generating dynamic response: {e}")
        return {"response": "I'm sorry, I couldn't generate a response. Please try again later."}

def decide_agent(query: str, additional_input=None):
    """
    Decides which agent to invoke based on the query content.
    :param query: The user's query.
    :param additional_input: Optional additional data (e.g., images, descriptions).
    :return: Response from the selected agent.
    """
    query_lower = query.lower().strip()

    # Handle greetings
    greeting_keywords = ["hi", "hello", "how are you", "hey"]
    if any(keyword in query_lower for keyword in greeting_keywords):
        return "Hi, Welcome to Cuisine Connect! How may I assist you today?"

    # Handle food recommendations
    recommendation_keywords = ["recommend", "show", "list", "suggest", "give"]
    if any(keyword in query_lower for keyword in recommendation_keywords):
        return get_food_recommendations(query)

    # Handle general food-related queries
    query_keywords = ["allergen", "ingredients", "calories", "health", "explain", "details", "information"]
    if any(keyword in query_lower for keyword in query_keywords):
        return handle_food_query(query)

    # Handle fraud or product issue queries
    fraud_keywords = ["fraud", "issue", "problem", "defective", "damaged", "broken"]
    if any(keyword in query_lower for keyword in fraud_keywords):
        if additional_input:
            # Check for missing inputs
            missing_keys = [key for key in ["image", "description", "order_id"] if key not in additional_input]
            if missing_keys:
                return {"error": f"Missing required inputs: {', '.join(missing_keys)}"}

            # Validate inputs (optional, add validation logic as needed)
            if not additional_input["description"].strip():
                return {"error": "Description cannot be empty."}
            if not isinstance(additional_input["image"], FileStorage):  # Flask's FileStorage for uploaded files
                return {"error": "Invalid image file."}
            if not additional_input["order_id"].strip():
                return {"error": "Order ID cannot be empty."}

            # Call fraud detection
            return handle_fraud_detection(
                description=additional_input["description"],
                image_file=additional_input["image"],
                order_id=additional_input["order_id"]
            )
        else:
            return {"error": "Additional input (image, description, order_id) required for fraud detection."}

    order_status_keywords = ["order status", "shipping status", "defective", "spoiled","damaged", "refund", "replace"]
    if any(keyword in query_lower for keyword in order_status_keywords):
        return handle_orders(query)

    print(f"Query: {query_lower}")
    order_creation_keywords = ["place order"]
    if any(keyword in query_lower for keyword in order_creation_keywords):
        print("Handling order creation")
        return handle_order_creation(query, additional_input)

    # Dynamic fallback for unrecognized queries
    return generate_dynamic_response(query)