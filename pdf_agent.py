import os
from dotenv import load_dotenv
import pypdf  # <--- Pure Python PDF Reader
import google.generativeai as genai

# 1. Load Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found.")
else:
    genai.configure(api_key=api_key)

# --- DYNAMIC MODEL SELECTOR ---
try:
    print("🔎 PDF Agent checking available AI models...")
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)

    chosen_model = None
    if 'models/gemini-2.0-flash' in available_models: chosen_model = 'gemini-2.0-flash'
    elif 'models/gemini-1.5-flash' in available_models: chosen_model = 'gemini-1.5-flash'
    elif 'models/gemini-pro' in available_models: chosen_model = 'gemini-pro'
    
    if not chosen_model and len(available_models) > 0: chosen_model = available_models[0]

    print(f"✅ PDF Agent Selected Model: {chosen_model}")
    model = genai.GenerativeModel(chosen_model)

except Exception as e:
    print(f"⚠️ Error selecting model: {e}. Defaulting to 'gemini-pro'.")
    model = genai.GenerativeModel('gemini-pro')
# ------------------------------

def analyze_pdf(file_path, question):
    print("📄 Processing PDF (Pure Python Mode)...")
    
    try:
        # 2. Load PDF Text Manually (No LangChain)
        reader = pypdf.PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
            
        print(f"   - Extracted {len(full_text)} characters.")

        # 3. Simple Context Filtering
        # Limit context to ~30k characters to fit in free tier
        context_text = full_text[:30000] 
        
        # 4. Ask Gemini
        print("   - Asking Gemini...")
        
        prompt = f"""
        You are a medical assistant. Answer the question based ONLY on the context below.
        
        CONTEXT:
        {context_text}
        
        QUESTION: 
        {question}
        """
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return f"I encountered an error reading the PDF: {str(e)}"

if __name__ == "__main__":
    pass