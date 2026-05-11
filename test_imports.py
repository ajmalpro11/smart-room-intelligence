# test_imports.py
# This script checks that all our libraries are correctly installed
# If you see "ALL OK" at the end, we are ready to go!

print("Testing library imports...")

try:
    import RPi.GPIO as GPIO
    print("✅ RPi.GPIO - OK")
except ImportError:
    print("❌ RPi.GPIO - FAILED")

try:
    import smbus2
    print("✅ smbus2 - OK")
except ImportError:
    print("❌ smbus2 - FAILED")

try:
    import cv2
    print("✅ OpenCV - OK")
except ImportError:
    print("❌ OpenCV - FAILED")

try:
    import flask
    print("✅ Flask - OK")
except ImportError:
    print("❌ Flask - FAILED")

try:
    import paho.mqtt.client
    print("✅ Paho MQTT - OK")
except ImportError:
    print("❌ Paho MQTT - FAILED")

try:
    from PIL import Image
    print("✅ Pillow - OK")
except ImportError:
    print("❌ Pillow - FAILED")

try:
    import gpiozero
    print("✅ gpiozero - OK")
except ImportError:
    print("❌ gpiozero - FAILED")

print("")
print("==============================")
print("ALL IMPORTS TESTED!")
print("==============================")
