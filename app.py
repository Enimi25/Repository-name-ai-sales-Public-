from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    msg = data.get("message", "").lower()

    if "price" in msg or "цена" in msg:
        reply = "Our price starts from $99/month. I can send you the full price list."
    elif "book" in msg or "appointment" in msg or "запис" in msg:
        reply = "Sure. What day and time works best for your appointment?"
    elif "pay" in msg or "оплат" in msg:
        reply = "I can send you a secure payment link now."
    else:
        reply = "I can help with price list, booking an appointment, or payment."

    return JSONResponse({"reply": reply})
