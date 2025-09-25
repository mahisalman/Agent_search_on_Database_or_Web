"""
Main Pipeline for Medical Agent
==============================

This script demonstrates the main pipeline for medical data analysis
using LangChain and SQL agents.
"""

import os
from pyprojroot import here
import pandas as pd

from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

print("🏥 Medical Agent Main Pipeline")
print("=" * 40)

# -------------------------------
# 1. Database Setup
# -------------------------------
print("📊 Setting up database...")
db_path = os.path.join(str(here("/assignment17/src/databases")), "PatientsDB.db")
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

print("🔍 Database inspection:")
print(f"🔹 Database Path: {db_path}")
print(f"🔹 Tables: {db.get_usable_table_names()}")

# Inspect table schemas
for table in db.get_usable_table_names():
    print(f"🔹 {table} schema:")
    schema = db.get_table_info([table])
    print(schema[:200] + "..." if len(schema) > 200 else schema)

print("\n✅ Database inspection complete.")

# -------------------------------
# 3. Environment Variables Setup
# -------------------------------
token = os.getenv("GITHUB_API_TOKEN", "your_github_token_here")
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4.1-mini" 

if not token:
    raise ValueError("❌ GITHUB_TOKEN environment variable not set. Please provide a valid token.")

llm = ChatOpenAI(
    model_name=model_name,
    openai_api_key=token,
    openai_api_base=endpoint,
    temperature=0.2,
)

print(f"🤖 LLM initialized: {model_name}")

# -------------------------------
# 4. Create SQL Agent
# -------------------------------
print("🔧 Creating SQL agent...")
sql_agent = create_sql_agent(
    llm,
    db=db,
    agent_type="openai-tools",
    verbose=True,
)

# -------------------------------
# 5. Example Queries
# -------------------------------
print("\n🚀 Running example queries...")

queries = [
    "How many patients are in each table?",
    "What is the age distribution of heart disease patients?",
    "Show me the average age by disease type",
    "Which disease has the most patients?",
    "What are the gender statistics for cancer patients?"
]

for i, query in enumerate(queries, 1):
    print(f"\n📋 Query {i}: {query}")
    try:
        result = sql_agent.invoke({"input": query})
        print(f"✅ Result: {result['output']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print("\n🎉 Main pipeline execution complete!")
