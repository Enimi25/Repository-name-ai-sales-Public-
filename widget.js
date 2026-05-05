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
    z-index:9999;
  ">
    <div style="background:#111;color:#fff;padding:12px">
      <b>AI Sales Assistant</b><br>
      <span style="font-size:12px;color:#7cffbd">Online now</span>
    </div>

    <div id="chat" style="padding:12px;height:260px;overflow:auto;background:#f5f5f7"></div>

    <div style="padding:10px;border-top:1px solid #eee">
      <input id="input" placeholder="Type..."
        style="width:68%;padding:8px;border-radius:8px;border:1px solid #ccc" />
      <button id="send"
        style="padding:8px 12px;background:#111;color:#fff;border:none;border-radius:8px">
        Send
      </button>
    </div>

    <div style="display:flex;gap:6px;padding:10px">
      <button class="quick" data-type="price">Price</button>
      <button class="quick" data-type="book">Book appointment</button>
      <button class="quick" data-type="pay">Pay now</button>
    </div>
  </div>
  `;

  document.body.appendChild(widget);

  const chat = widget.querySelector("#chat");
  const input = widget.querySelector("#input");
  const send = widget.querySelector("#send");

  function add(text, type) {
    const div = document.createElement("div");

    div.style.padding = "10px";
    div.style.marginBottom = "10px";
    div.style.borderRadius = "12px";
    div.style.maxWidth = "80%";
    div.style.fontSize = "14px";

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

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: text })
      });

      const data = await res.json();

      add(data.reply, "bot");
    } catch (e) {
      add("Server error. Try again.", "bot");
    }
  }

  send.onclick = () => {
    if (!input.value) return;
    sendMessage(input.value);
    input.value = "";
  };

  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      send.click();
    }
  });

  widget.querySelectorAll(".quick").forEach(btn => {
    btn.onclick = () => {
      const type = btn.getAttribute("data-type");

      if (type === "price") {
        sendMessage("What is your pricing?");
      }

      if (type === "book") {
        sendMessage("I want to book an appointment");
      }

      if (type === "pay") {
        sendMessage("I want to pay now");
      }
    };
  });

  // стартовое сообщение
  add("Hi! I can help you with pricing, booking or payment.", "bot");
})();
