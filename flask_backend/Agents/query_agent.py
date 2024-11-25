from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not found in environment variables"

# Define a fallback for broad or general food queries
def general_food_query_tool(query: str) -> str:
    """
    Handles broad or general food-related queries using OpenAI GPT.
    :param query: The user's question.
    :return: A comprehensive response based on general knowledge.
    """
    # Example general responses
    if "america" in query.lower():
        return "In America, you can enjoy iconic foods like hamburgers, hot dogs, apple pie, barbecue ribs, pancakes, and clam chowder. Don't miss the regional specialties like deep-dish pizza in Chicago or lobster rolls in New England!"
    return "That's an interesting question! Could you please provide more details or specify your query?"

# Wrap the tool in a LangChain Tool object
general_food_query = Tool(
    name="general_food_query",
    func=general_food_query_tool,
    description="Handles broad or general food-related questions.",
)

# List of tools
tools = [general_food_query]

# Define the custom prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in answering general food-related queries."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Load the LLM
llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-4o",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Bind tools to the LLM
llm_with_tools = llm.bind_tools(tools)

# Assemble the agent
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

# Function to handle broad or general food-related queries
def handle_food_query(user_query: str):
    """
    Invokes the general query agent with the provided query.
    :param user_query: The user's query string.
    :return: The agent's response as a dictionary.
    """
    return agent_executor.invoke({"input": user_query})