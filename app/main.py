import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import debug, explain, generate, optimize

load_dotenv()

app = FastAPI(
    title="AI Program Generator, Debugger & Optimizer",
    description="FastAPI POC for an intelligent coding assistant powered by Groq.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(generate.router, prefix="/generate", tags=["Generate"])
app.include_router(explain.router, prefix="/explain", tags=["Explain"])
app.include_router(debug.router, prefix="/debug", tags=["Debug"])
app.include_router(optimize.router, prefix="/optimize", tags=["Optimize"])


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
