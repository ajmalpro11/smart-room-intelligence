# ir_sensor.py
# Reads motion detection from IR obstacle avoidance sensor
# Outputs HIGH when object detected, LOW when clear

from gpiozero import DigitalInputDevice
import time

# --- Pin configuration ---
IR_PIN = 23  # GPIO 23 = Pi Pin 16

# Setup IR sensor
ir_sensor = DigitalInputDevice(IR_PIN, pull_up=True)

def is_motion_detected():
    # IR sensor outputs LOW when object detected
    # (pull_up=True means we invert the logic)
    return not ir_sensor.value

def main():
    print("IR Sensor ready... (Ctrl+C to stop)")
    print("Wave your hand in front of the sensor!")
    try:
        previous_state = False
        while True:
            motion = is_motion_detected()

            if motion and not previous_state:
                print("🔴 MOTION DETECTED!")

            elif not motion and previous_state:
                print("🟢 Clear — no motion")

            previous_state = motion
            time.sleep(0.1)  # check 10 times per second

    except KeyboardInterrupt:
        print("Sensor stopped")
        ir_sensor.close()

if __name__ == "__main__":
    main()
