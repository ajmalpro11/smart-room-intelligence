# publisher.py
# Reads all sensors and publishes data to MQTT broker
# Data flows: Sensors → MQTT → InfluxDB → Grafana

import paho.mqtt.client as mqtt
from gpiozero import DistanceSensor, DigitalInputDevice
import adafruit_dht
import board
import time
import json
from datetime import datetime

# --- MQTT Configuration ---
MQTT_BROKER = "localhost"
MQTT_PORT   = 1883
MQTT_TOPIC  = "smartroom/sensors"

# --- Sensor Setup ---
print("Initialising sensors...")
ultrasonic = DistanceSensor(echo=24, trigger=18, max_distance=4)
ir_sensor  = DigitalInputDevice(23, pull_up=False)
dht_sensor = adafruit_dht.DHT22(board.D17)

# --- MQTT Client Setup ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker!")
    else:
        print(f"Connection failed: {reason_code}")

client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

print("Publishing sensor data... (Ctrl+C to stop)")
print("")

def get_dht_readings():
    try:
        return dht_sensor.temperature, dht_sensor.humidity
    except RuntimeError:
        return None, None

try:
    while True:
        # Read all sensors
        distance = round(ultrasonic.distance * 100, 2)
        motion   = 1 if ir_sensor.value else 0
        temp, humidity = get_dht_readings()

        # Build data payload
        payload = {
            "timestamp": datetime.now().isoformat(),
            "distance":  distance,
            "motion":    motion,
            "temperature": temp,
            "humidity":    humidity
        }

        # Publish to MQTT
        client.publish(MQTT_TOPIC, json.dumps(payload))

        # Show in terminal
        print(f"Published → Distance: {distance}cm | "
              f"Motion: {'YES' if motion else 'no '} | "
              f"Temp: {temp}°C | "
              f"Humidity: {humidity}%")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nPublisher stopped")
    client.loop_stop()
    client.disconnect()
    ultrasonic.close()
    ir_sensor.close()
    dht_sensor.exit()
