# 🏠 Smart Room Intelligence System

> A fully local, edge-based IoT security and monitoring system built on Raspberry Pi 5.
> No cloud. No subscription. Just hardware, Python, and open source tools.

![Dashboard](photos/27_flask_dashboard.PNG)

---

## 📌 Project Overview

This system combines multiple sensors to detect intrusions, monitor environment,
and serve a live web dashboard — all running locally on a Raspberry Pi 5.

When motion is detected and an object is within range:
- 📸 Camera captures a timestamped photo
- 🔊 Buzzer sounds an alert
- 📝 Event is logged with temperature and humidity
- 📊 All data streams to a live Grafana dashboard
- 🌐 Live camera feed visible from any device on WiFi

---

## 🛠️ Built With

| Tool | Purpose |
|---|---|
| Raspberry Pi 5 | Edge computing platform |
| Python 3.13 | Core programming language |
| gpiozero | GPIO sensor control |
| Picamera2 | Camera capture |
| Mosquitto MQTT | IoT messaging broker |
| InfluxDB | Time-series data storage |
| Grafana | Live data visualization |
| Flask + SocketIO | Web dashboard |
| Docker | Container orchestration |
| OpenCV | Image processing |

---

## 📡 Sensors Used

| Sensor | GPIO Pins | Purpose |
|---|---|---|
| HC-SR04 Ultrasonic | TRIG:18 ECHO:24 | Distance detection |
| IR Obstacle Sensor | GPIO 23 | Motion detection |
| DHT22 | GPIO 17 | Temperature & humidity |
| MPU-6050 | I2C (SDA/SCL) | Vibration detection (pending) |
| Pi Camera Module 3 | CSI CAM0 | Image capture & live feed |
| Passive Buzzer | GPIO 25 | Audio alerts |

---

## 🗺️ System Architecture

```
HC-SR04 + IR + DHT22 + Camera + Buzzer
                 ↓
        Python Sensor Layer
                 ↓
        MQTT Broker (Mosquitto)
                 ↓
        Decision Engine (Python)
        if motion AND distance < 150cm:
            → capture photo
            → sound buzzer
            → log alert
                 ↓
        ┌────────┴────────┐
        ↓                 ↓
   InfluxDB          Flask Web App
        ↓                 ↓
   Grafana          Live Camera Feed
   Dashboard        + Sensor Status
                    + Alert Log
```

---

## 📸 Development Progress

### Phase 1 — Environment Setup

| Step | Screenshot |
|---|---|
| System updated | ![](photos/00_system_updated.PNG) |
| I2C scan (empty) | ![](photos/01_i2c_empty_scan.png) |
| Virtual environment | ![](photos/02_virtualenv_active.png) |
| Project structure | ![](photos/03_project_structure.png) |
| All imports OK | ![](photos/04_all_imports_ok.png) |
| First Git commit | ![](photos/05_first_git_commit.png) |
| GitHub live | ![](photos/06_github_live.png) |

### Phase 1 — Sensor Setup

| Sensor | Wiring | Live Readings |
|---|---|---|
| Ultrasonic | ![](photos/09_ultrasonic_wiring.jpg.jpeg) | ![](photos/10_ultrasonic_readings.png) |
| IR Sensor | ![](photos/11_ir_sensor_wiring.jpg.jpeg) | ![](photos/12_ir_sensor_readings.png) |
| Camera | — | ![](photos/13_camera_working.png) |
| DHT22 | ![](photos/14_dht22_wiring.jpg) | ![](photos/15_dht22_readings.png) |
| Full wiring | ![](photos/17_full_wiring.jpeg) | — |

### Phase 2 — Decision Engine

| Screenshot | Description |
|---|---|
| ![](photos/18_decision_engine_working.png) | Multi-sensor fusion triggering alerts |
| ![](photos/19_intruder_captured.jpg) | Auto-captured intruder photo |

### Phase 3 — IoT Pipeline

| Screenshot | Description |
|---|---|
| ![](photos/20_docker_working.png) | Docker installed and running |
| ![](photos/23_mqtt_publishing.PNG) | MQTT publisher streaming sensor data |
| ![](photos/24_mqtt_pipeline.PNG) | Full pipeline — publisher and subscriber |
| ![](photos/22_influxdb_connected.PNG) | InfluxDB connected to Grafana |
| ![](photos/25_grafana_temperature.PNG) | Live temperature chart |
| ![](photos/26_grafana_full_dashboard.PNG) | Full 4-panel Grafana dashboard |

### Phase 4 — Web Dashboard

![Flask Dashboard](photos/27_flask_dashboard.PNG)

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/ajmalpro11/smart-room-intelligence.git
cd smart-room-intelligence
```

### 2. Create virtual environment
```bash
python3 -m venv venv --system-site-packages
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Docker stack
```bash
docker compose up -d
```

### 5. Run MQTT publisher
```bash
python3 mqtt/publisher.py
```

### 6. Run MQTT subscriber
```bash
python3 mqtt/subscriber.py
```

### 7. Run web dashboard
```bash
python3 dashboard/app.py
```

Open `http://YOUR_PI_IP:5000` in any browser on your WiFi.

### 8. Run decision engine (intruder detection)
```bash
python3 processor/decision_engine.py
```

---

## 📁 Project Structure

```
smart-room/
├── sensors/
│   ├── ultrasonic.py      ← HC-SR04 distance sensor
│   ├── ir_sensor.py       ← IR motion detection
│   ├── dht22.py           ← Temperature & humidity
│   ├── mpu6050.py         ← Vibration (pending soldering)
│   └── camera.py          ← Pi Camera Module 3
├── mqtt/
│   ├── publisher.py       ← Reads sensors, sends to MQTT
│   └── subscriber.py      ← Receives MQTT, stores in InfluxDB
├── processor/
│   └── decision_engine.py ← Multi-sensor fusion + alerts
├── dashboard/
│   ├── app.py             ← Flask web server
│   └── templates/
│       └── index.html     ← Web dashboard UI
├── mosquitto/config/      ← MQTT broker config
├── influxdb/              ← Time-series database
├── grafana/               ← Dashboard config
├── photos/                ← Development screenshots
├── logs/                  ← Alert logs
├── docker-compose.yml     ← Full stack orchestration
├── requirements.txt       ← Python dependencies
└── README.md
```

---

## 📅 Project Phases

- [x] Phase 1 — Environment setup & sensor integration
- [x] Phase 2 — Multi-sensor decision engine
- [x] Phase 3 — MQTT + InfluxDB + Grafana pipeline
- [x] Phase 4 — Flask web dashboard with live camera
- [ ] Phase 5 — ML anomaly detection (coming soon)
- [ ] Phase 6 — MPU-6050 vibration sensor (pending soldering)

---
## 🔑 Credentials Setup

Copy the example env file and fill in your values:
```bash
cp .env.example .env
nano .env
```

> ⚠️ Never commit your `.env` file — it's already in `.gitignore`
---

## 👨‍💻 Author

**Ajumal Shamsudeen** — TH Rosenheim, Germany

[![GitHub](https://img.shields.io/badge/GitHub-ajmalpro11-black?logo=github)](https://github.com/ajmalpro11)

---

## 📄 License

MIT License — feel free to use and modify!
