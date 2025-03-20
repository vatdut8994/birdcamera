from picamera2 import Picamera2
import requests
import time
import io

URL = "http://bceb7f41087d-7754001953109090881.ngrok-free.app/upload"  # Change to your server's IP

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(main={"size": (640, 480)}))
picam2.start()

time.sleep(2)  # Give camera time to warm up

while True:
    frame = picam2.capture_array()
    
    # Encode as JPEG
    stream = io.BytesIO()
    picam2.capture_file(stream, format="jpeg")
    
    try:
        response = requests.post(URL, files={'image': ('frame.jpg', stream.getvalue(), 'image/jpeg')})
    except requests.exceptions.RequestException as e:
        print(f"Error sending frame: {e}")
    
    time.sleep(0.05)  # Adjust for desired frame rate
