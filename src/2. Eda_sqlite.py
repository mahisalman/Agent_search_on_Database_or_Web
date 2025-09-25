
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, inspect

class SQLiteEDA:
    """
    Perform Exploratory Data Analysis (EDA) on an existing SQLite database.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.conn = sqlite3.connect(db_path)
        self.inspector = inspect(self.engine)
        print(f"✅ Connected to database: {db_path}")

    def list_tables(self):
        """
        List all tables in the database.
        """
        tables = self.inspector.get_table_names()
        print("\n📊 Tables in database:")
        for t in tables:
            print(f" - {t}")
        return tables

    def table_info(self, table_name: str):
        """
        Show schema info (columns + types) and row count for a table.
        """
        print(f"\n📌 Table: {table_name}")
        # Columns
        columns = self.inspector.get_columns(table_name)
        print("   Columns:")
        for col in columns:
            print(f"     - {col['name']} ({col['type']})")

        # Row count
        count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table_name}", self.conn)
        print(f"   Total rows: {count['count'][0]}")

    def sample_data(self, table_name: str, n: int = 5):
        """
        Show first n rows from the table.
        """
        print(f"\n🔍 Sample rows from {table_name}:")
        df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT {n}", self.conn)
        print(df)

    def basic_statistics(self, table_name: str):
        """
        Generate basic descriptive statistics for numeric columns.
        """
        print(f"\n📈 Basic stats for {table_name}:")
        df = pd.read_sql(f"SELECT * FROM {table_name}", self.conn)
        print(df.describe(include="all"))

    def run_eda(self):
        """
        Run full EDA on all tables in the DB.
        """
        tables = self.list_tables()
        for t in tables:
            self.table_info(t)
            self.sample_data(t, n=5)
            self.basic_statistics(t)
            print("=" * 60)


if __name__ == "__main__":
    # 👇 Path to your combined database
    db_path = r"databases/PatientsDB.db"

    eda = SQLiteEDA(db_path)
    eda.run_eda()

