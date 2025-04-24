
import os
import re
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from chromadb import PersistentClient
from logger import logger

pdfs_directory = 'pdfs/'
CHROMA_DB_DIR = "vector_store/chroma_db"

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
client = PersistentClient(path=CHROMA_DB_DIR)

def upload_pdf(file):
    os.makedirs(pdfs_directory, exist_ok=True)
    file_path = os.path.join(pdfs_directory, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    logger.info(f"PDF saved to: {file_path}")
    return file_path

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    return loader.load()

def create_chunks(documents, file_name):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    for chunk in chunks:
        chunk.metadata["source"] = file_name
    return chunks

def sanitize_collection_name(file_name):
    name = os.path.splitext(file_name)[0].lower()
    name = re.sub(r'[^a-z0-9._-]', '-', name)
    return name.strip("-")[:63]

def index_pdf(file_path):
    file_name = os.path.basename(file_path)
    collection_name = sanitize_collection_name(file_name)
    logger.info(f"Indexing collection: {collection_name}")
    documents = load_pdf(file_path)
    chunks = create_chunks(documents, file_name)
    Chroma.from_documents(chunks, embedding_model, collection_name=collection_name, client=client)
    logger.info(f"Indexed {len(chunks)} chunks for {file_name}")

def retrieve_docs(query, file_name):
    collection_name = sanitize_collection_name(file_name)
    db = Chroma(client=client, collection_name=collection_name, embedding_function=embedding_model)
    return db.similarity_search(query, k=5)

