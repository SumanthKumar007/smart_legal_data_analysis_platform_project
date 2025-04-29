# 📄 Smart Legal Document Analysis Platform

A powerful AI-powered tool that allows users to upload legal PDFs, interact with an LLM (**Gemini 1.5 Pro**), retrieve relevant legal context using vector similarity search (**ChromaDB**), get concise summaries, and generate downloadable chat reports in PDF format.

---

## 🚀 Features

- 📁 **Upload legal PDF documents**  
- 📚 **Chunk and embed documents** using `sentence-transformers/all-MiniLM-L6-v2`  
- 🧠 **Ask legal questions** with context-aware answers using **Gemini Pro (Google Generative AI)**  
- 📝 **Summarize entire documents** intelligently  
- 🧾 **Download chat history** as a structured PDF report  
- 💰 **Track usage cost and token metrics**  
- 📜 **Activity and error logging** for transparency  

---

## 🧰 Tech Stack

| Component         | Technology                                     |
|------------------|-------------------------------------------------|
| **Frontend/UI**   | Streamlit                                       |
| **LLM**           | Google Gemini 1.5 Pro |
| **Embedding Model** | `sentence-transformers/all-MiniLM-L6-v2`        |
| **Vector DB**     | ChromaDB                                        |
| **PDF Processing**| pdfplumber                                      |
| **Logging**       | Python logging module                           |
| **Reports**       | reportlab                                       |

---

## 💬 Usage

1. **Upload a legal PDF**.
2. **Ask your legal questions** — the system will:
   - Fetch relevant document chunks using vector similarity.
   - Generate context-aware answers from Gemini 1.5 Pro.
3. **Summarize full documents** using a single prompt.
4. **View token usage and cost** in `chat_logs.csv`.
5. **Download a PDF report** of your chat from the sidebar.

 ✨ Perfect for law professionals, paralegals, and students seeking quick insights from legal documents with explainable AI.

---


📌 _Pro Tip: Use it to quickly assess contracts, extract clauses, or clarify legal terminology within uploaded files._

---

## Developed by **Sumanth Kumar**.
