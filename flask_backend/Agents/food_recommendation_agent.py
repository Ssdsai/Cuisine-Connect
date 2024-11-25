from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from dotenv import load_dotenv
from pymongo import MongoClient
import os

# Load environment variables
load_dotenv()
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not found in environment variables"

# MongoDB connection
try:
    from flask_backend.Db import get_db

    db = get_db()
    if db is not None:
        fooditems_collection = db["Fooditems"]
    else:
        raise ConnectionError("Failed to connect to the MongoDB database using get_db().")
except ImportError:
    # Fallback to direct connection using MONGO_URI
    assert os.getenv("MONGO_URI"), "MONGO_URI not found in environment variables"
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client["CuisineConnect"]
    fooditems_collection = db["Fooditems"]

# List of known cuisines in your MongoDB (you can extend this list as needed)
KNOWN_CUISINES = ["indian", "italian", "chinese", "mexican", "thai", "japanese", "american"]


def get_closest_cuisine(extracted_cuisine: str) -> str:
    """
    Fallback function to correct or map the extracted cuisine to a known cuisine.
    :param extracted_cuisine: The cuisine detected by OpenAI (can be misspelled or incorrect).
    :return: The closest valid cuisine name.
    """
    # Normalize and lowercase the cuisine to handle case sensitivity
    extracted_cuisine = extracted_cuisine.lower()

    # If the cuisine detected is not known, attempt a fuzzy match or correction
    if extracted_cuisine in KNOWN_CUISINES:
        return extracted_cuisine
    else:
        # Here, a more complex fuzzy matching could be used, like Levenshtein distance.
        # For now, just check if the cuisine is close to a known one based on substring matching
        for cuisine in KNOWN_CUISINES:
            if extracted_cuisine in cuisine:  # simple substring match
                return cuisine
        # If no match, return a default or "unknown" cuisine
        return "unknown"


# Step 1: Analyze the user input using OpenAI
def analyze_user_input(user_query: str) -> str:
    """
    Analyzes the user's query using OpenAI to extract the cuisine.
    :param user_query: The user's input query.
    :return: Extracted cuisine type or relevant keyword.
    """
    try:
        llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-4o-mini",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # Prompt to extract cuisine information
        prompt = f"""
        You are an assistant that extracts cuisine types or keywords from user queries about food. 
        Analyze the query below and respond with only the cuisine type or food category if present.
        If the cuisine is misspelled, please correct it based on common cuisines.

        User Query: "{user_query}"
        """

        response = llm.invoke([{"role": "user", "content": prompt}])
        extracted_cuisine = response.content.strip().lower()  # Normalize for consistent usage
        print(f"DEBUG: Extracted Cuisine: {extracted_cuisine}")

        # Correct the extracted cuisine based on the known cuisines
        corrected_cuisine = get_closest_cuisine(extracted_cuisine)
        return corrected_cuisine
    except Exception as e:
        return f"Error analyzing input: {e}"


# Step 2: Fetch all food items from MongoDB
def get_all_food_items() -> list:
    """
    Fetches all food items from MongoDB.
    :return: A list of food items or an empty list if no items are found or an error occurs.
    """
    try:
        # Fetch all food items, excluding MongoDB's '_id' field
        food_items = list(fooditems_collection.find({}, {"_id": 0}))
        if not food_items:
            print("DEBUG: No food items found in the database.")  # Log the case
            return []  # Return an empty list if no items are found
        return food_items
    except Exception as e:
        print(f"Error fetching food items: {e}")
        return []  # Return an empty list in case of an error


# Tool to fetch food items from the database based on cuisine
def fetch_food_recommendations_from_db(cuisine: str) -> list:
    """
    Fetch food recommendations based on the cuisine from MongoDB.
    :param cuisine: The cuisine to search for.
    :return: A list of recommended dishes with details (name, description, price, imageUrl, and spiceLevel).
    """
    cuisine = cuisine.lower()
    try:
        # Query MongoDB for food items matching the cuisine
        food_items = fooditems_collection.find({"cuisine": {"$regex": cuisine, "$options": "i"}})

        # Convert the cursor to a list and include relevant fields
        food_items_list = [
            {
                "name": item["name"],
                "description": item["description"],
                "price": item["price"],
                "imageUrl": item.get("imageUrl", ""),  # Handle cases where imageUrl might be missing
                "spiceLevel": item.get("spiceLevel", "Unknown")  # Default to "Unknown" if spiceLevel is missing
            }
            for item in food_items
        ]
        print(f"DEBUG: Query Results for {cuisine}: {food_items_list}")

        # Format recommendations with all details
        recommendations = [
            f"{item['name']} - {item['description']} (Price: ${item['price']:.2f}, Spice Level: {item['spiceLevel']})\nImage URL: {item['imageUrl']}"
            for item in food_items_list
        ]
        return recommendations if recommendations else [{"error": f"No recommendations found for {cuisine.capitalize()} cuisine."}]
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return [{"error": "Error fetching recommendations from the database."}]




# def fetch_food_recommendations_from_db(cuisine: str) -> str:
#     cuisine = cuisine.lower()
#     try:
#         food_items = fooditems_collection.find({"cuisine": {"$regex": cuisine, "$options": "i"}})
#
#         # Convert the cursor to a list for debugging
#         food_items_list = list(food_items)
#         print(f"DEBUG: Query Results for {cuisine}: {food_items_list}")
#
#         recommendations = [
#             f"{item['name']} - {item['description']} (Price: ${item['price']:.2f})"
#             for item in food_items_list
#         ]
#         if recommendations:
#             return (
#                     f"Recommended dishes for {cuisine.capitalize()} cuisine:\n" +
#                     "\n".join(recommendations)
#             )
#         else:
#             return f"No recommendations found for {cuisine.capitalize()} cuisine."
#     except Exception as e:
#         return f"Error fetching recommendations: {e}"


# Step 3: Generate recommendation based on query and data
def generate_recommendation(user_query: str) -> str:
    """
    Generates recommendations dynamically based on the user query.
    :param user_query: The user's input query.
    :return: A formatted string of recommendations.
    """
    try:
        # Extract the cuisine using analyze_user_input
        cuisine = analyze_user_input(user_query)
        if "error" in cuisine.lower():
            return cuisine  # Return error from analyze_user_input directly

        print(f"DEBUG: Detected cuisine from query: {cuisine}")

        # Fetch recommendations for the detected cuisine
        recommendations = fetch_food_recommendations_from_db(cuisine)
        return recommendations
    except Exception as e:
        return f"Error generating recommendations: {e}"


# Define the tool
recommend_food = Tool(
    name="recommend_food",
    func=fetch_food_recommendations_from_db,
    description="Recommends dishes based on the specified cuisine using data from MongoDB."
)

tools = [recommend_food]

# Define the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a food recommendation expert. Use the recommend_food tool to fetch recommendations based on user queries."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Initialize the OpenAI language model
llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

# Define the agent
agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
)

# Create the AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# Function to handle recommendations as an agent
def get_food_recommendations(user_query: str):
    """
    Handles user queries for food recommendations.
    :param user_query: The user's query.
    :return: A response generated by the agent.
    """
    try:
        print("Analyzing user input...")
        recommendations = generate_recommendation(user_query)
        return recommendations
    except Exception as e:
        return f"Error handling recommendation request: {e}"