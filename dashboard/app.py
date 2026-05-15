# app.py
# Flask web dashboard for Smart Room Intelligence System
# Shows live camera feed, sensor readings and alert log

from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO
from picamera2 import Picamera2
from gpiozero import DistanceSensor, DigitalInputDevice
import adafruit_dht
import board
import threading
import time
import os
import cv2

# --- Suppress logs ---
os.environ["LIBCAMERA_LOG_LEVELS"] = "3"

# --- Flask Setup ---
app = Flask(__name__)
app.config["SECRET_KEY"] = "smartroom2026"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

# --- Sensor Setup ---
print("Initialising sensors...")
ultrasonic = DistanceSensor(echo=24, trigger=18, max_distance=4)
ir_sensor  = DigitalInputDevice(23, pull_up=True)
dht_sensor = adafruit_dht.DHT22(board.D17)
print("Sensors ready!")

# --- Camera Setup ---
camera = Picamera2()
config = camera.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)
camera.configure(config)
camera.start()
time.sleep(1)

# --- Global sensor data ---
sensor_data = {
    "distance": 0,
    "motion": False,
    "temperature": 0,
    "humidity": 0
}

# --- Camera stream generator ---
def generate_frames():
    while True:
        frame = camera.capture_array()
        # Flip image: 0=vertical, 1=horizontal, -1=both
        frame = cv2.flip(frame, -1)
        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n"
               + frame_bytes + b"\r\n")
        time.sleep(0.05)

# --- Sensor reading thread ---
def read_sensors():
    while True:
        try:
            sensor_data["distance"] = round(
                ultrasonic.distance * 100, 2)
            sensor_data["motion"] = not ir_sensor.value
            try:
                sensor_data["temperature"] = dht_sensor.temperature
                sensor_data["humidity"]    = dht_sensor.humidity
            except RuntimeError:
                pass
            socketio.emit("sensor_update", sensor_data)
        except Exception as e:
            print(f"Sensor error: {e}")
        time.sleep(2)

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

# --- Start sensor thread ---
sensor_thread = threading.Thread(target=read_sensors, daemon=True)
sensor_thread.start()

if __name__ == "__main__":
    print("Starting Smart Room Dashboard...")
    print("Open http://192.168.1.101:5000 in your browser!")
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=False,
        allow_unsafe_werkzeug=True
    )
