from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/widget.js")
def widget():
    return FileResponse(os.path.join(BASE_DIR, "widget.js"))
