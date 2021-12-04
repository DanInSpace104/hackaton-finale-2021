import base64
import json
import pickle
import queue
import random
import threading

import cv2
import imutils
import numpy as np
import requests
from flask import Flask, Response, redirect, render_template, request, send_from_directory
from flask_socketio import SocketIO, join_room
from imutils.video import VideoStream
from pymemcache.client.base import Client

from find_pepper import find_pepper
from find_sn import get_sn_carriage

SERVER_URL = 'http://95.181.198.19:8000'

app = Flask(__name__, static_folder="./assets", template_folder='./assets')
sio = SocketIO(app)
cargo_room = []
weight_room = []

cap = None
latest_frame = None


@sio.event
def connect():
    print("I'm connected!", request.sid)


@sio.event
def disconnect():
    print("I'm disconnected!", request.sid)
    try:
        weight_room.remove(request.sid)
    except ValueError:
        pass
    try:
        cargo_room.remove(request.sid)
    except ValueError:
        pass


@sio.on('join_cargo')
def join_cargo():
    print('join_cargo', request.sid)
    cargo_room.append(request.sid)
    join_room('cargo_room')
    if len(cargo_room) < 2:
        sio.start_background_task(cargo_bg_thread)


@sio.on('join_weight')
def join_weight():
    print('join_weight', request.sid)
    weight_room.append(request.sid)
    join_room('weight_room')
    if len(cargo_room) < 2:
        sio.start_background_task(weight_bg_thread)


def cargo_bg_thread():
    mem = Client('localhost')
    while True:
        if len(cargo_room) == 0:
            print('empty cargo room')
            return
        img = pickle.loads(mem.get('latest_frame'))
        percent, images = find_pepper(img)
        img = images['result']
        mem.set('vagon1:trash_percent', str(percent))
        # for name, img in images.items():
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        frame = base64.encodebytes(frame).decode("utf-8")

        mem.set('vagon1:trash_image', frame)
        sio.emit('cargo_image', frame, to='cargo_room')
        # sio.emit('trash_percentage', percent, to='pepper_room')
        sio.sleep(0.2)


def weight_bg_thread():
    mem = Client('localhost')
    while True:
        if len(weight_room) == 0:
            print('empty weight room')
            return
        img = pickle.loads(mem.get('number_frame'))
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        frame = base64.encodebytes(frame).decode("utf-8")
        mem.set('vagon1:number_image', frame)
        mem.set('vagon1:cart_weight', 60000 + random.random() * 10000)
        sio.emit('weight_image', frame, to='weight_room')

        num = get_sn_carriage(img)
        if num:
            print(num)
            try:
                numn = int(num[0])
            except ValueError:
                pass

            print(numn)
            mem.set('vagon1:cart_number', str(numn))
            sio.emit('weight_number', numn, to='weight_room')
        sio.sleep(0.2)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/gallery')
def galerry():
    return render_template('gallery.html')


# @sio.on('join_gallery')
# def gallery():
#     mem = Client('localhost')
#     while True:
#         img = pickle.loads(mem.get('latest_frame'))
#         _, images = find_pepper(img)
#         for i, image in enumerate(images.values()):
#             frame = cv2.imencode('.jpg', image)[1].tobytes()
#             frame = base64.encodebytes(frame).decode("utf-8")
#             sio.emit('gallery' + str(i), frame)
#         sio.sleep(1)


@app.route('/index', methods=['post'])
def indexpost():
    global latest_frame
    if request.method == 'POST':
        data = {
            "cargo_weight": 1,
            "carriage_number": "1",
            "carriage_type": "1",
            # "carriage_photo": "",
            "quality_control": 23,
            # "carriage_quality_photo": "http://127.0.0.1:8000/media/carriage_quality/photo_2021-12-03_12-57-48.jpg",
            "train": 1,
        }
        if latest_frame is not None:
            frame = bytes(latest_frame)
            # frame = cv2.imencode('.jpg', latest_frame)[1].tobytes()
            # frame = base64.encodebytes(frame).decode("utf-8")
            data['carriage_photo'] = frame
            print(frame)
        else:
            print('where is frame???')
        # data.update(request.form)
        # trainnum = request.form.get('trainnum')

        # pepperweight = request.form.get('pepperweight')
        # carrtype = request.form.get('carrtype')
        # carrnum = request.form.get('carrnum')
    else:
        print('NOT POST')

    print(requests.post(SERVER_URL + '/api/carriages/', data))
    return redirect('/index')


@app.route('/cdump')
def cdump():
    return render_template('cargodump.html')


if __name__ == '__main__':
    FLASK_PORT = 5000
    FLASK_HOST = '0.0.0.0'
    sio.run(app, debug=True, host='0.0.0.0', port=5000)
