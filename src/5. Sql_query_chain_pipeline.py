"""
SQL Query Chain Pipeline
========================

This script demonstrates SQL query chaining for medical data analysis.
"""

import os
from pyprojroot import here
import pandas as pd

from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

print("🔗 SQL Query Chain Pipeline")
print("=" * 35)

# -------------------------------
# 1. Database Setup
# -------------------------------
print("📊 Setting up database...")
db_path = os.path.join(str(here("/assignment17/src/databases")), "PatientsDB.db")
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

print("🔍 Database inspection:")
print(f"🔹 Database Path: {db_path}")
print(f"🔹 Usable Tables:", db.get_usable_table_names())

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

# -------------------------------
# 4. Chained Queries
# -------------------------------
print("\n🚀 Running chained queries...")

# Chain 1: Patient Statistics
print("\n📋 Chain 1: Patient Statistics")
chain1_queries = [
    "Count total patients in each disease category",
    "Based on the previous result, which disease has the highest patient count?",
    "For the disease with highest count, show age statistics"
]

for i, query in enumerate(chain1_queries, 1):
    print(f"\n🔗 Step {i}: {query}")
    try:
        result = sql_agent.invoke({"input": query})
        print(f"✅ Result: {result['output']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

# Chain 2: Demographic Analysis
print("\n📋 Chain 2: Demographic Analysis")
chain2_queries = [
    "Show gender distribution across all diseases",
    "Which gender has higher disease prevalence?",
    "For the gender with higher prevalence, show age groups"
]

for i, query in enumerate(chain2_queries, 1):
    print(f"\n🔗 Step {i}: {query}")
    try:
        result = sql_agent.invoke({"input": query})
        print(f"✅ Result: {result['output']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print("\n🎉 SQL Query Chain Pipeline complete!")
