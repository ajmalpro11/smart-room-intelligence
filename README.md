# 🏠 Smart Room Intelligence System

A multi-sensor edge IoT system built on Raspberry Pi 5 that detects
intrusions, monitors environment, and serves a live web dashboard.
All processing happens locally — no cloud dependency.

---

## 🛠️ Built With

- Raspberry Pi 5
- Python 3.13
- MQTT (Mosquitto)
- InfluxDB + Grafana
- Flask
- OpenCV

---

## 📡 Sensors Used

| Sensor | Purpose |
|---|---|
| Ultrasonic (HC-SR04) | Distance detection |
| IR sensor | Motion detection |
| DHT22 | Temperature & humidity |
| MPU-6050 | Vibration detection |
| Pi Camera | Image capture |

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/ajmalpro11/smart-room-intelligence.git
cd smart-room-intelligence
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
smart-room/
├── sensors/
│   ├── ultrasonic.py
│   ├── ir_sensor.py
│   ├── dht22.py
│   ├── mpu6050.py
│   └── camera.py
├── mqtt/
│   └── publisher.py
├── processor/
│   └── decision_engine.py
├── dashboard/
│   └── app.py
├── photos/
├── requirements.txt
└── README.md
```
---

## 📸 Development Progress

### ✅ Phase 1 — Environment Setup

| Step | Screenshot |
|---|---|
| System updated | ![System Updated](photos/00_system_updated.png) |
| I2C scan | ![I2C Scan](photos/01_i2c_empty_scan.png) |
| Virtual environment | ![Venv Active](photos/02_virtualenv_active.png) |
| Project structure | ![Project Structure](photos/03_project_structure.png) |
| All imports OK | ![Imports OK](photos/04_all_imports_ok.png) |

> 📌 More screenshots added as each phase is completed.

---

## 🗺️ System Architecture

```
Sensors (Ultrasonic, IR, DHT22, MPU-6050, Camera)
        ↓
Python Data Collector
        ↓
MQTT Broker (Mosquitto)
        ↓
Decision Engine (Python)
        ↓
┌─────────────┴─────────────┐
↓                           ↓
InfluxDB              Flask Web App
↓                           ↓
Grafana Dashboard    Live Camera Feed
```
---

## 📅 Project Phases

- [x] Phase 1 — Environment setup & library installation
- [x] Phase 1 — Ultrasonic sensor (HC-SR04) working
- [x] Phase 1 — IR sensor motion detection working
- [x] Phase 1 — Pi Camera capture
- [x] Phase 1 — DHT22 temperature & humidity (arriving today)
- [ ] Phase 1 — MPU-6050 vibration detection (arriving today)
- [ ] Phase 2 — Decision engine (sensor fusion)
- [ ] Phase 3 — MQTT + InfluxDB + Grafana
- [ ] Phase 4 — Flask web dashboard
- [ ] Phase 5 — ML anomaly detection
---

## 👨‍💻 Author

**Ajumal Shamsudeen** — TH Rosenheim, Germany

[![GitHub](https://img.shields.io/badge/GitHub-ajmalpro11-black?logo=github)](https://github.com/ajmalpro11)
