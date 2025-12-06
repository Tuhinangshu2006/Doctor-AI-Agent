import os
import psycopg2
from dotenv import load_dotenv

# Load secrets from the .env file
load_dotenv()

# Get the URL securely
DB_URL = os.getenv("DB_URL")

def get_connection():
    """Returns a connection to the database."""
    try:
        if not DB_URL:
            print("❌ Error: DB_URL not found in .env file")
            return None
        return psycopg2.connect(DB_URL)
    except Exception as e:
        print("❌ Connection Failed:", e)
        return None

if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("✅ Connection Successful!")
        conn.close()