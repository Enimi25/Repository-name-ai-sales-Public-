(function () {

  const API = "/chat";

  // === КНОПКА (кружок) ===
  const button = document.createElement("div");
  button.innerHTML = "💬";
  button.style.position = "fixed";
  button.style.bottom = "20px";
  button.style.right = "20px";
  button.style.width = "60px";
  button.style.height = "60px";
  button.style.borderRadius = "50%";
  button.style.background = "linear-gradient(135deg,#6d28d9,#9333ea)";
  button.style.display = "flex";
  button.style.alignItems = "center";
  button.style.justifyContent = "center";
  button.style.cursor = "pointer";
  button.style.fontSize = "24px";
  button.style.zIndex = "9999";
  document.body.appendChild(button);

  // === ЧАТ ===
  const chat = document.createElement("div");
  chat.style.position = "fixed";
  chat.style.bottom = "90px";
  chat.style.right = "20px";
  chat.style.width = "320px";
  chat.style.height = "420px";
  chat.style.background = "#111";
  chat.style.borderRadius = "16px";
  chat.style.display = "none";
  chat.style.flexDirection = "column";
  chat.style.zIndex = "9999";
  chat.style.boxShadow = "0 10px 40px rgba(0,0,0,0.5)";
  document.body.appendChild(chat);

  // === HEADER ===
  const header = document.createElement("div");
  header.innerHTML = "AI Assistant";
  header.style.padding = "12px";
  header.style.color = "white";
  header.style.borderBottom = "1px solid #222";
  chat.appendChild(header);

  // === MESSAGES ===
  const messages = document.createElement("div");
  messages.style.flex = "1";
  messages.style.padding = "10px";
  messages.style.overflowY = "auto";
  chat.appendChild(messages);

  function add(text, type) {
    const msg = document.createElement("div");
    msg.innerText = text;
    msg.style.margin = "6px 0";
    msg.style.color = type === "user" ? "white" : "#aaa";
    msg.style.textAlign = type === "user" ? "right" : "left";
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
  }

  // === INPUT ===
  const input = document.createElement("input");
  input.placeholder = "Type...";
  input.style.border = "none";
  input.style.padding = "10px";
  input.style.background = "#222";
  input.style.color = "white";
  input.style.outline = "none";
  chat.appendChild(input);

  input.addEventListener("keypress", async (e) => {
    if (e.key === "Enter") {
      const text = input.value;
      add(text, "user");
      input.value = "";

      const res = await fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      const data = await res.json();
      add(data.reply, "bot");
    }
  });

  // === OPEN / CLOSE ===
  button.onclick = () => {
    chat.style.display = chat.style.display === "flex" ? "none" : "flex";
  };

})();
