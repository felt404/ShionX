const chat = new WSClient("/ws/chat");
const voice = new WSClient("/ws/voice");
const recorder = new Recorder();

const modelStatus = document.getElementById("model-status");
const connectionStatus = document.getElementById("connection-status");
const messagesBox = document.getElementById("chat-messages");
const sendBtn = document.getElementById("send-btn");
const input = document.getElementById("text-input");
const modelSelect = document.getElementById("model-select");
const memoryContent = document.getElementById("memory-content");
const recordBtn = document.getElementById("record-btn");
const stopRecordBtn = document.getElementById("stop-record-btn");

function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.textContent = `${role}: ${text}`;
  messagesBox.appendChild(div);
  messagesBox.scrollTop = messagesBox.scrollHeight;
}

async function api(path, opts = {}) {
  const res = await fetch(path, { headers: { "Content-Type": "application/json" }, ...opts });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function initSockets() {
  const c = chat.connect();
  c.onopen = () => connectionStatus.classList.add("connected");
  c.onclose = () => connectionStatus.classList.remove("connected");

  chat.on("response_chunk", (msg) => addMessage("assistant", msg.payload));
  chat.on("error", (msg) => addMessage("assistant", `Error: ${msg.payload}`));

  voice.connect();
}

async function loadModels() {
  const data = await api("/api/models");
  modelStatus.textContent = data.current_model || "No model loaded";
  modelSelect.innerHTML = "";
  data.available_models.forEach((name) => {
    const opt = document.createElement("option");
    opt.value = name;
    opt.textContent = name;
    modelSelect.appendChild(opt);
  });
}

sendBtn.addEventListener("click", () => {
  const text = input.value.trim();
  if (!text) return;
  addMessage("user", text);
  chat.send("text", text);
  input.value = "";
});

document.getElementById("swap-model-btn").addEventListener("click", async () => {
  if (!modelSelect.value) return;
  await api("/api/models/swap", {
    method: "POST",
    body: JSON.stringify({ model_path: modelSelect.value }),
  });
  await loadModels();
});

document.getElementById("load-history-btn").addEventListener("click", async () => {
  const data = await api("/api/memories?query=history&limit=20");
  memoryContent.textContent = JSON.stringify(data, null, 2);
});

document.getElementById("load-context-btn").addEventListener("click", async () => {
  const data = await api("/api/memories?query=context");
  memoryContent.textContent = JSON.stringify(data, null, 2);
});

document.getElementById("load-notes-btn").addEventListener("click", async () => {
  const data = await api("/api/memories?query=notes");
  memoryContent.textContent = JSON.stringify(data, null, 2);
});

recordBtn.addEventListener("click", async () => {
  await recorder.start();
  document.getElementById("voice-status").textContent = "Recording...";
  recordBtn.disabled = true;
  stopRecordBtn.disabled = false;
});

stopRecordBtn.addEventListener("click", async () => {
  const buf = await recorder.stop();
  if (buf && voice.socket?.readyState === WebSocket.OPEN) {
    voice.socket.send(buf);
  }
  document.getElementById("voice-status").textContent = "Stopped";
  recordBtn.disabled = false;
  stopRecordBtn.disabled = true;
});

initSockets();
loadModels().catch((e) => {
  modelStatus.textContent = "Model API unavailable";
  console.warn(e);
});
