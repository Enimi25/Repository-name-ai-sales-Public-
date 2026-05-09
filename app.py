from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import urllib.request
import urllib.error

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
            "reply": "AI is not connected yet. I can still help with pricing, booking, or payment."
        })

    system_prompt = f"""
You are an AI sales assistant embedded on a website.

Business context:
- Site name: {site_name}
- Business type: {business_type}
- Offer: {offer}
- Price starts from: {price}
- Payment link: {payment_link}

Your job:
- Act like a confident sales assistant.
- Keep answers short and useful.
- Help visitors understand the offer.
- Guide people toward one of these actions:
  1. get price
  2. book appointment
  3. pay now
  4. leave email or phone
- Ask only one question at a time.
- Do not write long explanations.
- Do not say you are an AI model.
- If user asks price, say the price starts from {price}.
- If user wants to book, ask for email or phone.
- If user wants to pay, send this payment link: {payment_link}.
- If user is unsure, explain the value in one short paragraph and ask what they want to do next.
"""

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "temperature": 0.4,
        "max_tokens": 220
    }

    try:
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=25) as response:
            result = json.loads(response.read().decode("utf-8"))

        reply = result["choices"][0]["message"]["content"]

        return JSONResponse({"reply": reply})

    except urllib.error.HTTPError as e:
        return JSONResponse({
            "reply": "AI is temporarily unavailable. I can still help with pricing, booking, or payment."
        })

    except Exception:
        return JSONResponse({
            "reply": "Connection issue. Please try again in a moment."
        })
