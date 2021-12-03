import argparse
import base64
import datetime
import json
import os
import threading
import time

import cv2
import imutils
import numpy as np
from flask import Flask, Response, render_template, request, send_from_directory
from flask_socketio import SocketIO
from imutils.video import VideoStream
from find_pepper import find_pepper

app = Flask(__name__, static_folder="./assets", template_folder='./assets')
socketio = SocketIO(app)
cap = None

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('check')
def gen(json):
    global cap
    if cap is None:
        cap = cv2.VideoCapture(-1)
    while cap.isOpened():
        ret, img = cap.read()
        if ret:
           # img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            frame = find_pepper(img)
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            frame = base64.encodebytes(frame).decode("utf-8")
            socketio.emit('image', frame)
            socketio.sleep(1)
        else:
            cap.release()
            break
    cap.release()
    cap = None
    print('exiting gen')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    FLASK_PORT = 5000
    FLASK_HOST = '0.0.0.0'
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
