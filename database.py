import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
DRIVER = os.getenv("DRIVER")

def get_connection():
    conn_str = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

def test_connection():
    try:
        conn = get_connection()
        print("✅ Connected to SmartLightsDW successfully!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_connection()