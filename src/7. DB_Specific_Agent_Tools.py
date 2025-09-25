"""
Database-Specific Agent Tools
=============================

This script creates database-specific tools for medical data analysis.
"""

import os
from pyprojroot import here

from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

print("🛠️  Database-Specific Agent Tools")
print("=" * 35)

# -------------------------------
# Database & LLM Setup
# -------------------------------
db_path = os.path.join(str(here("/assignment17/src/databases")), "PatientsDB.db")
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

token = os.getenv("GITHUB_API_TOKEN", "your_github_token_here")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4.1-mini"

llm = ChatOpenAI(
    model_name=model_name,
    openai_api_key=token,
    openai_api_base=endpoint,
    temperature=0.2,
)

print(f"🔹 Database: {db_path}")
print(f"🔹 Tables: {db.get_usable_table_names()}")
print(f"🤖 LLM: {model_name}")

# -------------------------------
# Database-Specific Tools
# -------------------------------

@tool
def get_table_info(table_name: str) -> str:
    """Get detailed information about a specific table."""
    try:
        schema = db.get_table_info([table_name])
        return f"Schema for {table_name}:\n{schema}"
    except Exception as e:
        return f"Error getting table info: {str(e)}"

@tool
def count_patients_by_disease(disease_type: str) -> str:
    """Count patients for a specific disease type."""
    try:
        result = db.run(f"SELECT COUNT(*) FROM {disease_type}_patients")
        return f"Total {disease_type} patients: {result}"
    except Exception as e:
        return f"Error counting patients: {str(e)}"

@tool
def get_age_statistics(disease_type: str) -> str:
    """Get age statistics for a specific disease type."""
    try:
        result = db.run(f"""
            SELECT 
                MIN(Age) as min_age,
                MAX(Age) as max_age,
                AVG(Age) as avg_age,
                COUNT(*) as total_patients
            FROM {disease_type}_patients
        """)
        return f"Age statistics for {disease_type}:\n{result}"
    except Exception as e:
        return f"Error getting age statistics: {str(e)}"

@tool
def get_gender_distribution(disease_type: str) -> str:
    """Get gender distribution for a specific disease type."""
    try:
        result = db.run(f"""
            SELECT Sex, COUNT(*) as count
            FROM {disease_type}_patients
            GROUP BY Sex
        """)
        return f"Gender distribution for {disease_type}:\n{result}"
    except Exception as e:
        return f"Error getting gender distribution: {str(e)}"

# -------------------------------
# Create Agent with Tools
# -------------------------------
print("\n🔧 Creating agent with database-specific tools...")

tools = [
    get_table_info,
    count_patients_by_disease,
    get_age_statistics,
    get_gender_distribution,
]

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
agent = create_react_agent(
    llm,
    tools=tools,
    checkpointer=memory,
)

print("✅ Agent with database-specific tools created!")

# -------------------------------
# Test the Tools
# -------------------------------
print("\n🚀 Testing database-specific tools...")

test_queries = [
    "Get table information for heart_disease_patients",
    "Count patients for heart_disease",
    "Get age statistics for cancer",
    "Show gender distribution for diabetes"
]

config = {"configurable": {"thread_id": "db_tools_test"}}

for i, query in enumerate(test_queries, 1):
    print(f"\n📋 Test {i}: {query}")
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": query}]}, config)
        print(f"✅ Response: {result['messages'][-1].content}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print("\n🎉 Database-specific agent tools testing complete!")
