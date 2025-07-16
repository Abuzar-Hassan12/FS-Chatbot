# BEFORE (likely in pirate/chain.py)
# from langchain.chat_models import ChatOpenAI
# model = ChatOpenAI()

# AFTER — switch to your local model
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(
    model="gemma3:1b",
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that gives information."),
        ("human", "{input}"),
    ]
)

cchain = prompt | llm
