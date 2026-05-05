(function () {
  const API = "/chat";

  // === BUTTON ===
  const button = document.createElement("div");
  button.style.position = "fixed";
  button.style.right = "24px";
  button.style.bottom = "24px";
  button.style.width = "64px";
  button.style.height = "64px";
  button.style.borderRadius = "50%";
  button.style.background = "linear-gradient(135deg,#7c3aed,#4f46e5)";
  button.style.display = "flex";
  button.style.alignItems = "center";
  button.style.justifyContent = "center";
  button.style.color = "white";
  button.style.fontSize = "26px";
  button.style.cursor = "pointer";
  button.style.zIndex = "9999";
  button.style.boxShadow = "0 10px 40px rgba(124,58,237,0.6)";
  button.innerHTML = "💬";

  // === CHAT WINDOW ===
  const chat = document.createElement("div");
  chat.style.position = "fixed";
  chat.style.right = "24px";
  chat.style.bottom = "100px";
  chat.style.width = "360px";
  chat.style.height = "520px";
  chat.style.background = "#0b0b0f";
  chat.style.borderRadius = "24px";
  chat.style.display = "none";
  chat.style.flexDirection = "column";
  chat.style.overflow = "hidden";
  chat.style.zIndex = "9999";
  chat.style.border = "1px solid rgba(255,255,255,0.08)";
  chat.style.boxShadow = "0 40px 120px rgba(0,0,0,0.8)";

  chat.innerHTML = `
    <div style="padding:18px;background:#0b0b0f;border-bottom:1px solid rgba(255,255,255,0.08);">
      <div style="font-weight:700;color:#fff;">AI Sales Assistant</div>
      <div style="font-size:12px;color:#7cffbd;">Online now</div>
    </div>

    <div id="w-messages" style="flex:1;padding:14px;overflow-y:auto;"></div>

    <div style="display:flex;gap:6px;padding:12px;border-top:1px solid rgba(255,255,255,0.06);">
      <button class="w-btn">Price</button>
      <button class="w-btn">Book</button>
      <button class="w-btn">Pay</button>
    </div>

    <div style="display:flex;border-top:1px solid rgba(255,255,255,0.06);">
      <input id="w-input" placeholder="Type..."
        style="flex:1;border:none;padding:14px;background:#111;color:#fff;outline:none;">
      <button id="sendBtn" style="padding:14px 16px;background:#7c3aed;border:none;color:#fff;cursor:pointer;">→</button>
    </div>
  `;

  document.body.appendChild(button);
  document.body.appendChild(chat);

  // === TOGGLE ===
  button.onclick = () => {
    chat.style.display = chat.style.display === "flex" ? "none" : "flex";
  };

  const messages = chat.querySelector("#w-messages");

  function add(text, type) {
    const div = document.createElement("div");
    div.style.margin = "10px 0";
    div.style.padding = "12px 14px";
    div.style.borderRadius = "14px";
    div.style.maxWidth = "80%";
    div.style.fontSize = "14px";
    div.style.lineHeight = "1.4";

    if (type === "user") {
      div.style.background = "linear-gradient(135deg,#7c3aed,#4f46e5)";
      div.style.marginLeft = "auto";
      div.style.color = "#fff";
    } else {
      div.style.background = "#16161f";
      div.style.color = "#cfcfe3";
    }

    div.innerText = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  // === QUICK BUTTONS ===
  chat.querySelectorAll(".w-btn").forEach(btn => {
    btn.style.flex = "1";
    btn.style.padding = "8px";
    btn.style.background = "#111";
    btn.style.color = "#fff";
    btn.style.border = "1px solid rgba(255,255,255,0.1)";
    btn.style.borderRadius = "999px";
    btn.style.cursor = "pointer";
    btn.style.fontSize = "12px";

    btn.onclick = () => send(btn.innerText);
  });

  async function send(text) {
    add(text, "user");

    try {
      const res = await fetch(API, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: text })
      });

      const data = await res.json();
      add(data.reply, "bot");
    } catch {
      add("Server error", "bot");
    }
  }

  // === INPUT ===
  const input = chat.querySelector("#w-input");
  const sendBtn = chat.querySelector("#sendBtn");

  input.addEventListener("keypress", e => {
    if (e.key === "Enter") {
      const text = input.value;
      input.value = "";
      send(text);
    }
  });

  sendBtn.onclick = () => {
    const text = input.value;
    input.value = "";
    send(text);
  };

})();
