
"""
SQLite Database Inspector with LangChain + SQLAlchemy
-----------------------------------------------------
This script:
1. Connects to a SQLite database
2. Uses LangChain's SQLDatabase for simple queries
3. Uses SQLAlchemy Inspector to list tables, schemas, columns, PKs, and FKs
"""

from pyprojroot import here
import os
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, inspect



# -------------------------------
# Database Path Setup
# -------------------------------
# db_path = "F://assignment17//src//databases//PatientsDB.db"
# db_path = str(here("databases")) + "/PatientsDB.db"
db_path = os.path.join(str(here("/assignment17/src/databases")), "PatientsDB.db")
print(f"✅ Using database: {db_path}")

# -------------------------------
# LangChain: Quick Checks
# -------------------------------
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
print("\n🔹 Database Dialect:", db.dialect)
print("🔹 Usable Tables:", db.get_usable_table_names())

# Example: Run a query
try:
    result = db.run("SELECT * FROM heart_disease_patients LIMIT 10;")
    print("\n📊 Sample Data from heart_disease_patients table:")
    print(result)
except Exception as e:
    print("\n⚠️ Could not fetch from heart_disease_patients table:", e)

# -------------------------------
# SQLAlchemy Inspector
# -------------------------------
engine = create_engine(f"sqlite:///{db_path}")
connection = engine.connect()
inspector = inspect(engine)

# Get all tables
table_names = inspector.get_table_names()
print("\n📋 Tables in database:", table_names)

# Inspect each table
for table_name in table_names:
    print(f"\n🔎 Information for table: {table_name}")

    # Schema (SQLite often returns ['main'])
    schemas = inspector.get_schema_names()
    print("   Schemas:", schemas)

    # Columns
    columns = inspector.get_columns(table_name)
    for col in columns:
        print(f"   Column: {col['name']} | Type: {col['type']}")

    # Primary Key Constraint
    pk_constraint = inspector.get_pk_constraint(table_name)
    print("   Primary Key:", pk_constraint)

    # Foreign Keys
    foreign_keys = inspector.get_foreign_keys(table_name)
    print("   Foreign Keys:", foreign_keys)

# Close connection
connection.close()
print("\n✅ Inspection complete.")






import os
print(os.path.exists(db_path))   # should print True
print(db_path)  
