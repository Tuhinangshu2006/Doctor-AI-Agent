import streamlit as st
import httpx

# The URL of your FastAPI Backend
# If you deploy to Render later, you will change this URL.
API_URL = "https://doctor-ai-agent.onrender.com"

st.set_page_config(page_title="Doctor's AI Assistant", page_icon="🏥")

st.title("🏥 AI Doctor Assistant")
st.write("Secure Patient Management & Medical Report Analysis")

# Create Tabs for different features
tab1, tab2 = st.tabs(["💬 Chat with Database", "📄 Analyze Reports (PDF)"])

# --- TAB 1: DATABASE CHAT ---
with tab1:
    st.header("Patient Database Query")
    st.info("Ask questions about your registered patients (e.g., 'Who has a fever?').")
    
    question = st.text_input("Enter your question:", placeholder="Who has a fever?")
    
    if st.button("Ask AI", key="ask_db"):
        if question:
            with st.spinner("Consulting the database..."):
                try:
                    # Send GET request to FastAPI
                    response = httpx.get(f"{API_URL}/ask", params={"q": question}, timeout=60.0)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Answer:")
                        st.write(data["answer"])
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
        else:
            st.warning("Please enter a question first.")

# --- TAB 2: PDF ANALYSIS ---
with tab2:
    st.header("Medical Report Analyzer")
    st.info("Upload a PDF lab report or prescription to get a summary/diagnosis.")
    
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    pdf_question = st.text_input("What do you want to know about this file?", value="Summarize the diagnosis and treatment.")
    
    if st.button("Analyze PDF", key="analyze_pdf"):
        if uploaded_file and pdf_question:
            with st.spinner("Reading document... (This uses AI)"):
                try:
                    # Prepare the file for upload
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    
                    # Send POST request to FastAPI
                    response = httpx.post(
                        f"{API_URL}/analyze-pdf", 
                        params={"question": pdf_question}, 
                        files=files,
                        timeout=30.0 # PDFs take longer to process
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Analysis Result:")
                        st.markdown(data["answer"])
                    else:
                        st.error(f"Server Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"Connection Error: {e}")
        else:
            st.warning("Please upload a file and ask a question.")

# Sidebar info
st.sidebar.title("System Status")
if st.sidebar.button("Check API Connection"):
    try:
        res = httpx.get(API_URL)
        if res.status_code == 200:
            st.sidebar.success("✅ Backend is Online")
        else:
            st.sidebar.error("❌ Backend Error")
    except:
        st.sidebar.error("❌ Backend Offline")