"""
Create SQL Agent for Medical Database
====================================

This script creates a specialized SQL agent for medical database queries.
"""

import os
from pyprojroot import here

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

print("🔧 Creating SQL Agent for Medical Database")
print("=" * 45)

# -------------------------------
# 1. Database Setup
# -------------------------------
print("📊 Setting up database connection...")
db_path = os.path.join(str(here("/assignment17/src/databases")), "PatientsDB.db")
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

print(f"🔹 Database Path: {db_path}")
print(f"🔹 Tables: {db.get_usable_table_names()}")

# -------------------------------
# 2. Setup LLM (GitHub Models)
# -------------------------------
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

print("✅ SQL Agent created successfully!")

# -------------------------------
# 4. Test the Agent
# -------------------------------
print("\n🚀 Testing the SQL agent...")

test_queries = [
    "Show me the schema of all tables",
    "Count patients in each disease category",
    "What is the age range of patients?",
    "Show gender distribution for each disease"
]

for i, query in enumerate(test_queries, 1):
    print(f"\n📋 Test Query {i}: {query}")
    try:
        result = sql_agent.invoke({"input": query})
        print(f"✅ Response: {result['output']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print("\n🎉 SQL Agent testing complete!")
