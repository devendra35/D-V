/* =========================================
   DΞV Portfolio — Frontend
   ========================================= */

if (typeof ScrollReveal !== "undefined") {
  ScrollReveal().reveal(".hero-left", {
    origin: "left",
    distance: "50px",
    duration: 1000,
    delay: 300
  });

  ScrollReveal().reveal(".hero-right", {
    origin: "right",
    distance: "50px",
    duration: 1000,
    delay: 500
  });

  ScrollReveal().reveal(".navbar", {
    origin: "top",
    distance: "20px",
    duration: 800,
    delay: 200
  });

  ScrollReveal().reveal(".about-img", {
    origin: "left",
    distance: "50px",
    duration: 1000,
    delay: 200
  });

  ScrollReveal().reveal(".about-content", {
    origin: "right",
    distance: "50px",
    duration: 1000,
    delay: 300
  });

  ScrollReveal().reveal(".contact-section", {
    origin: "bottom",
    distance: "60px",
    duration: 1000,
    delay: 300
  });
}

const DEV_API_URL =
  window.DEV_API_BASE_URL ||
  "http://127.0.0.1:8001";

async function askDEV(message) {
  const response = await fetch(`${DEV_API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: message
    })
  });

  if (!response.ok) {
    throw new Error(`DΞV API error: ${response.status}`);
  }

  return await response.json();
}

window.DEV = {
  ask: askDEV
};

console.log("DΞV API READY:", DEV_API_URL);

const devLauncher = document.getElementById("dev-launcher");
const devChat = document.getElementById("dev-chat");
const devClose = document.getElementById("dev-close");
const devInput = document.getElementById("dev-input");
const devChatForm = document.getElementById("dev-chat-form");
const devMessages = document.getElementById("dev-messages");

if (devLauncher && devChat) {
  devLauncher.onclick = () => {
    const isOpen = devChat.classList.toggle("open");

    devChat.setAttribute(
      "aria-hidden",
      String(!isOpen)
    );

    if (isOpen && devInput) {
      devInput.focus();
    }
  };
}

if (devClose && devChat) {
  devClose.onclick = () => {
    devChat.classList.remove("open");
    devChat.setAttribute("aria-hidden", "true");
  };
}

console.log("DΞV DOM CHECK:", {
  launcher: !!document.getElementById("dev-launcher"),
  chat: !!document.getElementById("dev-chat"),
  close: !!document.getElementById("dev-close")
});

/* =========================================
   DΞV Thinking Animation
   ========================================= */

function addDEVThinking() {
  if (!devMessages) {
    return null;
  }

  const message = document.createElement("div");

  message.className =
    "dev-message dev-message-ai dev-thinking-message";

  message.innerHTML = `
    <div class="dev-message-avatar">DΞV</div>

    <div class="dev-message-content dev-thinking">
      <span></span>
      <span></span>
      <span></span>
    </div>
  `;

  devMessages.appendChild(message);

  devMessages.scrollTop = devMessages.scrollHeight;

  return message;
}

function removeDEVThinking(message) {
  if (message && message.parentNode) {
    message.remove();
  }
}

/* =========================================
   Chat
   ========================================= */

if (devChatForm) {
  devChatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = devInput?.value.trim();

    if (!message) {
      return;
    }

    console.log("DΞV MESSAGE:", message);

    addDEVMessage(message, "user");

    if (devInput) {
      devInput.value = "";
      devInput.disabled = true;
    }

    const sendButton =
      devChatForm.querySelector("button[type='submit']");

    if (sendButton) {
      sendButton.disabled = true;
    }

    const thinkingMessage = addDEVThinking();

    try {
      const result = await window.DEV.ask(message);

      console.log("DΞV RESPONSE:", result);

      removeDEVThinking(thinkingMessage);

      addDEVMessage(result.response, "ai");
    } catch (error) {
      console.error("DΞV CHAT ERROR:", error);

      removeDEVThinking(thinkingMessage);

      addDEVMessage(
        "Sorry, DΞV is temporarily unavailable.",
        "ai"
      );
    } finally {
      if (devInput) {
        devInput.disabled = false;
        devInput.focus();
      }

      if (sendButton) {
        sendButton.disabled = false;
      }
    }
  });
}

/* =========================================
   Add Message
   ========================================= */

function addDEVMessage(content, type = "ai") {
  if (!devMessages) {
    return;
  }

  const message = document.createElement("div");

  message.className =
    type === "user"
      ? "dev-message dev-message-user"
      : "dev-message dev-message-ai";

  message.innerHTML = `
    ${
      type === "ai"
        ? '<div class="dev-message-avatar">DΞV</div>'
        : ""
    }

    <div class="dev-message-content">
      ${
        type === "ai" && typeof marked !== "undefined"
          ? marked.parse(content)
          : content
      }
    </div>
  `;

  devMessages.appendChild(message);

  devMessages.scrollTop = devMessages.scrollHeight;
}