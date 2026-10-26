import threading
import time
import random
import math
from flask import Flask, jsonify
import cv2
import mediapipe as mp
import pyvirtualcam
from pyvirtualcam import PixelFormat
import numpy as np

HOST = "127.0.0.1"
PORT = 8765
WIDTH, HEIGHT, FPS = 640, 480, 30
CAMERA_INDEX = 0

app = Flask(__name__)

@app.after_request
def allow_extension_origin(response):
    origin = __import__("flask").request.headers.get("Origin", "")
    # Permit the extension popup to call the localhost companion, but not arbitrary websites.
    if origin.startswith("chrome-extension://"):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

state_lock = threading.Lock()
state = {"enabled": False, "running": False, "message": "Ready"}
worker = None
stop_event = threading.Event()

def get_state():
    with state_lock:
        return dict(state)

def set_state(**kwargs):
    with state_lock:
        state.update(kwargs)

@app.get("/status")
def status():
    return jsonify(get_state())

@app.post("/start")
def start():
    global worker
    if worker and worker.is_alive():
        set_state(enabled=True, message="Thanos mode enabled")
        return jsonify(get_state())
    stop_event.clear()
    set_state(enabled=True, running=True, message="Starting camera...")
    worker = threading.Thread(target=video_loop, daemon=True)
    worker.start()
    return jsonify(get_state())

@app.post("/stop")
def stop():
    stop_event.set()
    set_state(enabled=False, message="Thanos mode disabled")
    return jsonify(get_state())

def finger_up(lm, tip, pip):
    # In normalized image coordinates, a finger tip above its middle joint is usually extended.
    return lm[tip].y < lm[pip].y

def classify_hand(lm):
    # Heuristic classification; assumes palm faces the camera reasonably clearly.
    fingers = [
        finger_up(lm, 8, 6),   # index
        finger_up(lm, 12, 10), # middle
        finger_up(lm, 16, 14), # ring
        finger_up(lm, 20, 18), # pinky
    ]
    # Thumb-tip to index-tip distance, normalized by palm width.
    palm_width = max(0.03, math.hypot(lm[5].x - lm[17].x, lm[5].y - lm[17].y))
    pinch = math.hypot(lm[4].x - lm[8].x, lm[4].y - lm[8].y) / palm_width < 0.35
    if sum(fingers) >= 4:
        return "palm"
    if sum(fingers) <= 1:
        return "fist"
    if pinch:
        return "snap"
    return "other"

def make_particles(width, height, count=1700):
    particles = []
    for _ in range(count):
        particles.append({
            "x": random.uniform(0, width), "y": random.uniform(0, height),
            "vx": random.uniform(-3.8, 3.8), "vy": random.uniform(-4.2, 2.0),
            "r": random.randint(1, 4), "life": random.uniform(0.45, 1.0)
        })
    return particles

def dust_frame(frame, progress, particles):
    h, w = frame.shape[:2]
    # A fast, stylized purple dust dissolve: image fades while particles drift across it.
    out = cv2.convertScaleAbs(frame, alpha=max(0.0, 1.0 - progress * 1.25), beta=0)
    overlay = np.zeros_like(out)
    for p in particles:
        x = int(p["x"] + p["vx"] * progress * 26)
        y = int(p["y"] + p["vy"] * progress * 26)
        if 0 <= x < w and 0 <= y < h:
            radius = max(1, int(p["r"] * (1.0 + progress)))
            # BGR purple / violet glow approximation
            cv2.circle(overlay, (x, y), radius + 2, (130, 35, 95), -1, cv2.LINE_AA)
            cv2.circle(overlay, (x, y), radius, (220, 145, 255), -1, cv2.LINE_AA)
    return cv2.addWeighted(out, 1.0, overlay, 0.9, 0)

def video_loop():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    if not cap.isOpened():
        set_state(running=False, message="Could not open webcam. Check CAMERA_INDEX in companion.py.")
        return

    mp_hands = mp.solutions.hands
    particles = make_particles(WIDTH, HEIGHT)
    prev_gesture = "other"
    palm_armed = False
    effect_start = None
    cooldown_until = 0.0
    try:
        # OBS Virtual Camera should be started in OBS before running if backend cannot auto-connect.
        with mp_hands.Hands(
            static_image_mode=False, max_num_hands=1,
            model_complexity=0, min_detection_confidence=0.55,
            min_tracking_confidence=0.5
        ) as hands:
            with pyvirtualcam.Camera(width=WIDTH, height=HEIGHT, fps=FPS, fmt=PixelFormat.BGR) as virtual_cam:
                set_state(running=True, message="Running. Select OBS Virtual Camera in Google Meet.")
                while not stop_event.is_set():
                    ok, frame = cap.read()
                    if not ok:
                        time.sleep(0.02)
                        continue
                    frame = cv2.resize(frame, (WIDTH, HEIGHT))
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    result = hands.process(rgb)
                    gesture = "other"
                    if result.multi_hand_landmarks:
                        gesture = classify_hand(result.multi_hand_landmarks[0].landmark)

                    now = time.time()
                    if gesture == "palm":
                        palm_armed = True
                    trigger = palm_armed and (
                        (prev_gesture == "palm" and gesture in ("fist", "snap")) or
                        (gesture in ("fist", "snap") and prev_gesture == "palm")
                    )
                    if trigger and now >= cooldown_until:
                        effect_start = now
                        cooldown_until = now + 3.0
                        palm_armed = False
                        particles = make_particles(WIDTH, HEIGHT)
                    if gesture in ("fist", "snap") and palm_armed and prev_gesture not in ("palm",):
                        # Allows palm -> short transition even if one intermediate frame is missed.
                        if now >= cooldown_until:
                            effect_start = now
                            cooldown_until = now + 3.0
                            palm_armed = False
                            particles = make_particles(WIDTH, HEIGHT)

                    output = frame
                    if effect_start is not None:
                        progress = (now - effect_start) / 1.7
                        if progress <= 1.0:
                            output = dust_frame(frame, progress, particles)
                        else:
                            effect_start = None
                    # Small status indicator is intentionally not drawn into outgoing video.
                    virtual_cam.send(np.ascontiguousarray(output))
                    virtual_cam.sleep_until_next_frame()
                    prev_gesture = gesture
    except Exception as exc:
        set_state(running=False, message=f"Camera error: {exc}")
    finally:
        cap.release()
        set_state(running=False)

if __name__ == "__main__":
    print("Thanos Snap companion listening on http://127.0.0.1:8765")
    print("Keep this terminal open. Press Ctrl+C to exit.")
    app.run(host=HOST, port=PORT, debug=False, threaded=True)
