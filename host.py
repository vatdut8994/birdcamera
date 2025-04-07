import os
from datetime import datetime
from flask import Flask, request, Response
from flask_compress import Compress
from PIL import Image
import io

app = Flask(__name__)
Compress(app)  # Enable compression

latest_frame = None
SAVE_PATH = "recordings"  # Directory to store motion events
os.makedirs(SAVE_PATH, exist_ok=True)

@app.route("/")
def home():
    return "Congrats bro it finally works"

@app.route('/upload', methods=['POST'])
def upload():
    global latest_frame
    file = request.files.get('image')
    if file:
        try:
            # Open the image using Pillow and convert to RGB for consistency.
            latest_frame = Image.open(file.stream).convert("RGB")
        except Exception as e:
            return "Invalid image", 400

        # Save image with timestamp when motion is detected
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_file_path = os.path.join(SAVE_PATH, f"{timestamp}.jpg")
        latest_frame.save(save_file_path, format="JPEG")

    return "Frame received", 200

def generate():
    global latest_frame
    while True:
        if latest_frame is not None:
            # Convert the Pillow image to JPEG bytes.
            img_io = io.BytesIO()
            latest_frame.save(img_io, format='JPEG')
            img_bytes = img_io.getvalue()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False, threaded=True)
