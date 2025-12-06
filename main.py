from fastapi import FastAPI, UploadFile, File
from db_connect import get_connection
from ai_agent import ask_agent          # The Database Brain
from pdf_agent import analyze_pdf       # The PDF Brain
import shutil
import os

app = FastAPI()

# 1. The Front Door
@app.get("/")
def read_root():
    return {"message": "Doctor Agent API is Live!", "status": "healthy"}

# 2. Get Raw Patient List (Database only)
@app.get("/patients")
def get_patients():
    try:
        conn = get_connection()
        if conn is None:
            return {"error": "Database connection failed"}
        
        cur = conn.cursor()
        cur.execute("SELECT id, full_name, age, symptoms FROM patients LIMIT 10;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {"patients": rows}
    except Exception as e:
        return {"error": str(e)}

# 3. Chat with the AI (Database + Brain)
# Usage: http://127.0.0.1:8000/ask?q=Who has a fever?
@app.get("/ask")
def ask_doctor_agent(q: str):
    print(f"User asked: {q}")
    answer = ask_agent(q)
    return {"question": q, "answer": answer}

# 4. Chat with PDF (New Feature)
@app.post("/analyze-pdf")
def chat_with_pdf(question: str, file: UploadFile = File(...)):
    """
    Upload a PDF and ask a question about it.
    """
    # Save the uploaded file temporarily so the AI can read it
    temp_filename = f"temp_{file.filename}"
    
    try:
        # Write the uploaded bytes to a temp file on disk
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Run the AI analysis on the saved file
        answer = analyze_pdf(temp_filename, question)
        return {"filename": file.filename, "answer": answer}

    except Exception as e:
        return {"error": str(e)}
        
    finally:
        # Cleanup: Delete the temp file so storage doesn't fill up
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            print(f"🧹 Cleaned up {temp_filename}")