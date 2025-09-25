"""
LangGraph Medical Agent
======================

This script demonstrates the creation of a medical agent using LangGraph
with database and web search capabilities.
"""

import os
from pyprojroot import here
import pandas as pd

from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch

print("🏥 Initializing Medical Agent with LangGraph")
print("=" * 50)

# -------------------------------
# 1. Database Setup
# -------------------------------
print("📊 Setting up database connection...")
db_path = os.path.join(str(here("/assignment17/src/databases")), "PatientsDB.db")
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

print("🔍 Database inspection:")
print(f"🔹 Database Path: {db_path}")
print(f"🔹 Tables: {db.get_usable_table_names()}")

# -------------------------------
# 2. Setup LLM (GitHub Models)
# -------------------------------
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "your_tavily_api_key_here")
token = os.getenv("GITHUB_API_TOKEN", "your_github_token_here")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4.1-mini"

if not token:
    raise ValueError("❌ GITHUB_TOKEN environment variable not set.")

llm = ChatOpenAI(
    model_name=model_name,
    openai_api_key=token,
    openai_api_base=endpoint,
    temperature=0.2,
)

print(f"🤖 LLM initialized: {model_name}")

# -------------------------------
# 3. Create SQL Agent
# -------------------------------
print("🔧 Creating SQL agent...")
sql_agent = create_sql_agent(
    llm,
    db=db,
    agent_type="openai-tools",
    verbose=True,
)

# -------------------------------
# 4. Web Search Tool
# -------------------------------
print("🌐 Setting up web search tool...")
web_search = TavilySearch(
    max_results=3,
    topic="general",
)
web_search.name = "web_search"
web_search.description = "Search the web for medical information"

# -------------------------------
# 5. Utility Tools
# -------------------------------
@tool
def get_patient_count(table_name: str) -> int:
    """Get the total number of patients in a specific table."""
    result = db.run(f"SELECT COUNT(*) FROM {table_name}")
    return int(result)

@tool
def get_age_statistics(table_name: str) -> dict:
    """Get age statistics for patients in a specific table."""
    result = db.run(f"""
        SELECT 
            MIN(Age) as min_age,
            MAX(Age) as max_age,
            AVG(Age) as avg_age,
            COUNT(*) as total_patients
        FROM {table_name}
    """)
    return result

# -------------------------------
# 6. Create LangGraph Agent
# -------------------------------
print("🧠 Creating LangGraph agent...")
memory = MemorySaver()

tools = [
    get_patient_count,
    get_age_statistics,
    web_search,
]

agent = create_react_agent(
    llm,
    tools=tools,
    checkpointer=memory,
)

print("✅ Medical Agent created successfully!")

# -------------------------------
# 7. Example Usage
# -------------------------------
print("\n🚀 Running example queries...")
config = {"configurable": {"thread_id": "medical_session"}}

# Example 1: Database query
print("\n📊 Example 1: Database Statistics")
query1 = "How many heart disease patients do we have and what are their age statistics?"
result1 = agent.invoke({"messages": [{"role": "user", "content": query1}]}, config)
print(f"Response: {result1['messages'][-1].content}")

# Example 2: Web search
print("\n🌐 Example 2: Web Search")
query2 = "What are the latest treatments for diabetes?"
result2 = agent.invoke({"messages": [{"role": "user", "content": query2}]}, config)
print(f"Response: {result2['messages'][-1].content}")

print("\n🎉 Medical Agent demonstration complete!")
