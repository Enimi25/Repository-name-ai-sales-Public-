(function () {
  const widget = document.createElement("div");

  widget.innerHTML = `
  <div style="
    position:fixed;
    bottom:20px;
    right:20px;
    width:320px;
    background:#fff;
    border-radius:20px;
    overflow:hidden;
    box-shadow:0 20px 60px rgba(0,0,0,0.4);
    font-family:sans-serif;
  ">
    <div style="background:#111;color:#fff;padding:12px">
      <b>AI Sales Assistant</b><br>
      <span style="font-size:12px;color:#7cffbd">Online now</span>
    </div>

    <div id="chat" style="padding:12px;height:260px;overflow:auto;background:#f5f5f7"></div>

    <div style="padding:10px;border-top:1px solid #eee">
      <input id="input" placeholder="Type..."
        style="width:70%;padding:8px;border-radius:8px;border:1px solid #ccc" />
      <button id="send" style="padding:8px 12px;background:#111;color:#fff;border:none;border-radius:8px">
        Send
      </button>
    </div>

    <div style="display:flex;gap:6px;padding:10px">
      <button class="quick" data="price">Price</button>
      <button class="quick" data="book">Book</button>
      <button class="quick" data="pay">Pay</button>
    </div>
  </div>
  `;

  document.body.appendChild(widget);

  const chat = widget.querySelector("#chat");
  const input = widget.querySelector("#input");
  const send = widget.querySelector("#send");

  function add(text, type) {
    const div = document.createElement("div");
    div.style.padding = "8px";
    div.style.marginBottom = "8px";
    div.style.borderRadius = "10px";
    div.style.maxWidth = "80%";

    if (type === "user") {
      div.style.background = "#111";
      div.style.color = "#fff";
      div.style.marginLeft = "auto";
    } else {
      div.style.background = "#fff";
    }

    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
  }

  async function sendMessage(text) {
    add(text, "user");

    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    add(data.reply, "bot");
  }

  send.onclick = () => {
    if (!input.value) return;
    sendMessage(input.value);
    input.value = "";
  };

  widget.querySelectorAll(".quick").forEach(btn => {
    btn.onclick = () => sendMessage(btn.getAttribute("data"));
  });

  add("Hi! I can help you with pricing, booking or payment.", "bot");
})();
