// -------------------- Expression config --------------------
const EXPRESSIONS = ["sad","happy","confused","mad","freaky","relaxed","shocked"];

// Normalize backend labels -> your 7 buckets
const LABEL_MAP = {
  sad:"sad", happy:"happy", confused:"confused",
  angry:"mad", mad:"mad",
  disgust:"freaky", disgusted:"freaky", fear:"freaky", scared:"freaky",
  neutral:"relaxed", relaxed:"relaxed",
  surprised:"shocked", shock:"shocked", shocked:"shocked"
};

// Default monkey images (your folders)
const MONKEY = {
  sad:      "/photos/default-monkey/monkey-sad.png",
  happy:    "/photos/default-monkey/monkeyhappy.png",
  confused: "/photos/default-monkey/monkey-thinking.png",
  mad:      "/photos/default-monkey/monkeymad.png",
  freaky:   "/photos/default-monkey/monkey-freaky.png",
  relaxed:  "/photos/default-monkey/relaxed.png",
  shocked:  "/photos/default-monkey/monkey-bruh.gif",
};
const DEFAULT_MONKEY = "/photos/default-monkey/monkey-bruh.gif";

// Optional presets (Shrek set)
const PRESETS = {
  sad:      ["/photos/shrek-default/shrek-sad.png"],
  happy:    ["/photos/shrek-default/shrek-happy.png"],
  confused: ["/photos/shrek-default/shrek-confused.png"],
  mad:      ["/photos/shrek-default/shrek-mad.png"],
  freaky:   ["/photos/shrek-default/shrek-rizzing.png"],
  relaxed:  ["/photos/shrek-default/shrek-relaxed.png"],
  shocked:  ["/photos/shrek-default/shrek-bruh.png"],
};

// -------------------- LocalStorage helpers --------------------
const PRESET_NONE = -1;
const UPLOAD_KEY = n => `expr_upload_${n}`;
const PRESET_KEY = n => `expr_preset_${n}`;

const getUpload     = n => localStorage.getItem(UPLOAD_KEY(n));
const setUpload     = (n,d) => localStorage.setItem(UPLOAD_KEY(n), d);
const clearUpload   = n => localStorage.removeItem(UPLOAD_KEY(n));

// IMPORTANT FIX: treat null/""/"-1" as NO PRESET
function getPresetIndex(n){
  const s = localStorage.getItem(PRESET_KEY(n));
  if (s === null || s === "" || s === "-1") return PRESET_NONE;
  const i = parseInt(s, 10);
  return Number.isNaN(i) ? PRESET_NONE : i;
}
function setPresetIndex(n, i){
  localStorage.setItem(PRESET_KEY(n), String(i));
}
function clearPreset(n){
  localStorage.setItem(PRESET_KEY(n), String(PRESET_NONE)); // store -1 explicitly
}

// Resolve final image: upload > preset > monkey
function imageFor(name){
  const up = getUpload(name); if (up) return up;
  const idx = getPresetIndex(name);
  if (idx >= 0 && PRESETS[name]?.[idx]) return PRESETS[name][idx];
  return MONKEY[name] || DEFAULT_MONKEY;
}

