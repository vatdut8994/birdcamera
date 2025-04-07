import cv2
import requests
import time

URL = "http://192.168.1.57:7777/upload"  # Change to your server's IP

# Initialize the camera using OpenCV
cap = cv2.VideoCapture(0)  # 0 is usually the default camera (USB or built-in)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)   # Set lower resolution for faster upload
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

time.sleep(1)  # Allow camera to warm up

while True:
    ret, frame = cap.read()
    if not ret:
        continue  # Skip if frame not captured successfully
    
    # Encode the frame as JPEG (Lower quality for faster transmission)
    _, img_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])  
    
    try:
        requests.post(URL, files={'image': ('frame.jpg', img_encoded.tobytes(), 'image/jpeg')}, timeout=0.5)
    except requests.exceptions.RequestException:
        pass  # Ignore occasional network errors

    time.sleep(0.02)  # 30-50 FPS range

# When done (though you probably never reach here in while True)
cap.release()
