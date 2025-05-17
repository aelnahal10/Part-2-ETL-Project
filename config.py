# config.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_engine():
    connection_string = (
        f"mssql+pyodbc://{os.getenv('SQL_USER')}:{os.getenv('SQL_PASSWORD')}"
        f"@{os.getenv('SQL_SERVER')}:{os.getenv('SQL_PORT')}/{os.getenv('SQL_DB')}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )
    return create_engine(connection_string, fast_executemany=True)
