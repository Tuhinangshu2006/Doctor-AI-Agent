from db_connect import get_connection, DB_URL

def debug():
    print("🔍 --- DIAGNOSTIC REPORT ---")
    
    # 1. Check where we are connecting
    masked_url = DB_URL.split("@")[-1] if "@" in DB_URL else "UNKNOWN"
    print(f"📡 Connecting to Server: ...@{masked_url}")
    
    conn = get_connection()
    if not conn:
        print("❌ Connection Failed!")
        return

    cur = conn.cursor()
    
    # 2. Count the rows
    cur.execute("SELECT COUNT(*) FROM patients;")
    count = cur.fetchone()[0]
    print(f"📊 Total Patients found: {count}")
    
    # 3. Show the last 5 entries
    if count > 0:
        print("\n📋 Last 5 Patients Added:")
        cur.execute("SELECT id, full_name, created_at FROM patients ORDER BY id DESC LIMIT 5;")
        rows = cur.fetchall()
        for row in rows:
            print(f"   ID {row[0]}: {row[1]} (Created: {row[2]})")
    
    conn.close()
    print("\n--------------------------")

if __name__ == "__main__":
    debug()