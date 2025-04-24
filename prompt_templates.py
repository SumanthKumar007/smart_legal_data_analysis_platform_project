from langchain_core.prompts import ChatPromptTemplate

custom_prompt_template = ChatPromptTemplate.from_template("""
Use the pieces of information provided in the context and previous conversation history to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Don't provide anything out of the given context.

Previous Conversation:
{history}

Question: {question} 
Context: {context} 
Answer:
""")

summary_prompt_template = ChatPromptTemplate.from_template("""
Summarize the given legal document concisely while preserving key details.
Provide a structured summary that highlights the most important points.

Document:
{context}

Summary:
""")
