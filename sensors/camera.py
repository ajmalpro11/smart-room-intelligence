# camera.py
# Captures photos using Pi Camera Module 3 (IMX708)
# Uses picamera2 library — official Pi 5 camera library

from picamera2 import Picamera2
from datetime import datetime
import time
import os
os.environ["LIBCAMERA_LOG_LEVELS"] = "3"

# --- Setup ---
PHOTOS_DIR = "/home/ajmalpro11/smart-room/photos"

def setup_camera():
    camera = Picamera2()
    config = camera.create_still_configuration(
        main={"size": (1920, 1080)},  # Full HD
        display=None
    )
    camera.configure(config)
    return camera

def capture_photo(camera, reason="capture"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{PHOTOS_DIR}/{reason}_{timestamp}.jpg"
    camera.start()
    time.sleep(0.5)  # let camera adjust exposure
    camera.capture_file(filename)
    camera.stop()
    print(f"Photo saved: {filename}")
    return filename

def main():
    print("Initialising camera...")
    camera = setup_camera()
    print("Camera ready!")
    print("Press Enter to capture a photo (Ctrl+C to stop)")
    try:
        while True:
            input("")
            capture_photo(camera, reason="manual")
    except KeyboardInterrupt:
        print("Camera stopped")
        camera.close()

if __name__ == "__main__":
    main()
