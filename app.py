from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


@app.get("/")
def root():
    return {"status": "ok", "demo": "/demo"}


@app.get("/demo", response_class=HTMLResponse)
def demo():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Sales Assistant</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
*{box-sizing:border-box}
body{
  margin:0;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;
  background:#050507;
  color:white;
  overflow-x:hidden;
}
body:before{
  content:"";
  position:fixed;
  inset:0;
  background:
    radial-gradient(circle at 75% 30%,rgba(124,58,237,.45),transparent 30%),
    radial-gradient(circle at 20% 80%,
