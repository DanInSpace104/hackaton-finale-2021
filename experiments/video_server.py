import base64
import json
from time import sleep

import cv2
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = '78581099#lkjh'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('check')
def gen(json):
    print('startginh gen')
    cap = cv2.VideoCapture("rtsp://admin:123456@10.0.10.123:554/ISAPI/Streaming/Channels/101")
    while cap.isOpened():
        ret, img = cap.read()
        if ret:
            img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            frame = base64.encodebytes(frame).decode("utf-8")
            socketio.emit('image', frame)
            socketio.sleep()
        else:
            break
    print('exiting gen')


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
