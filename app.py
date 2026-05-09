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
            "reply": "GROQ_API_KEY is missing in Render Environment."
        })

    client = Groq(api_key=api_key.strip())

    system_prompt = f"""
You are an AI sales assistant embedded on a website.

Business context:
- Site name: {site_name}
- Business type: {business_type}
- Offer: {offer}
- Price starts from: {price}
- Payment link: {payment_link}

Rules:
- Answer briefly.
- Act like a confident sales assistant.
- Help with pricing, booking, payment, or lead capture.
- Ask only one question at a time.
- If user asks price, say price starts from {price}.
- If user wants booking, ask for email or phone.
- If user wants payment, send this payment link: {payment_link}.
- Do not say you are an AI model.
- Do not write long explanations.
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.4,
            max_tokens=220
        )

        reply = completion.choices[0].message.content
        return JSONResponse({"reply": reply})

    except Exception as e:
        print("GROQ SDK ERROR:", str(e))
        return JSONResponse({
            "reply": "Groq SDK error: " + str(e)[:500]
        })
