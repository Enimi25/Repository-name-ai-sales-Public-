from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
import json
import re
from datetime import datetime
import urllib.request
import urllib.error

app = FastAPI()

LEADS_FILE = "leads.json"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/widget.js")
def widget():
    return FileResponse("widget.js", media_type="application/javascript")


@app.get("/leads")
def get_leads():
    if not os.path.exists(LEADS_FILE):
        return JSONResponse({"leads": []})

    try:
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            leads = json.load(f)
        return JSONResponse({"leads": leads})
    except Exception:
        return JSONResponse({"leads": []})


def extract_email(text: str):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else ""


def extract_phone(text: str):
    match = re.search(r"(\+?\d[\d\s\-\(\)]{7,}\d)", text)
    return match.group(0).strip() if match else ""


def detect_language_hint(text: str):
    if re.search(r"[а-яА-ЯёЁ]", text):
        return "ru"
    if re.search(r"[\u0590-\u05FF]", text):
        return "he"
    if re.search(r"[\u0600-\u06FF]", text):
        return "ar"
    return "auto"


def save_lead_local(lead):
    leads = []

    if os.path.exists(LEADS_FILE):
        try:
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads = json.load(f)
        except Exception:
            leads = []

    leads.append(lead)

    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)


def save_lead_to_google_sheets(lead):
    webhook_url = os.getenv("GOOGLE_SHEETS_WEBHOOK_URL")

    if not webhook_url:
        print("GOOGLE_SHEETS_WEBHOOK_URL is missing")
        return False

    try:
        payload = json.dumps(lead).encode("utf-8")

        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AI-Sales
