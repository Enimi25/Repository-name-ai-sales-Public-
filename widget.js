(function () {
  if (window.AISalesAssistantLoaded) return;
  window.AISalesAssistantLoaded = true;

  const API_BASE = "https://repository-name-ai-sales-public.onrender.com";

  const style = document.createElement("style");
  style.innerHTML = `
    #ai-sales-widget-button {
      position: fixed;
      right: 24px;
      bottom: 24px;
      width: 64px;
      height: 64px;
      border-radius: 50%;
      border: none;
      background: #111;
      color: white;
      font-size: 26px;
      cursor: pointer;
      z-index: 999999;
    }

    #ai-sales-widget {
      position: fixed;
      right: 24px;
      bottom: 100px;
      width: 360px;
      height: 520px;
      background: #fff;
      border-radius: 22px;
      overflow: hidden;
      display: none;
      flex-direction: column;
      z-index: 999999;
    }

    #ai-sales-header {
      background: #111;
      color: white;
      padding: 16px;
      display: flex;
      justify-content: space-between;
    }

    #ai-sales-messages {
      flex: 1;
      padding: 12px;
      overflow-y: auto;
      background: #f5f5f7;
    }

    .msg {
      padding: 10px;
      border-radius: 12px;
      margin-bottom: 10px;
      max-width: 80%;
    }

    .bot { background: white; }
    .user { background: #111; color: white; margin-left: auto; }

    #ai-sales-input-area {
      display: flex;
      padding: 10px;
      border-top: 1px solid #eee;
    }

    #ai-sales-input {
      flex: 1;
      padding: 10px;
      border-radius: 999px;
      border: 1px solid #ddd;
    }

    #ai-sales-send {
      margin-left: 8px;
      padding: 10px 16px;
      border-radius: 999px;
      border: none;
      background: #111;
      color: white;
      cursor: pointer;
    }

    #ai-sales-actions {
      display: flex;
      gap: 6px;
      padding: 10px;
      border-top: 1px solid #eee;
      background: white;
    }

    #ai-sales-actions button {
      flex: 1;
      border-radius: 999px;
      border: 1px solid #111;
      padding: 6px;
      font-size: 12px;
      cursor: pointer;
      background: white;
    }
  `;
  document.head.appendChild(style);

  const button = document.createElement("button");
  button.id = "ai-sales-widget-button";
  button.innerHTML = "💬";

  const widget = document.createElement("div");
  widget.id = "ai-sales-widget";
  widget.innerHTML = `
    <div id="ai-sales-header">
      <div>AI Sales Assistant</div>
      <div id="ai-sales-close">×</div>
    </div>
    <div id="ai-sales-messages"></div>

    <div id="ai-sales-actions">
      <button data-msg="price">Price list</button>
      <button data-msg="book">Book appointment</button>
      <button data-msg="how">How it works</button>
    </div>

    <div id="ai-sales-input-area">
      <input id="ai-sales-input" placeholder="Type..." />
      <button id="ai-sales-send">Send</button>
    </div>
  `;

  document.body.appendChild(button);
  document.body.appendChild(widget);

  const messages = widget.querySelector("#ai-sales-messages");

  function add(text, cls) {
    const div = document.createElement("div");
    div.className = "msg " + cls;
    div.innerText = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  async function sendMessage(text) {
    add(text, "user");

    const res = await fetch(API_BASE + "/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    add(data.reply, "bot");
  }

  button.onclick = () => {
    widget.style.display = "flex";
  };

  widget.querySelector("#ai-sales-close").onclick = () => {
    widget.style.display = "none";
  };

  widget.querySelector("#ai-sales-send").onclick = () => {
    const input = widget.querySelector("#ai-sales-input");
    if (!input.value) return;
    sendMessage(input.value);
    input.value = "";
  };

  widget.querySelectorAll("#ai-sales-actions button").forEach(btn => {
    btn.onclick = () => sendMessage(btn.dataset.msg);
  });

  add("Hi! I can help you with pricing, booking or payments.", "bot");
})();
