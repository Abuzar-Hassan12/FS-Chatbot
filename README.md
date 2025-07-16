# FS-Chatbot

A powerful local chatbot built with [LangChain](https://www.langchain.com/), [LangServe](https://github.com/langchain-ai/langserve), and [Ollama](https://ollama.com/) using the **Gemma3-1b** model. Designed for interactive conversations with markdown support and a smooth web UI.

---

# Features

- Local LLM inference using **Ollama** (`gemma3:1b`)
- Backend powered by **FastAPI**
- LangChain and LangServe integration
- Interactive chat UI with markdown rendering
- Typing indicator, instant response, enter-to-send
- Clickable suggested questions for quick prompts

---

# Project Structure


---

# Setup Instructions

### 1. Install Ollama (for local LLM)
Follow instructions from: https://ollama.com/download

Make sure the `gemma3:1b` model is available:
```bash
ollama pull gemma3:1b

#Clone the Repository
git clone https://github.com/Abuzar-Hassan12/FS-Chatbot.git
cd fs-chatbot/app
#Create a Virtual Environment (optional but recommended)
python -m venv .venv
.\.venv\Scripts\activate     # On Windows
source .venv/bin/activate    # On Linux/Mac


#install Dependancies
pip install -r requirements.txt
