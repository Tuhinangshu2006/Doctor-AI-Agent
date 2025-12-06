import psycopg2
from db_connect import DB_URL

def get_symptom_counts():
    """
    Counts patients grouped by symptom using SQL.
    Returns a list of tuples: (symptom_name, count)
    """
    conn = None
    results = []
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # SQL does the heavy lifting here with GROUP BY and COUNT
        # We also let SQL sort the results by count (descending)
        query = """
        SELECT symptoms, COUNT(*) 
        FROM patients 
        GROUP BY symptoms 
        ORDER BY COUNT(*) DESC;
        """
        
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error fetching symptom counts: {e}")
    finally:
        if conn: conn.close()
        
    return results

def get_average_age():
    """
    Calculates the average age using SQL AVG function.
    Returns a float or None.
    """
    conn = None
    avg_age = None
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # SQL Aggregation: efficient for millions of rows
        query = "SELECT AVG(age) FROM patients;"
        
        cur.execute(query)
        result = cur.fetchone()
        
        # result is a tuple like (35.4,), we want the first element
        if result:
            avg_age = result[0]
            
        cur.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error fetching average age: {e}")
    finally:
        if conn: conn.close()
        
    return avg_age

def generate_report():
    print("📊 --- PATIENT DATA ANALYSIS REPORT --- 📊\n")
    
    # 1. Symptom Breakdown
    print("1. Symptom Breakdown:")
    counts = get_symptom_counts()
    
    if counts:
        # Basic text formatting for a table look
        print(f"{'Symptom':<20} | {'Count':<10}")
        print("-" * 32)
        for symptom, count in counts:
            print(f"{symptom:<20} | {count:<10}")
    else:
        print("   No data found or table is empty.")
        
    print("\n" + "-" * 32 + "\n")

    # 2. Average Age
    avg_age = get_average_age()
    
    if avg_age:
        # Convert Decimal to float and round to 1 decimal place
        print(f"2. Average Patient Age: {float(avg_age):.1f} years")
    else:
        print("2. Average Patient Age: N/A")
        
    print("\n---------------------------------------")

if __name__ == "__main__":
    generate_report()