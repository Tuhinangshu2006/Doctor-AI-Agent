import requests
import random
import sys
# THE ENGINEERING UPGRADE: Import the connection tool, don't hardcode passwords
from db_connect import get_connection

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
API_URL = 'https://randomuser.me/api/'
SYMPTOMS_LIST = ['Fever', 'Cough', 'Headache', 'Fatigue']

def ingest_data():
    conn = None
    try:
        print("🌍 Fetching data from RandomUser API...")
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        users = data['results']
        
        print(f"📦 Retrieved {len(users)} records. Connecting to database...")
        
        # 1. USE THE MODULE (No passwords here!)
        conn = get_connection()
        if conn is None:
            print("❌ Could not connect to the database. Stopping.")
            return

        cur = conn.cursor()

        # 2. SCHEMA FIX: Changed 'name' to 'full_name' to match your table
        insert_query = """
        INSERT INTO patients (full_name, age, symptoms)
        VALUES (%s, %s, %s)
        """

        count = 0
        total = len(users)

        for user in users:
            count += 1
            
            # Extract Data
            first = user['name']['first']
            last = user['name']['last']
            full_name = f"{first} {last}"
            age = user['dob']['age']
            symptom = random.choice(SYMPTOMS_LIST)

            # Execute
            cur.execute(insert_query, (full_name, age, symptom))
            print(f"   Importing {count}/{total}: {full_name} ({age}, {symptom})")

        # Commit all changes
        conn.commit()
        print("\n✅ Success! All 50 records have been imported.")
        cur.close()

    except requests.exceptions.RequestException as e:
        print(f"\n❌ API Error: {e}")
        
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        # Only rollback if we actually have a connection
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()
            print("🔒 Connection closed.")

if __name__ == "__main__":
    ingest_data()