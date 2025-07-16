from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
# Get the full path to the .env file inside my_app
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key)

prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.
Answer the user's question clearly and concisely.

Question: {input}
""")

chain: Runnable = prompt | llm
