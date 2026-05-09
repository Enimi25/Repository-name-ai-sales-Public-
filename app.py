from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os

app = FastAPI()

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

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()

    message = data.get("message", "")
    site_name = data.get("siteName", "this business")
    business_type = data.get("businessType", "online business")
    offer = data.get("offer", "AI Sales Assistant")
    price = data.get("price", "$99/month")
    payment_link = data.get("paymentLink", "https://buy.stripe.com/test_your_payment_link")

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return JSONResponse({
            "reply": "AI is not connected yet. Please try again later."
        })

    client = Groq(api_key=api_key.strip())

    system_prompt = f"""
You are an AI sales assistant embedded on a website.

ABSOLUTE LANGUAGE RULE:
- Understand all major human languages.
- Always answer in the same language as the user's intent.
- If the user writes in Russian Cyrillic, answer in Russian Cyrillic.
- If the user writes Russian using Latin letters / transliteration, answer in normal Russian Cyrillic.
- Examples of Russian transliteration:
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
- If user wants to pay, send this payment link: {payment_link}.
- If user asks about Instagram or social media, answer that the business can connect Instagram later, but now you can help here with price, booking, or payment.
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
            "reply": reply
        })

    except Exception as e:
        print("GROQ SDK ERROR:", str(e))
        return JSONResponse({
            "reply": "AI connection error. Please try again."
        })
