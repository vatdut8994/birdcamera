import picamera2
import time

# Initialize the camera
picam2 = picamera2.Picamera2()

# Configure the camera
config = picam2.create_still_configuration()
picam2.configure(config)

# Start the camera
picam2.start()

# Capture a still image
picam2.annotate(text="Captured Image")
picam2.capture_file("image.jpg")
time.sleep(2)

# Stop the camera
picam2.stop()
