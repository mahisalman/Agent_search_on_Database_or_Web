import os
import re
import pandas as pd
from sqlalchemy import create_engine, inspect


class PrepareSQLFromTabularData:
    """
    A class that prepares a SQLite database from CSV or XLSX files in a given directory.
    Each file is read into a DataFrame and stored as a SQL table inside combineddata.db.
    """

    def __init__(self, files_dir: str, db_name: str = "PatientsDB.db") -> None:
        """
        Initialize an instance of PrepareSQLFromTabularData.

        Args:
            files_dir (str): Directory containing the CSV/XLSX files.
            db_name (str): SQLite database file name.
        """
        self.files_directory = files_dir
        self.file_dir_list = [
            f for f in os.listdir(files_dir) if f.endswith((".csv", ".xlsx"))
        ]

        # Ensure DB folder exists
        os.makedirs("databases", exist_ok=True)
        db_path = os.path.join("databases", db_name)

        # Create SQLite connection string
        self.engine = create_engine(f"sqlite:///{db_path}")
        print(f"✅ Using database: {db_path}")
        print("📂 Number of files detected:", len(self.file_dir_list))

    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean DataFrame column names to be SQL-friendly.
        - lowercase
        - replace spaces & special chars with underscores
        - strip leading/trailing underscores
        """
        clean_cols = []
        for col in df.columns:
            col_clean = col.strip().lower()
            col_clean = re.sub(r"[^0-9a-zA-Z]+", "_", col_clean)
            col_clean = col_clean.strip("_")
            clean_cols.append(col_clean)
        df.columns = clean_cols
        return df

    def _prepare_db(self):
        """
        Convert CSV/XLSX files into SQL tables.
        Table name = file name (without extension).
        """
        for file in self.file_dir_list:
            full_file_path = os.path.join(self.files_directory, file)
            file_name, file_extension = os.path.splitext(file)
            table_name = file_name.lower().replace(" ", "_")

            # Read file
            if file_extension.lower() == ".csv":
                df = pd.read_csv(full_file_path)
            elif file_extension.lower() == ".xlsx":
                df = pd.read_excel(full_file_path)
            else:
                print(f"⚠️ Skipping unsupported file: {file}")
                continue

            # Clean column names
            df = self._clean_column_names(df)

            # Save DataFrame to SQL
            df.to_sql(table_name, self.engine, if_exists="replace", index=False)
            print(f"📌 Saved table: {table_name} ({len(df)} rows)")

        print("==============================")
        print("✅ All files saved into the SQL database.")

    def _validate_db(self):
        """
        Validate the database by listing all tables.
        """
        insp = inspect(self.engine)
        table_names = insp.get_table_names()
        print("==============================")
        print("📊 Available tables in database:", table_names)
        print("==============================")

    def run_pipeline(self):
        """
        Run the pipeline: import → validate.
        """
        self._prepare_db()
        self._validate_db()


if __name__ == "__main__":
    # 👇 Update this path to where your CSV files are stored
    files_directory = r"F:\Assignment17\data\csv_xlsx"

    pipeline = PrepareSQLFromTabularData(files_directory)
    pipeline.run_pipeline()
