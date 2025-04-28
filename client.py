import cv2
import numpy as np
import requests
import time
from picamera2 import Picamera2

URL = "http://75.183.209.207:9265/upload"  # Change to your server's IP

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (320, 240), "format": "RGB888"}))  # Lower resolution for speed
picam2.start()

time.sleep(1)  # Allow camera to warm up

while True:
    frame = picam2.capture_array()  # Get frame as a NumPy array
    
    # Encode the frame as JPEG (Lower quality for faster transmission)
    _, img_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])  
    
    try:
        requests.post(URL, files={'image': ('frame.jpg', img_encoded.tobytes(), 'image/jpeg')}, timeout=0.5)
    except requests.exceptions.RequestException:
        print("error")
        pass  # Ignore occasional network errors
    
    # time.sleep(0.02)  # Adjust sleep time for 30-50 FPS
