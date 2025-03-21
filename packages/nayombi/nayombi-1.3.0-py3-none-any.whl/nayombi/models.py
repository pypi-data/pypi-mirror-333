# models.py
# import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai.chat_models import ChatMistralAI
# from dotenv import load_dotenv
# load_dotenv()
def initialize_policy_model(mistral_api):
    """Initialize the model responsible for enforcing the system policy."""
    return ChatMistralAI(
        model="mistral-large-latest",
        temperature=0,
        max_retries=2,
        api_key=mistral_api,
    )

def initialize_execution_model(google_api_key):
    """Initialize the model responsible for database task execution."""
    #print(google_api_key)
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=google_api_key,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=5,
    )
