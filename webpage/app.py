# webpage/app.py
# pip install flask-socketio eventlet python-socketio opencv-python
import os, base64, numpy as np, cv2
from pathlib import Path
from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit

ROOT = Path(__file__).resolve().parents[1]  # repo root
WEB  = ROOT / "webpage"
PH   = ROOT / "photos"

app = Flask(__name__, static_folder=str(ROOT), static_url_path="")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

@app.route("/")
def index():
    return send_from_directory(str(WEB), "index.html")

@app.route("/webpage/<path:filename>")
def serve_webpage(filename):
    return send_from_directory(str(WEB), filename)

@app.route("/photos/<path:filename>")
def serve_photos(filename):
    return send_from_directory(str(PH), filename)

def decode_dataurl(data_url:str):
    b64 = data_url.split(",", 1)[1] if "," in data_url else data_url
    buf = np.frombuffer(base64.b64decode(b64), np.uint8)
    return cv2.imdecode(buf, cv2.IMREAD_COLOR)

def run_model(frame_bgr):
    # stub you can replace with TF+dlib; returns (score, label)
    if frame_bgr is None: return 0.5, "relaxed"
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    m = float(np.mean(gray))
    if m > 150: return 0.9, "happy"
    if m < 70:  return 0.9, "sad"
    return 0.6, "neutral"

@socketio.on("start")
def on_start(_): emit("server_ready", {"ok": True})

@socketio.on("frame")
def on_frame(payload):
    frame = decode_dataurl(payload.get("image",""))
    score, label = run_model(frame)
    emit("expression", {"expression": label, "score": float(score)})
    return {"ok": True}  # ack

@socketio.on("stop")
def on_stop(): emit("stopped", {"ok": True})

if __name__ == "__main__":
    print("Serving on http://localhost:5000")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
