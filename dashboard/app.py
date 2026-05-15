# app.py
import os
os.environ["LIBCAMERA_LOG_LEVELS"] = "3"

from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO
from picamera2 import Picamera2
import paho.mqtt.client as mqtt
import threading
import json
import time
import cv2

# --- Flask Setup ---
app = Flask(__name__)
app.config["SECRET_KEY"] = "smartroom2026"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# --- Global sensor data ---
sensor_data = {
    "distance": 0,
    "motion": False,
    "temperature": 0,
    "humidity": 0
}

# --- Global camera frame ---
output_frame = None
frame_lock = threading.Lock()

# --- Camera Setup ---
print("Initialising camera...")
camera = Picamera2()
config = camera.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)
camera.configure(config)
camera.start()
time.sleep(1)
print("Camera ready!")

# --- Camera capture thread ---
def capture_frames():
    global output_frame
    while True:
        frame = camera.capture_array()
        frame = cv2.flip(frame, -1)
        _, buffer = cv2.imencode(
            ".jpg", frame,
            [cv2.IMWRITE_JPEG_QUALITY, 70]
        )
        with frame_lock:
            output_frame = buffer.tobytes()
        time.sleep(0.05)

# --- Camera stream generator ---
def generate_frames():
    global output_frame
    while True:
        with frame_lock:
            if output_frame is None:
                continue
            frame = output_frame
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n"
               + frame + b"\r\n")
        time.sleep(0.05)

# --- MQTT Setup ---
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Flask MQTT connected!")
        client.subscribe("smartroom/sensors")

def on_message(client, userdata, msg):
    global sensor_data
    try:
        data = json.loads(msg.payload.decode())
        sensor_data["distance"]    = data.get("distance", 0)
        sensor_data["motion"]      = bool(data.get("motion", 0))
        sensor_data["temperature"] = data.get("temperature", 0)
        sensor_data["humidity"]    = data.get("humidity", 0)
        print(f"Dashboard updated: {sensor_data}")
    except Exception as e:
        print(f"MQTT error: {e}")

def start_mqtt():
    time.sleep(5)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect("localhost", 1883, 60)
        client.loop_forever()
    except Exception as e:
        print(f"Flask MQTT error: {e}")

# --- Read alert log ---
def get_alerts():
    log_file = "/home/ajmalpro11/smart-room/logs/alerts.log"
    if not os.path.exists(log_file):
        return []
    with open(log_file, "r") as f:
        lines = f.readlines()
    return lines[-10:]

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/sensors")
def sensors():
    return jsonify(sensor_data)

@app.route("/alerts")
def alerts():
    return jsonify(get_alerts())

# --- Start threads ---
camera_thread = threading.Thread(target=capture_frames, daemon=True)
camera_thread.start()

mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
mqtt_thread.start()

if __name__ == "__main__":
    print("Starting Smart Room Dashboard...")
    print("Open http://192.168.1.101:5000 in your browser!")
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False,
        allow_unsafe_werkzeug=True
    )
