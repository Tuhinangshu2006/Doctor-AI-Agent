import psycopg2

# 1. The Single Source of Truth
# Paste your Real Neon String here ONE LAST TIME.
DB_URL = 'postgresql://neondb_owner:npg_KW2lhbdAto3x@ep-tiny-leaf-ae7hetx9-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

def get_connection():
    """Returns a connection to the database."""
    try:
        return psycopg2.connect(DB_URL)
    except Exception as e:
        print("❌ Connection Failed:", e)
        return None

# Test it only if we run this file directly
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("✅ Connection Successful!")
        conn.close()