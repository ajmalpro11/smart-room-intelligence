# ir_debug.py
# Shows raw sensor value so we can understand what's happening

from gpiozero import DigitalInputDevice
import time

IR_PIN = 23

ir_sensor = DigitalInputDevice(IR_PIN, pull_up=True)

print("Raw sensor values (Ctrl+C to stop)")
print("Wave your hand and watch the number change...")
print("")

while True:
    print(f"Raw value: {ir_sensor.value}")
    time.sleep(0.3)
