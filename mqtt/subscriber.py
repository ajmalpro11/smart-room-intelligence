# subscriber.py
# Receives MQTT messages and stores them in InfluxDB
# Data flows: MQTT → InfluxDB → Grafana

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from datetime import datetime

# --- Configuration ---
MQTT_BROKER  = "localhost"
MQTT_PORT    = 1883
MQTT_TOPIC   = "smartroom/sensors"

INFLUX_URL   = "http://localhost:8086"
INFLUX_TOKEN = "smartroom-token-2026"
INFLUX_ORG   = "smartroom"
INFLUX_BUCKET = "sensors"

# --- InfluxDB Setup ---
influx_client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)
print("Connected to InfluxDB!")

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker!")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to: {MQTT_TOPIC}")
        print("Waiting for sensor data...")
    else:
        print(f"Connection failed: {reason_code}")

def on_message(client, userdata, msg):
    try:
        # Parse incoming JSON
        data = json.loads(msg.payload.decode())

        # Build InfluxDB data points
        points = []

        if data.get("distance") is not None:
            points.append(
                Point("sensors")
                .tag("location", "room")
                .field("distance", float(data["distance"]))
            )

        if data.get("motion") is not None:
            points.append(
                Point("sensors")
                .tag("location", "room")
                .field("motion", int(data["motion"]))
            )

        if data.get("temperature") is not None:
            points.append(
                Point("sensors")
                .tag("location", "room")
                .field("temperature", float(data["temperature"]))
            )

        if data.get("humidity") is not None:
            points.append(
                Point("sensors")
                .tag("location", "room")
                .field("humidity", float(data["humidity"]))
            )

        # Write to InfluxDB
        write_api.write(bucket=INFLUX_BUCKET, record=points)
        print(f"Stored → Temp: {data.get('temperature')}°C | "
              f"Humidity: {data.get('humidity')}% | "
              f"Distance: {data.get('distance')}cm | "
              f"Motion: {data.get('motion')}")

    except Exception as e:
        print(f"Error processing message: {e}")

# --- MQTT Client Setup ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
print("Starting subscriber... (Ctrl+C to stop)")
client.loop_forever()
