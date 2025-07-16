# app/pirate/chain.py
from langchain_ollama import ChatOllama  # updated import

from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(
    model="gemma3:1b",
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that gives information."),
    ("human", "{input}"),
])

chain = prompt | llm
