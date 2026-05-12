# ultrasonic.py
# Reads distance from HC-SR04 ultrasonic sensor
# Uses gpiozero - fully compatible with Raspberry Pi 5

from gpiozero import DistanceSensor
import time

# --- Pin configuration ---
# TRIG = GPIO 18, ECHO = GPIO 24
sensor = DistanceSensor(echo=24, trigger=18, max_distance=4)

def get_distance():
    distance = sensor.distance * 100  # convert metres to cm
    return round(distance, 2)

def main():
    print("Sensor initialising... please wait")
    time.sleep(2)
    print("Reading distance... (Ctrl+C to stop)")
    try:
        while True:
            dist = get_distance()
            print(f"Distance: {dist} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped")
        sensor.close()

if __name__ == "__main__":
    main()
