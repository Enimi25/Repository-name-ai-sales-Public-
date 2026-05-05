(function () {
  const API = "/chat";

  // === BUTTON (кружок) ===
  const button = document.createElement("div");
  button.style.position = "fixed";
  button.style.right = "20px";
  button.style.bottom = "20px";
  button.style.width = "60px";
  button.style.height = "60px";
  button.style.borderRadius = "50%";
  button.style.background = "linear-gradient(135deg,#7c3aed,#4f46e5)";
  button.style.display = "flex";
  button.style.alignItems = "center";
  button.style.justifyContent = "center";
  button.style.color = "white";
  button.style.fontSize = "24px";
  button.style.cursor = "pointer";
  button.style.zIndex = "9999";
  button.innerHTML = "💬";

  // === CHAT WINDOW ===
  const chat = document.createElement("div");
  chat.style.position = "fixed";
  chat.style.right = "20px";
  chat.style.bottom = "90px";
  chat.style.width = "320px";
  chat.style.height = "420px";
  chat.style.background = "#111";
  chat.style.borderRadius = "16px";
  chat.style.display = "none";
  chat.style.flexDirection = "column";
  chat.style.overflow = "hidden";
  chat.style.zIndex = "9999";

  chat.innerHTML = `
    <div style="padding:12px;background:#000;color:#fff;font-weight:bold;">
      AI Sales Assistant
    </div>

    <div id="w-messages" style="flex:1;padding:10px;overflow-y:auto;background:#1a1a1a;"></div>

    <div style="display:flex;gap:5px;padding:8px;background:#111;">
      <button class="w-btn">Price</button>
      <button class="w-btn">Book</button>
      <button class="w-btn">Pay</button>
    </div>

    <input id="w-input" placeholder="Type..."
      style="border:none;padding:10px;background:#222;color:#fff;">
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
    div.style.margin = "6px 0";
    div.style.padding = "8px 10px";
    div.style.borderRadius = "10px";
    div.style.maxWidth = "80%";

    if (type === "user") {
      div.style.background = "#4f46e5";
      div.style.marginLeft = "auto";
      div.style.color = "#fff";
    } else {
      div.style.background = "#333";
      div.style.color = "#ddd";
    }

    div.innerText = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  // === QUICK BUTTONS ===
  chat.querySelectorAll(".w-btn").forEach(btn => {
    btn.style.flex = "1";
    btn.style.padding = "6px";
    btn.style.background = "#222";
    btn.style.color = "#fff";
    btn.style.border = "none";
    btn.style.borderRadius = "6px";
    btn.style.cursor = "pointer";

    btn.onclick = () => {
      send(btn.innerText);
    };
  });

  // === SEND ===
  async function send(text) {
    add(text, "user");

    try {
      const res = await fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      const data = await res.json();
      add(data.reply, "bot");
    } catch (e) {
      add("Error connecting to server", "bot");
    }
  }

  // === INPUT ===
  chat.querySelector("#w-input").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      const text = e.target.value;
      e.target.value = "";
      send(text);
    }
  });

})();
