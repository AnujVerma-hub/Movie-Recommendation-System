from Rag_system.prompt_builder import Prompt_build, format_context
from llm.ollama_client import ollama_chat
from Rag_system.config import *
from Rag.retriever import retrieve_docs




def rag_answer(user_prompt):
    docs = retrieve_docs(DATA_PATH,user_prompt)

    retrieved_context = format_context(docs)

    final_prompt = f"""
    {user_prompt}

    Additional reference context:
    {retrieved_context}
    """
    
    

    return ollama_chat(user_prompt)


