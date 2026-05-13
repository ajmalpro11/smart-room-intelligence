# dht22.py
# Reads temperature and humidity from DHT22 sensor
# Uses adafruit-circuitpython-dht library

import adafruit_dht
import board
import time

# --- Pin configuration ---
# DATA pin connected to GPIO 17 = board.D17
dht_sensor = adafruit_dht.DHT22(board.D17)

def get_readings():
    temperature = dht_sensor.temperature  # Celsius
    humidity = dht_sensor.humidity        # percentage
    return temperature, humidity

def main():
    print("DHT22 ready... (Ctrl+C to stop)")
    print("Reading temperature and humidity...")
    print("")
    try:
        while True:
            try:
                temp, humidity = get_readings()
                print(f"Temperature: {temp}°C  |  Humidity: {humidity}%")
            except RuntimeError as e:
                # DHT22 sometimes misreads — just try again
                print(f"Reading error: {e} — retrying...")
            time.sleep(2)  # DHT22 needs 2 seconds between readings
    except KeyboardInterrupt:
        print("Sensor stopped")
        dht_sensor.exit()

if __name__ == "__main__":
    main()