// -------------------- Build Customizer (Guidelines) --------------------
function buildCustomizer(){
  const grid = document.getElementById("customizerGrid");
  if (!grid) return;
  grid.innerHTML = "";

  EXPRESSIONS.forEach(name=>{
    const card = document.createElement("div"); card.className = "custom-card";
    const title = document.createElement("h4"); title.textContent = name[0].toUpperCase()+name.slice(1);

    const preview = document.createElement("img");
    preview.className = "preview";
    preview.alt = `preview ${name}`;
    preview.src = imageFor(name);

    const row = document.createElement("div"); row.className = "row";

    const select = document.createElement("select");
    select.add(new Option("Default (Monkey)", String(PRESET_NONE)));
    (PRESETS[name]||[]).forEach((url,i)=> select.add(new Option(`Preset ${i+1}`, String(i))));
    select.value = String(getPresetIndex(name));
    select.addEventListener("change", ()=>{
      const idx = parseInt(select.value, 10);
      if (Number.isInteger(idx) && idx >= 0) setPresetIndex(name, idx);
      else setPresetIndex(name, PRESET_NONE);      // <- store -1, not remove
      if (!getUpload(name)) preview.src = imageFor(name);
    });

    const upload = document.createElement("input");
    upload.type = "file"; upload.accept = "image/*";
    upload.addEventListener("change", ()=>{
      const f = upload.files?.[0]; if (!f) return;
      const r = new FileReader();
      r.onload = ()=>{ setUpload(name, r.result); preview.src = r.result; };
      r.readAsDataURL(f);
    });

    const clearBtn = document.createElement("button");
    clearBtn.className="icon";
    clearBtn.textContent="Clear upload";
    clearBtn.title = "Remove your upload so preset/default applies";
    clearBtn.addEventListener("click", ()=>{
      clearUpload(name);
      preview.src = imageFor(name);               // now correctly falls to Monkey
    });

    row.append(select, upload, clearBtn);
    card.append(title, preview, row);
    grid.appendChild(card);
  });

  document.getElementById("resetBtn")?.addEventListener("click", ()=>{
    // You can now cancel this (OK/Cancel) properly
    if (!confirm("Reset all expressions to Default (Monkey)?")) return;
    EXPRESSIONS.forEach(n=>{
      clearUpload(n);
      clearPreset(n);                              // sets -1
    });
    buildCustomizer();                             // rebuild previews = monkeys
  });
}

// -------------------- Camera + Socket.IO --------------------
const startBtn = document.getElementById("startBtn");
const stopBtn  = document.getElementById("stopBtn");
const guidelinesCard = document.getElementById("guidelinesCard");

const videoEl  = document.getElementById("camera");
const canvas   = document.getElementById("offscreen");
const ctx      = canvas.getContext("2d");
const expressionImage = document.getElementById("expressionImage");
const expressionLabel = document.getElementById("expressionLabel");

const W = 320, H = 240;
let sending = false, stream = null;

const socket = io(); // same-origin

function fadeOutGuidelines(){
  guidelinesCard?.classList.add("fade-out");
  document.getElementById("app")?.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function startCamera(){
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 } }, audio: false});
    videoEl.srcObject = stream;
    await videoEl.play();
    canvas.width = W; canvas.height = H;
    sending = true;
    socket.emit("start", { ts: Date.now() });
    sendFrameLoop();
  } catch (e) {
    console.error(e);
    alert("We couldn't access your camera. Please allow camera permissions and try again.");
  }
}

function sendFrameLoop(){
  if (!sending) return;
  if (videoEl.readyState >= 2) {
    ctx.drawImage(videoEl, 0, 0, W, H);
    const jpeg = canvas.toDataURL("image/jpeg", 0.65);
    socket.emit("frame", { image: jpeg }, () => setTimeout(sendFrameLoop, 200)); // ~5 fps
  } else {
    requestAnimationFrame(sendFrameLoop);
  }
}

function stopEverything(){
  sending = false;
  socket.emit("stop", {});
  if (stream){ stream.getTracks().forEach(t=>t.stop()); stream=null; }
  videoEl.srcObject = null;
}

socket.on("expression", ({ expression, score })=>{
  const raw = (expression||"").toLowerCase().trim();
  const key = LABEL_MAP[raw] || "relaxed";
  expressionImage.src = imageFor(key);
  expressionLabel.textContent = `${key[0].toUpperCase()+key.slice(1)}${Number.isFinite(score)?` (${Number(score).toFixed(2)})`:''}`;
});

startBtn?.addEventListener("click", async ()=>{
  fadeOutGuidelines();
  await startCamera();
});
stopBtn?.addEventListener("click", stopEverything);

document.addEventListener("DOMContentLoaded", ()=>{
  buildCustomizer();
  if (expressionImage && !expressionImage.src) expressionImage.src = DEFAULT_MONKEY;
});
