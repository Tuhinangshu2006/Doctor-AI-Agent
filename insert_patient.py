import psycopg2
import sys

# ------------------------------------------------------------------
# CONFIGURATION
# Paste your full Neon.tech connection string inside the quotes below.
# ------------------------------------------------------------------
DB_URL = 'postgresql://neondb_owner:npg_KW2lhbdAto3x@ep-tiny-leaf-ae7hetx9-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

def add_patient(name, age, symptoms):
    """
    Inserts a new patient into the database using parameterized queries.
    """
    conn = None
    try:
        # Connect to the database
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # SQL Query with %s placeholders
        # We do NOT put quotes around %s, the library handles that for us.
        insert_query = """
        INSERT INTO patients (full_name, age, symptoms)
        VALUES (%s, %s, %s)
        """
        
        # Tuple of data to insert
        data_to_insert = (name, age, symptoms)

        # Execute the query
        # The library safely combines the query and the data here
        cur.execute(insert_query, data_to_insert)

        # Commit the transaction (save changes)
        conn.commit()
        
        print(f"✅ Successfully added patient: {name}")

        cur.close()

    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        # Rollback changes if an error occurs
        if conn:
            conn.rollback()
            
    except Exception as e:
        print(f"❌ General error: {e}")

    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    # Test the function with the requested data
    add_patient('Alice Smith', 28, 'Severe Headache')