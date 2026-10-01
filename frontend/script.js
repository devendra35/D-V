/* =========================================
   DΞV Portfolio — Frontend
   ========================================= */

/* -----------------------------------------
   Existing ScrollReveal animations
   ----------------------------------------- */

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


/* -----------------------------------------
   DΞV API configuration
   ----------------------------------------- */

const DEV_API_URL = "http://127.0.0.1:8001";


/* -----------------------------------------
   DΞV Chat API helper
   ----------------------------------------- */

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


/* -----------------------------------------
   Expose DΞV API
   ----------------------------------------- */

window.DEV = {
  ask: askDEV
};

console.log("DΞV API READY");



/* -----------------------------------------
   DΞV Chat UI
   ----------------------------------------- */

const devLauncher = document.getElementById("dev-launcher");
const devChat = document.getElementById("dev-chat");
const devClose = document.getElementById("dev-close");
const devInput = document.getElementById("dev-input");

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

const devChatForm = document.getElementById("dev-chat-form");

/* -----------------------------------------
   DΞV Chat API Connection
   ----------------------------------------- */

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
    }

    try {
      const result = await window.DEV.ask(message);

      console.log("DΞV RESPONSE:", result);

      addDEVMessage(result.response, "ai");
    } catch (error) {
      console.error("DΞV CHAT ERROR:", error);
    }
  });
}



/* -----------------------------------------
   DΞV Message Rendering
   ----------------------------------------- */

const devMessages = document.getElementById("dev-messages");

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


