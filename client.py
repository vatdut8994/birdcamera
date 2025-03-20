import cv2
import requests
import time

URL = "http://bceb7f41087d-7754001953109090881.ngrok-free.app/upload"  # Change to your server's IP

cap = cv2.VideoCapture(0)  # Open default camera
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    _, img_encoded = cv2.imencode('.jpg', frame)
    try:
        response = requests.post(URL, files={'image': ('frame.jpg', img_encoded.tobytes(), 'image/jpeg')})
    except requests.exceptions.RequestException as e:
        print(f"Error sending frame: {e}")
    
    time.sleep(0.05)  # Adjust for desired frame rate

cap.release()
