import io
import time
import requests
import picamera

URL = "http://bceb7f41087d-7754001953109090881.ngrok-free.app/upload"  # Change to your server's IP

# Initialize PiCamera
camera = picamera.PiCamera()
camera.resolution = (640, 480)  # Adjust resolution as needed
camera.framerate = 20
time.sleep(2)  # Allow camera to warm up

stream = io.BytesIO()

for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
    stream.seek(0)
    try:
        response = requests.post(URL, files={'image': ('frame.jpg', stream.read(), 'image/jpeg')})
    except requests.exceptions.RequestException as e:
        print(f"Error sending frame: {e}")

    stream.seek(0)
    stream.truncate()

    time.sleep(0.05)  # Adjust sleep to control frame rate
