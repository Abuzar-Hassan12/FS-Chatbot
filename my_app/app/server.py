# app/server.py

import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from langserve import add_routes
from my_app.app.training import chain as training_chain
import markdown as md

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# Add current directory to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# FastAPI app
app = FastAPI(openapi_url=None, docs_url=None)

# Mount static directory for css/js
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("templates/index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/chat")
async def chat_api(request: Request):
    data = await request.json()
    user_input = data.get("input", "").strip()

    if not user_input:
        return JSONResponse(content={"response": "⚠️ Please type something."})

    result = training_chain.invoke({"input": user_input})
    html_response = md.markdown(result.content)
    return JSONResponse(content={"response": html_response})

# Add LangChain route
add_routes(app, training_chain, path="/training")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)