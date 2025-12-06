import os
import google.generativeai as genai
from dotenv import load_dotenv
from db_connect import get_connection

# 1. Load the Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env file")
else:
    # 2. Configure the Brain
    genai.configure(api_key=api_key)

# --- DYNAMIC MODEL SELECTOR ---
# This block asks Google: "What models can I use?" and picks one.
try:
    print("🔎 Checking available AI models...")
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            
    # print(f"📋 Your Account has access to: {available_models}")

    # Priority list: Try to find a "Flash" model (Fast & Free tier friendly)
    chosen_model = None
    
    # Check for specific stable versions first
    if 'models/gemini-2.0-flash' in available_models:
        chosen_model = 'gemini-2.0-flash'
    elif 'models/gemini-1.5-flash' in available_models:
        chosen_model = 'gemini-1.5-flash'
    elif 'models/gemini-flash-latest' in available_models:
        chosen_model = 'gemini-flash-latest'
    elif 'models/gemini-pro' in available_models:
        chosen_model = 'gemini-pro'
    
    # If none of the specific ones are found, search for ANY flash model
    if not chosen_model:
        for m in available_models:
            if 'flash' in m and 'exp' not in m: # Prefer stable flash over experimental
                chosen_model = m
                break
    
    # Fallback: Just grab the first available one if nothing else matches
    if not chosen_model and len(available_models) > 0:
        chosen_model = available_models[0]

    if not chosen_model:
        print("❌ No text-generation models found for this API key.")
        exit()

    print(f"✅ Selected Model: {chosen_model}")
    model = genai.GenerativeModel(chosen_model)

except Exception as e:
    print(f"⚠️ Error checking models: {e}. Trying default 'gemini-pro'...")
    model = genai.GenerativeModel('gemini-pro')
# ------------------------------

def get_patient_data_as_text():
    """
    Fetches patients from DB and converts them into a text string.
    """
    conn = get_connection()
    if conn is None:
        return "Error: Database Disconnected."
    
    cur = conn.cursor()
    # Fetch 20 patients to keep the prompt small
    cur.execute("SELECT full_name, age, symptoms FROM patients LIMIT 20;")
    rows = cur.fetchall()
    conn.close()
    
    # Format the data into a readable string
    context = ""
    for row in rows:
        context += f"Patient: {row[0]}, Age: {row[1]}, Symptoms: {row[2]}\n"
    
    return context

def ask_agent(question):
    """
    This function accepts a question string, gets data from DB,
    and asks Gemini to answer it.
    """
    # 3. Get the Data
    patient_data = get_patient_data_as_text()
    
    # 4. Create the Prompt
    prompt = f"""
    You are a medical assistant. Answer the question based ONLY on the patient data below.
    
    PATIENT DATA:
    {patient_data}
    
    QUESTION: {question}
    """
    
    try:
        # 5. Direct generation call
        response = model.generate_content(prompt)
        # Return the text so the API can send it to the user
        return response.text
    except Exception as e:
        return f"I encountered an error: {str(e)}"

# Test block - only runs if you type 'python ai_agent.py'
if __name__ == "__main__":
    print(ask_agent("Who has a fever?"))