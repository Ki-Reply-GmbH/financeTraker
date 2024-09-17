import os
from langchain_openai import ChatOpenAI
from config import GPT_MODEL_NAME, MAX_TOKENS_COUNT, TEMPERATURE, STREAMING
def setup_llm():
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key is None:
        raise ValueError("OpenAI API key not found. Please check the environment variable.")
    
    chat = ChatOpenAI(
        model=GPT_MODEL_NAME,
        api_key=api_key,
        max_tokens=MAX_TOKENS_COUNT,
        temperature=TEMPERATURE,
        streaming=STREAMING
        
    )
    
    return chat
