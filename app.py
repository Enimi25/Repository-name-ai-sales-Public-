from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import json
import os
import re

app = FastAPI()

LEADS_FILE = "leads.json"
BOOKINGS_FILE = "bookings.json"

COMPANY_NAME = "AI Sales Assistant"

PAYMENT_LINK = "https://buy.stripe.com/test_your_payment_link"
CALENDLY_LINK = "https://calendly.com/your-link/demo"

OFFER_NAME = "AI Sales Assistant for Website"
OFFER_PRICE = "$99/month"


class ChatRequest(BaseModel):
    message: str
    page_url: str | None = None
    session_id: str | None = None


def load_json(file):
    if not os.path.exists(file):
        return []

    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []


def save_json(file, item):
    data = load_json(file)
    data.append(item)

    with open(file, "w") as f:
        json.dump(data, f, indent=2)


def extract_email(text):
    found = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )
    return found[0] if found else None


def extract_phone(text):
    found = re.findall(r"\+?\d[\d\s().-]{7,}\d", text)
    return found[0] if found else None


def wants_payment(message):
    m = message.lower()
    return any(x in m for x in [
        "pay", "payment", "buy", "checkout", "start now",
        "order", "sign me up",
        "oplata", "oplatit", "kupit", "beru", "hochu kupit"
    ])


def wants_booking(message):
    m = message.lower()
    return any(x in m for x in [
        "book", "demo", "call", "meeting", "appointment",
        "schedule", "consultation",
        "zapis", "priem", "sozvon", "vstrecha", "konsultaciya"
    ])


def wants_price(message):
    m = message.lower()
    return any(x in m for x in [
        "price", "pricing", "cost", "how much",
        "cena", "skolko", "stoimost"
    ])


def save_lead(email, phone, message, page_url, session_id, status):
    lead = {
        "created_at": datetime.utcnow().isoformat(),
        "email": email,
        "phone": phone,
        "message": message,
        "page_url": page_url,
        "session_id": session_id,
        "status": status
    }

    save_json(LEADS_FILE, lead)
    return lead


def save_booking(email, phone, message, page_url, session_id):
    booking = {
        "created_at": datetime.utcnow().isoformat(),
        "email": email,
        "phone": phone,
        "message": message,
        "page_url": page_url,
        "session_id": session_id,
        "status": "confirmed",
        "confirmation": "Booking request confirmed"
    }

    save_json(BOOKINGS_FILE, booking)
    return booking


def sales_reply(req):
    message = req.message
    email = extract_email(message)
    phone = extract_phone(message)

    if wants_payment(message):
        save_lead(email, phone, message, req.page_url, req.session_id, "payment_link_sent")

        return (
            f"Great. Here is the payment link:\n{PAYMENT_LINK}\n\n"
            f"Plan: {OFFER_NAME}\n"
            f"Price: {OFFER_PRICE}\n\n"
            "After payment, we will contact you to install the assistant on your website."
        )

    if wants_booking(message):
        if email or phone:
            save_booking(email, phone, message, req.page_url, req.session_id)

            return (
                "Perfect. Your booking request is confirmed.\n\n"
                "Our team will contact you shortly to confirm the exact time.\n\n"
                f"You can also book directly here:\n{CALENDLY_LINK}"
            )

        return (
            "Sure. I can book you in.\n\n"
            "Please send your email or phone number, and I will confirm the request."
        )

    if wants_price(message):
        return (
            f"The starting price is {OFFER_PRICE}.\n\n"
            "It includes a website AI assistant that answers visitors, captures leads, "
            "and sends them to payment or booking.\n\n"
            f"Payment link:\n{PAYMENT_LINK}\n\n"
            f"Demo booking:\n{CALENDLY_LINK}"
        )

    if email or phone:
        save_lead(email, phone, message, req.page_url, req.session_id, "contact_captured")

        return (
            "Thanks. I saved your contact.\n\n"
            "Do you want to start now or book a quick demo?\n\n"
            f"Payment:\n{PAYMENT_LINK}\n\n"
            f"Demo:\n{CALENDLY_LINK}"
        )

    return (
        "Hi. I can help you get started.\n\n"
        "I can do 2 things for you:\n"
        f"1. Send payment link: {PAYMENT_LINK}\n"
        f"2. Book a demo: {CALENDLY_LINK}\n\n"
        "Do you want pricing, demo, or payment link?"
    )


@app.get("/")
def home():
    return {
        "status": "ok",
        "product": "AI Sales Closing Widget",
        "demo": "http://127.0.0.1:8001/demo",
        "leads": "http://127.0.0.1:8001/leads",
        "bookings": "http://127.0.0.1:8001/bookings"
    }


@app.post("/chat")
def chat(req: ChatRequest):
    return {
        "reply": sales_reply(req),
        "session_id": req.session_id or "local-session"
    }


@app.get("/leads")
def get_leads():
    leads = load_json(LEADS_FILE)

    return {
        "total": len(leads),
        "leads": leads
    }


@app.get("/bookings")
def get_bookings():
    bookings = load_json(BOOKINGS_FILE)

    return {
        "total": len(bookings),
        "bookings": bookings
    }


