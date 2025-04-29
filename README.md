📄 Smart Legal Document Analysis Platform
A powerful AI-powered tool that allows users to upload legal PDFs, interact with an LLM (Gemini 1.5 Pro), retrieve relevant legal context using vector similarity search (via ChromaDB), get concise summaries, and generate downloadable chat reports in PDF format.






🚀 Features

📁 Upload legal PDF documents
📚 Chunk and embed documents using sentence-transformers/all-MiniLM-L6-v2
🧠 Ask legal questions with context-aware answers using Gemini Pro (Google Generative AI)
📝 Summarize entire documents intelligently
🧾 Download chat history as a structured PDF report
💰 Track usage cost and token metrics
📜 Activity and error logging for transparency






🧰 Tech Stack

Frontend/UI: Streamlit
LLM: Google Gemini 1.5 Pro via langchain-google-genai
Embedding Model: sentence-transformers/all-MiniLM-L6-v2
Vector DB: ChromaDB
PDF Processing: pdfplumber
Logging: Python logging module
Reports: reportlab





💬 Usage

Upload a legal PDF.
Ask questions — the system will fetch relevant chunks and generate an answer.
View token usage and cost in chat_logs.csv.
Download a PDF report of your chat from the sidebar.




