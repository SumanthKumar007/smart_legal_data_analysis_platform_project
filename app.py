import os
os.environ["STREAMLIT_WATCH_DIRECTORIES"] = "false"

import sys
if '_classes' in sys.modules:
    del sys.modules['_classes']



import re
from PyPDF2 import PdfReader
import streamlit as st
import time
import base64
from vector_database import index_pdf, upload_pdf, retrieve_docs
from services.llm_service import answer_query, summarize_document
from services.pdf_report import generate_report
from logger import logger

st.set_page_config(page_title="AI Lawyer", layout="centered")

# Load and display image logo
with open("compliant.png", "rb") as f:
    image_data = f.read()
    encoded_image = base64.b64encode(image_data).decode()

st.markdown(
    f"""
    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 20px;">
        <img src="data:image/png;base64,{encoded_image}" width="120"/>
    </div>
    """,
    unsafe_allow_html=True
)

# Header & CSS styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
        .custom-header {
            text-align: center;
            margin-bottom: 20px;
        }
        .custom-header h1 {
            font-family: 'Bebas Neue', sans-serif;
            color: white;
            font-size: 48px;
            margin-top: 10px;
        }
        body {
            background-color: #eef1f5;
            color: #333;
        }
        .stTextArea textarea {
            font-size: 16px;
            background-color: #000 !important;
            color: #fff !important;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #555;
        }
        .stButton button {
            background-color: #2e7d32;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
        }
        .stButton button:hover {
            background-color: #1b5e20;
        }
        .summary-box, .chat-message {
            background-color: #ffffff;
            padding: 15px;
            border-left: 5px solid #2e7d32;
            border-radius: 6px;
            color: #000;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>
    <div class="custom-header">
        <h1>🤖 Legal AI Chatbot</h1>
    </div>
""", unsafe_allow_html=True)

# Session initialization
if "user_queries" not in st.session_state:
    st.session_state.user_queries = []
if "ai_responses" not in st.session_state:
    st.session_state.ai_responses = []
if "pdf_filename" not in st.session_state:
    st.session_state.pdf_filename = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""

# Upload + summarize + index
uploaded_file = st.file_uploader("📄 Please upload a legal document (PDF) to begin", type="pdf")

if uploaded_file:
    current_file_name = uploaded_file.name
    if st.session_state.pdf_filename != current_file_name:
        with st.spinner("📂 Loading document..."):
            try:
                file_path = upload_pdf(uploaded_file)
                st.session_state.pdf_filename = current_file_name
                index_pdf(file_path)
                time.sleep(1)
                logger.info(f"Document indexed: {file_path}")
                st.success("✅ Document successfully loaded")

                docs = retrieve_docs("What is this document about?", uploaded_file.name)
                brief = summarize_document(docs)
                st.markdown(f"<div class='summary-box'><b>📑 Document Overview:</b><br>{brief}</div>", unsafe_allow_html=True)
                st.markdown("<i>💬 Please provide your questions and doubts about this document. I will help you understand it clearly.</i>", unsafe_allow_html=True)

            except Exception as e:
                st.error("❌ Failed to process document.")
                logger.exception("Upload or indexing failed")
        st.session_state.user_queries = []
        st.session_state.ai_responses = []
        st.session_state.summary = ""

# QA Interaction
if st.session_state.pdf_filename:
    query = st.text_area("💬 Enter your legal question below:", height=100)
    if st.button("🧠 Generate Response"):
        if not query.strip():
            st.warning("⚠️ Please enter a valid question.")
        else:
            start = time.time()
            with st.spinner("🤖 Generating response, please wait..."):
                try:
                    docs = retrieve_docs(query, st.session_state.pdf_filename)
                    history = ""
                    for q, a in zip(st.session_state.user_queries, st.session_state.ai_responses):
                        history += f"User: {q}\nAI: {a}\n"

                    response = answer_query(docs, query, history)
                    end = time.time()
                    duration = round(end - start, 2)

                    st.markdown(f"<div class='chat-message'><strong>User:</strong> {query}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='chat-message'><strong>AI Lawyer:</strong> {response}<br><small>⏱️ Response time: {duration} seconds</small></div>", unsafe_allow_html=True)

                    st.session_state.user_queries.append(query)
                    st.session_state.ai_responses.append(response)

                    logger.info(f"Answered: {query}")
                except Exception as e:
                    st.error("❌ Failed to generate response.")
                    logger.exception("Query failed")

# Chat history + report
if st.session_state.user_queries:
    st.markdown("---")
    st.markdown("### 📚 Chat History")
    for q, a in zip(st.session_state.user_queries, st.session_state.ai_responses):
        st.markdown(f"<div class='chat-message'><strong>User:</strong> {q}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-message'><strong>AI Lawyer:</strong> {a}</div>", unsafe_allow_html=True)

    if st.button("📥 Generate Chat Report"):
        try:
            # Generate the report
            report_path = generate_report(st.session_state.user_queries, st.session_state.ai_responses)
            
            # Use Streamlit's download button to enable single-click download
            with open(report_path, "rb") as file:
                st.download_button(
                    label="📄 Download Report",
                    data=file,
                    file_name="AI_Lawyer_Report.pdf",
                    mime="application/pdf"
                )
            logger.info("User downloaded chat report")
    
        except Exception as e:
            st.error("❌ Failed to generate or download the report.")
            logger.exception("Report generation failed")

