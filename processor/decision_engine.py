# decision_engine.py
# Combines all sensors into one intelligent detection system
# Logic: IR + Ultrasonic → Camera + Buzzer + Log

from gpiozero import DistanceSensor, DigitalInputDevice, Buzzer
from picamera2 import Picamera2
import adafruit_dht
import board
import time
import os
from datetime import datetime

# --- Suppress camera log noise ---
os.environ["LIBCAMERA_LOG_LEVELS"] = "3"

# --- Configuration ---
PHOTOS_DIR = "/home/ajmalpro11/smart-room/photos"
LOG_FILE   = "/home/ajmalpro11/smart-room/logs/alerts.log"
DISTANCE_THRESHOLD = 150  # cm — alert if closer than this

# --- Sensor setup ---
print("Initialising sensors...")

ultrasonic = DistanceSensor(echo=24, trigger=18, max_distance=4)
ir_sensor  = DigitalInputDevice(23, pull_up=False)
buzzer     = Buzzer(25)
dht_sensor = adafruit_dht.DHT22(board.D17)

# --- Camera setup ---
camera = Picamera2()
config = camera.create_still_configuration(
    main={"size": (1920, 1080)},
    display=None
)
camera.configure(config)

print("All sensors ready!")
print("System armed — monitoring... (Ctrl+C to stop)")
print("")

# --- Helper functions ---
def get_distance():
    return round(ultrasonic.distance * 100, 2)

def is_motion():
    return  ir_sensor.value

def get_environment():
    try:
        temp = dht_sensor.temperature
        humidity = dht_sensor.humidity
        return temp, humidity
    except RuntimeError:
        return None, None

def capture_photo(reason="intruder"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"{PHOTOS_DIR}/{reason}_{timestamp}.jpg"
    camera.start()
    time.sleep(0.5)
    camera.capture_file(filename)
    camera.stop()
    return filename

def sound_alert():
    for _ in range(3):
        buzzer.on()
        time.sleep(0.2)
        buzzer.off()
        time.sleep(0.2)

def log_alert(distance, temp, humidity, photo):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"[{timestamp}] ALERT! "
        f"Distance: {distance}cm | "
        f"Temp: {temp}°C | "
        f"Humidity: {humidity}% | "
        f"Photo: {photo}\n"
    )
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    print(log_entry.strip())

# --- Main loop ---
def main():
    last_alert_time = 0
    alert_cooldown  = 10  # seconds between alerts

    try:
        while True:
            distance = get_distance()
            motion   = is_motion()

            # Show live status
            print(f"Distance: {distance}cm | Motion: {'YES' if motion else 'no '}", end="\r")

            # --- Decision logic ---
            if motion and distance < DISTANCE_THRESHOLD:
                current_time = time.time()

                # Cooldown check — don't spam alerts
                if current_time - last_alert_time > alert_cooldown:
                    print("\n🔴 INTRUDER DETECTED!")

                    # Get environment readings
                    temp, humidity = get_environment()

                    # Capture photo
                    photo = capture_photo(reason="intruder")
                    print(f"📸 Photo saved: {photo}")

                    # Sound buzzer
                    sound_alert()

                    # Log the alert
                    log_alert(distance, temp, humidity, photo)

                    last_alert_time = current_time

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nSystem disarmed")
        buzzer.off()
        camera.close()
        dht_sensor.exit()
        ultrasonic.close()
        ir_sensor.close()

if __name__ == "__main__":
    main()
