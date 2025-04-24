import os
import csv
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from config import COST_PER_1K_INPUT, COST_PER_1K_OUTPUT, CSV_LOG_PATH, MODEL_NAME
from prompt_templates import custom_prompt_template, summary_prompt_template
from utils.document_utils import get_context
from logger import logger

llm_model = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.3)

def _log_usage(response):
    usage = getattr(response, "usage_metadata", None)
    input_tokens = usage.get("input_tokens", 0) if usage else 0
    output_tokens = usage.get("output_tokens", 0) if usage else 0
    total_tokens = input_tokens + output_tokens
    cost = round((input_tokens * COST_PER_1K_INPUT + output_tokens * COST_PER_1K_OUTPUT) / 1000, 6)

    log_row = {
        "timestamp": datetime.now().isoformat(),
        "model": MODEL_NAME,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost_usd": cost
    }

    file_exists = os.path.isfile(CSV_LOG_PATH)
    with open(CSV_LOG_PATH, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=log_row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_row)

    return total_tokens, cost

def answer_query(documents, query, history=""):
    context = get_context(documents)
    chain = custom_prompt_template | llm_model

    try:
        response = chain.invoke({"question": query, "context": context, "history": history})
        total_tokens, cost = _log_usage(response)
        logger.info(f"Answer generated. Tokens: {total_tokens}, Cost: ${cost}")
    except Exception as e:
        logger.exception("Failed to generate response.")
        return "❌ An error occurred while answering your question."

    return response.content if hasattr(response, "content") else str(response)

def summarize_document(documents):
    context = get_context(documents)
    chain = summary_prompt_template | llm_model

    try:
        response = chain.invoke({"context": context})
        total_tokens, cost = _log_usage(response)
        logger.info(f"Document summarized. Tokens: {total_tokens}, Cost: ${cost}")
    except Exception as e:
        logger.exception("Failed to summarize document.")
        return "❌ An error occurred while summarizing the document."

    return response.content if hasattr(response, "content") else str(response)