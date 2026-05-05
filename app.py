from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (чтобы widget работал везде)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# сайт
@app.get("/")
def home():
    return FileResponse("index.html")

# widget.js
@app.get("/widget.js")
def widget():
    return FileResponse("widget.js")


# 🔥 УМНЫЙ ОТВЕТ БОТА
@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    msg = data.get("message", "").lower()

    # логика
    if "price" in msg or "цена" in msg:
        reply = "Стоимость начинается от $99/месяц. Хочешь оплатить или посмотреть демо?"

    elif "demo" in msg or "book" in msg or "запис" in msg:
        reply = "Отлично. Оставь email или телефон — я запишу тебя на демо."

    elif "pay" in msg or "оплат" in msg:
        reply = "Вот ссылка на оплату: https://buy.stripe.com/test_your_payment_link"

    elif "hello" in msg or "hi" in msg:
        reply = "Привет! Я могу помочь с оплатой или записью на демо."

    else:
        reply = "Я могу помочь с ценой, оплатой или записью на демо. Что тебя интересует?"

    return JSONResponse({"reply": reply})
