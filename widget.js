(function () {
  if (window.AISalesWidgetLoaded) return;
  window.AISalesWidgetLoaded = true;

  const SCRIPT_URL = "https://repository-name-ai-sales-public.onrender.com";
  const API = SCRIPT_URL + "/chat";

  const config = window.AISalesAssistantConfig || {};

  const siteName = config.siteName || document.title || "this business";
  const businessType = config.businessType || "online business";
  const offer = config.offer || "AI Sales Assistant";
  const price = config.price || "$99/month";
  const paymentLink = config.paymentLink || "https://buy.stripe.com/test_your_payment_link";

  const css = document.createElement("style");
  css.innerHTML = `
    #aiw-btn {
      position: fixed;
      right: 24px;
      bottom: 24px;
      width: 64px;
      height: 64px;
      border-radius: 50%;
      border: none;
      background: linear-gradient(135deg,#7c3aed,#4f46e5);
      color: white;
      font-size: 26px;
      cursor: pointer;
      z-index: 999999;
      box-shadow: 0 16px 45px rgba(124,58,237,0.55);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: 0.2s ease;
    }

    #aiw-btn:hover {
      transform: translateY(-2px) scale(1.04);
      box-shadow: 0 22px 60px rgba(124,58,237,0.7);
    }

    #aiw-box {
      position: fixed;
      right: 24px;
      bottom: 102px;
      width: 370px;
      height: 540px;
      background: #0b0b0f;
      color: white;
      border-radius: 26px;
      display: none;
      flex-direction: column;
      overflow: hidden;
      z-index: 999999;
      border: 1px solid rgba(255,255,255,0.1);
      box-shadow: 0 40px 120px rgba(0,0,0,0.8);
      font-family: Arial, sans-serif;
    }

    #aiw-head {
      padding: 18px;
      background: #0b0b0f;
      border-bottom: 1px solid rgba(255,255,255,0.08);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    #aiw-title {
      font-weight: 800;
      font-size: 16px;
    }

    #aiw-status {
      color: #7cffbd;
      font-size: 12px;
      margin-top: 3px;
    }

    #aiw-close {
      background: none;
      border: none;
      color: white;
      font-size: 22px;
      cursor: pointer;
      opacity: 0.8;
    }

    #aiw-messages {
      flex: 1;
      padding: 16px;
      overflow-y: auto;
      background:
        radial-gradient(circle at 80% 20%, rgba(124,58,237,0.18), transparent 35%),
        linear-gradient(180deg,#111118,#0b0b0f);
    }

    .aiw-msg {
      max-width: 84%;
      padding: 12px 14px;
      margin-bottom: 12px;
      border-radius: 16px;
      font-size: 14px;
      line-height: 1.4;
      white-space: pre-wrap;
    }

    .aiw-user {
      margin-left: auto;
      background: linear-gradient(135deg,#7c3aed,#4f46e5);
      color: white;
      border-bottom-right-radius: 6px;
    }

    .aiw-bot {
      background: rgba(255,255,255,0.08);
      color: #f2f2f5;
      border: 1px solid rgba(255,255,255,0.08);
      border-bottom-left-radius: 6px;
    }

    #aiw-actions {
      display: flex;
      gap: 8px;
      padding: 12px;
      background: #0f0f13;
      border-top: 1px solid rgba(255,255,255,0.08);
    }

    #aiw-actions button {
      flex: 1;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.12);
      background: rgba(255,255,255,0.05);
      color: white;
      padding: 10px 8px;
      font-weight: 700;
      font-size: 12px;
      cursor: pointer;
      transition: 0.2s ease;
    }

    #aiw-actions button:hover {
      background: rgba(124,58,237,0.25);
      border-color: rgba(168,85,247,0.5);
    }

    #aiw-input-row {
      display: flex;
      gap: 8px;
      padding: 12px;
      background: #0b0b0f;
      border-top: 1px solid rgba(255,255,255,0.08);
    }

    #aiw-input {
      flex: 1;
      border: 1px solid rgba(255,255,255,0.12);
      background: #15151b;
      color: white;
      border-radius: 999px;
      padding: 12px 14px;
      outline: none;
      font-size: 14px;
    }

    #aiw-input::placeholder {
      color: #777789;
    }

    #aiw-send {
      border: none;
      border-radius: 999px;
      background: linear-gradient(135deg,#7c3aed,#4f46e5);
      color: white;
      padding: 0 18px;
      font-weight: 900;
      cursor: pointer;
    }

    @media (max-width: 520px) {
      #aiw-box {
        right: 14px;
        left: 14px;
        width: auto;
        height: 72vh;
        bottom: 92px;
      }

      #aiw-btn {
        right: 18px;
        bottom: 18px;
      }
    }
  `;
  document.head.appendChild(css);

  const btn = document.createElement("button");
  btn.id = "aiw-btn";
  btn.innerHTML = "💬";

  const box = document.createElement("div");
  box.id = "aiw-box";
  box.innerHTML = `
    <div id="aiw-head">
      <div>
        <div id="aiw-title">AI Sales Assistant</div>
        <div id="aiw-status">Online now</div>
      </div>
      <button id="aiw-close">×</button>
    </div>

    <div id="aiw-messages"></div>

    <div id="aiw-actions">
      <button data-msg="What is your price list?">Price</button>
      <button data-msg="I want to book an appointment">Book</button>
      <button data-msg="I want to pay now">Pay</button>
    </div>

    <div id="aiw-input-row">
      <input id="aiw-input" placeholder="Type your message..." />
      <button id="aiw-send">→</button>
    </div>
  `;

  document.body.appendChild(btn);
  document.body.appendChild(box);

  const messages = box.querySelector("#aiw-messages");
  const input = box.querySelector("#aiw-input");

  function addMessage(text, type) {
    const div = document.createElement("div");
    div.className = "aiw-msg " + (type === "user" ? "aiw-user" : "aiw-bot");
    div.innerText = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  async function sendMessage(text) {
    if (!text || !text.trim()) return;

    addMessage(text, "user");

    const typing = document.createElement("div");
    typing.className = "aiw-msg aiw-bot";
    typing.innerText = "Typing...";
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;

    try {
      const res = await fetch(API, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: text,
          siteName: siteName,
          businessType: businessType,
          offer: offer,
          price: price,
          paymentLink: paymentLink
        })
      });

      const data = await res.json();

      typing.remove();
      addMessage(data.reply || "I can help with pricing, booking, or payment.", "bot");
    } catch (err) {
      typing.remove();
      addMessage("Connection error. Please try again.", "bot");
    }
  }

  btn.onclick = function () {
    box.style.display = box.style.display === "flex" ? "none" : "flex";
  };

  box.querySelector("#aiw-close").onclick = function () {
    box.style.display = "none";
  };

  box.querySelector("#aiw-send").onclick = function () {
    const text = input.value;
    input.value = "";
    sendMessage(text);
  };

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      const text = input.value;
      input.value = "";
      sendMessage(text);
    }
  });

  box.querySelectorAll("#aiw-actions button").forEach(function (button) {
    button.onclick = function () {
      sendMessage(button.getAttribute("data-msg"));
    };
  });

  addMessage("Hi! I can help you with pricing, booking, or payment.", "bot");
})();
