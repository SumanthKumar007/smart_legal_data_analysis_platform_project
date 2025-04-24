import logging
import os
import warnings

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("legal-rag")

logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
logging.getLogger("chromadb").setLevel(logging.WARNING)
logging.getLogger("pdfplumber").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.WARNING)
warnings.filterwarnings("ignore", message="CropBox missing from /Page, defaulting to MediaBox")