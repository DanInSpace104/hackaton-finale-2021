import base64
import json
import requests


import cv2
import imutils
import numpy as np
from flask import Flask, Response, render_template, request, send_from_directory
from flask_socketio import SocketIO
from imutils.video import VideoStream
from find_pepper import find_pepper
from find_sn import get_sn_carriage

SERVER_URL = 'http://95.181.198.19:8000'

app = Flask(__name__, static_folder="./assets", template_folder='./assets')
socketio = SocketIO(app)
cap = None

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/gallery')
def galerry():
    return render_template('gallery.html')


@app.route('/index', methods= ['post'])
def indexpost():
    if request.method == 'POST':
        trainnum = request.form.get('trainnum')
        cargoweight = request.form.get('cargoweight')
        carrtype = request.form.get('carrtype')
        carrnum = request.form.get('carrnum')
    message = json.dumps({"trainnum": trainnum, "cargoweight": cargoweight, "carrtype": carrtype, "carrnum": carrnum})
    requests.post(SERVER_URL, message)


@app.route('/cdump')
def cdump():
    return render_template('cargodump.html')


@socketio.on('check')
def gen(json):
    global cap
    if cap is None:
        cap = cv2.VideoCapture(-1)
    while cap.isOpened():
        ret, img = cap.read()
        if ret:
           # img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

            images = find_pepper(img)
            frames = []
            for i, img in enumerate(images):
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                frame = base64.encodebytes(frame).decode("utf-8")
                socketio.emit('image'+str(i), frame)

            num = get_sn_carriage(img)
            if num:
                print(num)
                try:
                    numn = int(num[0])
                except ValueError:
                    continue
                print(numn)
                socketio.emit('number', numn)
            socketio.sleep(0.2)
        else:
            cap.release()
            break
    cap.release()
    cap = None
    print('exiting gen')




if __name__ == '__main__':
    FLASK_PORT = 5000
    FLASK_HOST = '0.0.0.0'
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
