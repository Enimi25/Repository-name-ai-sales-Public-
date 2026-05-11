from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
import json
import re
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime

app = FastAPI()

LEADS_FILE = "leads.json"
COMPANIES_FILE = "companies.json"

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


def load_companies():
    if not os.path.exists(COMPANIES_FILE):
        return {}

    try:
        with open(COMPANIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_companies(companies):
    with open(COMPANIES_FILE, "w", encoding="utf-8") as f:
        json.dump(companies, f, ensure_ascii=False, indent=2)


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
                "User-Agent": "AI-Sales-Assistant/1.0"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=20) as response:
            body = response.read().decode("utf-8")
            print("GOOGLE SHEETS RESPONSE:", body)

        return True

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print("GOOGLE SHEETS HTTP ERROR:", e.code, error_body)
        return False

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


@app.get("/connect/google")
def connect_google(companyId: str = "default_company"):
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

    if not client_id or not redirect_uri:
        return HTMLResponse("""
        <h2>Google OAuth is not configured</h2>
        <p>Missing GOOGLE_CLIENT_ID or GOOGLE_REDIRECT_URI in Render Environment.</p>
        """)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/calendar.events",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid"
    ]

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
        "state": companyId
    }

    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)

    return RedirectResponse(auth_url)


@app.get("/google/callback")
def google_callback(code: str = "", state: str = "default_company"):
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

    if not code:
        return HTMLResponse("""
        <h2>Google connection failed</h2>
        <p>No authorization code received.</p>
        """)

    if not client_id or not client_secret or not redirect_uri:
        return HTMLResponse("""
        <h2>Google OAuth is not configured</h2>
        <p>Missing GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, or GOOGLE_REDIRECT_URI.</p>
        """)

    try:
        token_payload = urllib.parse.urlencode({
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }).encode("utf-8")

        token_req = urllib.request.Request(
            "https://oauth2.googleapis.com/token",
            data=token_payload,
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            method="POST"
        )

        with urllib.request.urlopen(token_req, timeout=25) as token_response:
            token_data = json.loads(token_response.read().decode("utf-8"))

        access_token = token_data.get("access_token", "")
        refresh_token = token_data.get("refresh_token", "")

        user_email = ""
        user_name = ""

        if access_token:
            user_req = urllib.request.Request(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={
                    "Authorization": "Bearer " + access_token
                },
                method="GET"
            )

            with urllib.request.urlopen(user_req, timeout=25) as user_response:
                user_data = json.loads(user_response.read().decode("utf-8"))
                user_email = user_data.get("email", "")
                user_name = user_data.get("name", "")

        company_id = state or "default_company"

        companies = load_companies()
        old_company = companies.get(company_id, {})

        if not refresh_token:
            refresh_token = old_company.get("refresh_token", "")

        companies[company_id] = {
            "companyId": company_id,
            "google_connected": True,
            "google_email": user_email,
            "google_name": user_name,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "connected_at": datetime.utcnow().isoformat() + "Z",
            "calendar_id": "primary",
            "sheet_id": old_company.get("sheet_id", "")
        }

        save_companies(companies)

        return HTMLResponse(f"""
        <html>
          <body style="font-family: Arial; padding: 40px;">
            <h1>✅ Google connected successfully</h1>
            <p><b>Company ID:</b> {company_id}</p>
            <p><b>Google account:</b> {user_email}</p>
            <p>You can close this page.</p>
          </body>
        </html>
        """)

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print("GOOGLE OAUTH HTTP ERROR:", e.code, error_body)
        return HTMLResponse(f"""
        <h2>Google OAuth error</h2>
        <pre>{error_body}</pre>
        """)

    except Exception as e:
        print("GOOGLE OAUTH ERROR:", str(e))
        return HTMLResponse(f"""
        <h2>Google OAuth error</h2>
        <pre>{str(e)}</pre>
        """)


@app.get("/company/status")
def company_status(companyId: str = "default_company"):
    companies = load_companies()
    company = companies.get(companyId)

    if not company:
        return JSONResponse({
            "companyId": companyId,
            "google_connected": False
        })

    return JSONResponse({
        "companyId": companyId,
        "google_connected": company.get("google_connected", False),
        "google_email": company.get("google_email", ""),
        "google_name": company.get("google_name", ""),
        "calendar_id": company.get("calendar_id", "primary"),
        "sheet_id": company.get("sheet_id", ""),
        "connected_at": company.get("connected_at", "")
    })


@app.get("/companies")
def get_companies():
    companies = load_companies()

    safe_companies = {}

    for company_id, company in companies.items():
        safe_companies[company_id] = {
            "companyId": company.get("companyId", company_id),
            "google_connected": company.get("google_connected", False),
            "google_email": company.get("google_email", ""),
            "google_name": company.get("google_name", ""),
            "calendar_id": company.get("calendar_id", "primary"),
            "sheet_id": company.get("sheet_id", ""),
            "connected_at": company.get("connected_at", "")
        }

    return JSONResponse({"companies": safe_companies})


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
