import os
from dotenv import load_dotenv
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain.agents import create_structured_chat_agent
from langchain_openai import ChatOpenAI
from langchain.tools.tavily_search import TavilySearchResults

print("Loading environment variables from .env file...")
load_dotenv()
print("Environment variables loaded.")

print("Getting the Tavily API key from the environment variable...")
tavily_api_key = os.getenv("TAVILY_API_KEY")
print(f"Tavily API key: {tavily_api_key}")

print("Initializing the Tavily search wrapper...")
search = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
print("Tavily search wrapper initialized.")

print("Setting up the Tavily search tool...")
tavily_tool = TavilySearchResults(api_wrapper=search)
print("Tavily search tool set up.")

print("Initializing the agent with the Tavily search tool and the OpenAI language model...")
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
agent = create_structured_chat_agent(
    llm=llm,
    tools=[tavily_tool],
)
print("Agent initialized.")

print("Defining a sample search query...")
query = "What happened in the latest burning man floods?"
print(f"Search query: {query}")

try:
    print("Running the agent with the sample query...")
    result = agent.invoke(query)
    print("Agent run completed.")
    print("Search results:")
    print(result)
except Exception as e:
    print("An error occurred.")
    print(f"Error details: {str(e)}")