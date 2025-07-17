# my_app/app/server.py

import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from langserve import add_routes
from app.training import chain as training_chain
import markdown as md

# Set up project root and load .env
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # my_app/
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

# Add app directory to sys.path (for import resolution)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = FastAPI(openapi_url=None, docs_url=None)

# ✅ Serve static files (CSS/JS/Images)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# ✅ Serve index.html from templates folder
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# ✅ Chat endpoint
@app.post("/chat")
async def chat_api(request: Request):
    data = await request.json()
    user_input = data.get("input", "").strip()

    if not user_input:
        return JSONResponse(content={"response": "⚠️ Please type something."})

    result = training_chain.invoke({"input": user_input})
    html_response = md.markdown(result.content)
    return JSONResponse(content={"response": html_response})

# ✅ LangServe route
add_routes(app, training_chain, path="/training")

# ✅ Run server locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
