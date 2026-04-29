const BACKEND = "";

const micBtn = document.getElementById("micBtn");
const replyEl = document.getElementById("reply");
const statusEl = document.getElementById("status");
const avatar = document.getElementById("avatar");

if (!window.SpeechRecognition && !window.webkitSpeechRecognition) {
  statusEl.textContent = "Sorry — Web Speech API is not supported. Please use Google Chrome.";
  micBtn.disabled = true;
  throw new Error("SpeechRecognition not available");
}

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.interimResults = false;
recognition.maxAlternatives = 1;

function setStatus(text) {
  statusEl.textContent = text;
}

function setBusy(busy) {
  micBtn.disabled = busy;
}

micBtn.addEventListener("click", () => {
  recognition.start();
  setStatus("Listening...");
  setBusy(true);
});

recognition.addEventListener("result", async (event) => {
  const transcript = event.results[0][0].transcript;
  setStatus("Thinking...");

  let reply;
  try {
    const chatRes = await fetch(`${BACKEND}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: transcript }),
    });
    const chatData = await chatRes.json();
    reply = chatData.reply;
  } catch {
    replyEl.textContent = "I'm afraid I couldn't reach my thinking facilities. Please try again.";
    setStatus("Error — backend unreachable");
    setBusy(false);
    return;
  }

  replyEl.textContent = reply;
  setStatus("Speaking...");
  avatar.classList.add("speaking");

  try {
    const speakRes = await fetch(`${BACKEND}/speak`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: reply }),
    });
    const audioBlob = await speakRes.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);

    audio.addEventListener("ended", () => {
      avatar.classList.remove("speaking");
      setStatus("Ready");
      setBusy(false);
      URL.revokeObjectURL(audioUrl);
    });

    audio.play();
  } catch {
    avatar.classList.remove("speaking");
    setStatus("Ready");
    setBusy(false);
  }
});

recognition.addEventListener("error", (event) => {
  setStatus(`Microphone error: ${event.error}`);
  setBusy(false);
});

document.getElementById("clearBtn").addEventListener("click", async () => {
  await fetch(`${BACKEND}/clear`, { method: "POST" });
  replyEl.textContent = "Good day. How may I be of service?";
  setStatus("Memory cleared");
  setTimeout(() => setStatus("Ready"), 2000);
});

recognition.addEventListener("end", () => {
  if (statusEl.textContent === "Listening...") {
    setStatus("Ready");
    setBusy(false);
  }
});
