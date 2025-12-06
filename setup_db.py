import psycopg2

# PASTE YOUR REAL NEON CONNECTION STRING HERE
DB_URL = 'postgresql://neondb_owner:npg_KW2lhbdAto3x@ep-tiny-leaf-ae7hetx9-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

def create_table():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # SQL Command to build the table
        # Notice we use 'full_name' not 'name'
        create_query = """
        CREATE TABLE IF NOT EXISTS patients (
            id SERIAL PRIMARY KEY,
            full_name TEXT NOT NULL,
            age INTEGER,
            symptoms TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cur.execute(create_query)
        conn.commit()  # <--- CRITICAL: This saves the table
        print("✅ Table 'patients' created successfully!")
        
    except Exception as e:
        print("❌ Error:", e)
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    create_table()