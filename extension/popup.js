const statusEl = document.getElementById("status");
const errorEl = document.getElementById("error");
const connectBtn = document.getElementById("connect");
const stopBtn = document.getElementById("stop");
const BASE = "http://127.0.0.1:8765";

async function request(path, method = "GET") {
  const response = await fetch(`${BASE}${path}`, { method });
  if (!response.ok) throw new Error(`Companion returned HTTP ${response.status}`);
  return response.json();
}
function showStatus(data) {
  statusEl.textContent = data.message || (data.enabled ? "Enabled" : "Disabled");
}
async function refresh() {
  try {
    errorEl.textContent = "";
    showStatus(await request("/status"));
  } catch (err) {
    statusEl.textContent = "Companion app is not running";
    errorEl.textContent = "Start companion.py first. " + err.message;
  }
}
connectBtn.addEventListener("click", async () => {
  try {
    errorEl.textContent = "";
    showStatus(await request("/start", "POST"));
  } catch (err) {
    errorEl.textContent = "Could not connect. Start companion.py first. " + err.message;
  }
});
stopBtn.addEventListener("click", async () => {
  try {
    errorEl.textContent = "";
    showStatus(await request("/stop", "POST"));
  } catch (err) {
    errorEl.textContent = err.message;
  }
});
refresh();
