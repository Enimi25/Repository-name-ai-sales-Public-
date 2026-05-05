from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/widget.js")
def widget():
    return FileResponse("widget.js")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "").lower()

    # простая логика (пока без AI)
    if "price" in message:
        reply = "Our price starts from $99/month."
    elif "book" in message:
        reply = "Sure. Send your email or phone and I’ll confirm."
    elif "pay" in message:
        reply = "Here is your payment link: https://buy.stripe.com/test"
    else:
        reply = "I can help with pricing, booking or payment."

    return JSONResponse({"reply": reply})
