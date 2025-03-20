from flask import Flask, request, Response
import cv2
import numpy as np

app = Flask(__name__)

latest_frame = None  # Stores the most recent frame


@app.route('/upload', methods=['POST'])
def upload():
    global latest_frame
    file = request.files.get('image')
    if file:
        img_np = np.frombuffer(file.read(), np.uint8)
        latest_frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    return "Frame received", 200


def generate():
    global latest_frame
    while True:
        if latest_frame is not None:
            _, buffer = cv2.imencode('.jpg', latest_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=False)
