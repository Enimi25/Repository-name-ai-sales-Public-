from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
import json
import re
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

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
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

    if not sheet_id or not service_account_json:
        print("GOOGLE SHEETS NOT CONFIGURED")
        return False

    try:
        service_account_info = json.loads(service_account_json)

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=scopes
        )

        client = gspread.authorize(credentials)
        sheet = client.open_by_key(sheet_id).sheet1

        sheet.append_row([
            lead.get("time", ""),
            lead.get("companyId", ""),
            lead.get("siteName", ""),
            lead.get("source", ""),
            lead.get("language", ""),
            lead.get("message", ""),
            lead.get("email", ""),
            lead.get("phone", ""),
            lead.get("status", "")
        ])

        return True

    except Exception as e:
        print("GOOGLE SHEETS ERROR:", str(e))
        return False


def save_lead(message, email, phone, source, language, site_name, company_id):
    lead = {
        "time": datetime.utcnow().isoformat() + "Z",
        "companyId": company_id,
        "siteName": site_name,
        "source": source,
        "language": language,
        "message": message,
        "email": email,
        "phone": phone,
        "status": "new"
    }

    save_lead_local(lead)
    saved_to_sheets = save_lead_to_google_sheets(lead)

    return {
        "lead": lead,
        "saved_to_sheets": saved_to_sheets
    }


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()

    message = data.get("message", "")
    company_id = data.get("companyId", "default_company")
    site_name = data.get("siteName", "this business")
    business_type = data.get("businessType", "online business")
    offer = data.get("offer", "AI Sales Assistant")
    price = data.get("price", "$99/month")
    payment_link = data.get("paymentLink", "https://buy.stripe.com/test_your_payment_link")
    source = data.get("source", "website widget")

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return JSONResponse({
            "reply": "AI is not connected yet. Please try again later."
        })

    email = extract_email(message)
    phone = extract_phone(message)
    language = detect_language_hint(message)

    lead_saved = False
    saved_to_sheets = False

    if email or phone:
        result = save_lead(
            message=message,
            email=email,
            phone=phone,
            source=source,
            language=language,
            site_name=site_name,
            company_id=company_id
        )

        lead_saved = True
        saved_to_sheets = result["saved_to_sheets"]

    client = Groq(api_key=api_key.strip())

    system_prompt = f"""
You are an AI sales assistant embedded on a website.

ABSOLUTE LANGUAGE RULE:
- Understand all major human languages.
- Always answer in the same language as the user's intent.
- If the user writes in Russian Cyrillic, answer in Russian Cyrillic.
- If the user writes Russian using Latin letters / transliteration, answer in normal Russian Cyrillic.
- Examples:
  "privet" means "привет"
  "skolko stoit" means "сколько стоит"
  "a vy est v instagram" means "а вы есть в Instagram"
  "hochu zapisatsya" means "хочу записаться"
  "kak oplatit" means "как оплатить"
- If the user writes in English, answer in English.
- If the user writes in Hebrew, answer in Hebrew.
- If the user writes in Spanish, answer in Spanish.
- If the user writes in Arabic, answer in Arabic.
- If the user writes in French, answer in French.
- If the user writes in German, answer in German.
- Never answer Russian transliteration with Latin transliteration.
- Never say "I only speak English".
- Never refuse because of language.
- Never mention translation.

Business context:
- Company ID: {company_id}
- Site name: {site_name}
- Business type: {business_type}
- Offer: {offer}
- Price starts from: {price}
- Payment link: {payment_link}

Your job:
- Act like a confident sales assistant.
- Be friendly, short, natural, and sales-focused.
- Help visitors understand the offer.
- Guide the visitor toward one clear action:
  1. ask price
  2. book appointment
  3. pay now
  4. leave email or phone
- Ask only one question at a time.
- Do not write long explanations.
- Do not say you are an AI model.
- Do not sound robotic.

Sales rules:
- If user asks about price, say that price starts from {price}.
- If user wants to book, ask for email or phone.
- If user sends email or phone, confirm that the request was received and say that the team will contact them soon.
- If user wants to pay, send this payment link: {payment_link}.
- If user asks about Instagram or social media, answer that Instagram/Facebook can be connected later, but now you can help here with price, booking, or payment.
- If user is unsure, explain the value briefly and ask what they want to do next.
- If user says hello, greet them and ask how you can help with price, booking, or payment.
- If user asks what this is, explain that this assistant helps businesses convert website visitors into leads, bookings, and payments.

Answer format:
- 1 to 3 short sentences.
- No markdown.
- No bullets unless really needed.
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.25,
            max_tokens=220
        )

        reply = completion.choices[0].message.content

        return JSONResponse({
            "reply": reply,
            "lead_saved": lead_saved,
            "saved_to_sheets": saved_to_sheets,
            "companyId": company_id
        })

    except Exception as e:
        print("GROQ SDK ERROR:", str(e))
        return JSONResponse({
            "reply": "AI connection error. Please try again."
        })
