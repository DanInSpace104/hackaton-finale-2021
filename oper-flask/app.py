from flask import Flask, Response, redirect, render_template, request, send_from_directory
from flask_socketio import SocketIO, join_room
from imutils.video import VideoStream
from pymemcache.client.base import Client

app = Flask(__name__, static_folder="./assets", template_folder='./assets')
sio = SocketIO(app)


@sio.event
def connect():
    print(request.sid, 'connected!')


@sio.event
def get_data():
    # картинки: номер вагона, распознание брака
    # данные по вагону: процент брака, вес вагона, номер вагона
    print('get_data')
    mem = Client('localhost')

    def get_data():
        sio.sleep(1)
        return {
            'trash_image': mem.get('vagon1:trash_image').decode('utf-8'),
            'number_image': mem.get('vagon1:number_image').decode('utf-8'),
            'trash_percent': mem.get('vagon1:trash_percent').decode(),
            'cart_number': mem.get('vagon1:cart_number').decode(),
            'cart_weight': mem.get('vagon1:cart_weight').decode(),
        }

    # print(mem.get('vagon1:cart_number').decode())
    sio.emit('data', {0: get_data(), 1: get_data(), 2: get_data()})


@app.route('/')
def index():
    print('index')
    return render_template('index.html')


if __name__ == '__main__':
    FLASK_PORT = 5001
    FLASK_HOST = '0.0.0.0'
    sio.run(app, debug=True, host=FLASK_HOST, port=FLASK_PORT)