@app.get("/widget.js")
def widget_js():
    js = """
(function () {
  if (window.AISalesCloserLoaded) return;
  window.AISalesCloserLoaded = true;

  const API_URL = "http://127.0.0.1:8001/chat";

  let sessionId = localStorage.getItem("ai_sales_session");

  if (!sessionId) {
    sessionId = "session-" + Date.now();
    localStorage.setItem("ai_sales_session", sessionId);
  }

  const box = document.createElement("div");

  box.innerHTML = `
    <div id="ai-sales-bubble">💬</div>

    <div id="ai-sales-window">
      <div id="ai-sales-header">
        <div>
          <strong>AI Sales Assistant</strong>
          <small>Online now</small>
        </div>
        <button id="ai-sales-close">×</button>
      </div>

      <div id="ai-sales-messages">
        <div class="bot">
          Hi. I can help you start, book a demo, or send the payment link.
        </div>
      </div>

      <div id="ai-sales-quick">
        <button data-text="Show me the price">Price</button>
        <button data-text="I want to book a demo">Book demo</button>
        <button data-text="Send me payment link">Pay now</button>
      </div>

      <div id="ai-sales-input-wrap">
        <input id="ai-sales-input" placeholder="Type your message..." />
        <button id="ai-sales-send">Send</button>
      </div>
    </div>
  `;

  document.body.appendChild(box);

  const style = document.createElement("style");

  style.innerHTML = `
    #ai-sales-bubble {
      position: fixed;
      right: 24px;
      bottom: 24px;
      width: 62px;
      height: 62px;
      border-radius: 50%;
      background: #111;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      cursor: pointer;
      z-index: 999999;
      box-shadow: 0 12px 35px rgba(0,0,0,.3);
    }

    #ai-sales-window {
      position: fixed;
      right: 24px;
      bottom: 96px;
      width: 360px;
      height: 520px;
      background: white;
      border-radius: 18px;
      box-shadow: 0 20px 70px rgba(0,0,0,.3);
      display: none;
      flex-direction: column;
      overflow: hidden;
      z-index: 999999;
      font-family: Arial, sans-serif;
    }

    #ai-sales-header {
      background: #111;
      color: white;
      padding: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    #ai-sales-header small {
      display: block;
      color: #9cffb1;
      margin-top: 3px;
      font-size: 12px;
    }

    #ai-sales-close {
      background: none;
      border: none;
      color: white;
      font-size: 24px;
      cursor: pointer;
    }

    #ai-sales-messages {
      flex: 1;
      padding: 14px;
      overflow-y: auto;
      background: #f6f6f6;
    }

    .bot, .user {
      padding: 10px 12px;
      border-radius: 14px;
      margin-bottom: 10px;
      max-width: 86%;
      font-size: 14px;
      line-height: 1.45;
      white-space: pre-line;
    }

    .bot {
      background: white;
      color: #111;
    }

    .user {
      background: #111;
      color: white;
      margin-left: auto;
    }

    #ai-sales-quick {
      display: flex;
      gap: 6px;
      padding: 10px;
      border-top: 1px solid #eee;
      background: white;
    }

    #ai-sales-quick button {
      flex: 1;
      border: 1px solid #111;
      background: white;
      color: #111;
      border-radius: 999px;
      padding: 8px;
      font-size: 12px;
      cursor: pointer;
    }

    #ai-sales-input-wrap {
      display: flex;
      padding: 10px;
      border-top: 1px solid #ddd;
      gap: 8px;
      background: white;
    }

    #ai-sales-input {
      flex: 1;
      padding: 11px;
      border: 1px solid #ccc;
      border-radius: 12px;
      outline: none;
    }

    #ai-sales-send {
      background: #111;
      color: white;
      border: none;
      border-radius: 12px;
      padding: 10px 14px;
      cursor: pointer;
    }
  `;

  document.head.appendChild(style);

  const bubble = document.getElementById("ai-sales-bubble");
  const win = document.getElementById("ai-sales-window");
  const close = document.getElementById("ai-sales-close");
  const input = document.getElementById("ai-sales-input");
  const send = document.getElementById("ai-sales-send");
  const messages = document.getElementById("ai-sales-messages");
  const quickButtons = document.querySelectorAll("#ai-sales-quick button");

  bubble.onclick = function () {
    win.style.display = "flex";
    bubble.style.display = "none";
  };

  close.onclick = function () {
    win.style.display = "none";
    bubble.style.display = "flex";
  };

  function addMessage(text, cls) {
    const div = document.createElement("div");
    div.className = cls;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  async function sendMessage(customText) {
    const text = customText || input.value.trim();

    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: text,
          page_url: window.location.href,
          session_id: sessionId
        })
      });

      const data = await res.json();
      addMessage(data.reply, "bot");
    } catch (e) {
      addMessage("Something went wrong. Please try again.", "bot");
    }
  }

  send.onclick = function () {
    sendMessage();
  };

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  quickButtons.forEach(function (btn) {
    btn.onclick = function () {
      sendMessage(btn.getAttribute("data-text"));
    };
  });
})();
"""

    return Response(content=js, media_type="application/javascript")


@app.get("/demo")
def demo():
    html = """
<!DOCTYPE html>
<html>
<head>
  <title>Demo Store</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 40px;
      background: #f5f5f5;
    }

    .card {
      background: white;
      padding: 30px;
      border-radius: 18px;
      max-width: 700px;
      margin: auto;
      box-shadow: 0 10px 30px rgba(0,0,0,.08);
    }

    button {
      background: #111;
      color: white;
      border: none;
      padding: 14px 20px;
      border-radius: 12px;
      cursor: pointer;
      font-size: 16px;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>Demo Company Website</h1>
    <p>This page shows how the AI Sales Assistant works on a real client website.</p>
    <p>The bot can capture leads, send payment links, and confirm booking requests.</p>
    <button>Buy Now</button>
  </div>

  <script src="http://127.0.0.1:8001/widget.js"></script>
</body>
</html>
"""

    return HTMLResponse(html)
