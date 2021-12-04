from flask import Flask, Response, redirect, render_template, request, send_from_directory
from flask_socketio import SocketIO, join_room
from imutils.video import VideoStream
from pymemcache.client.base import Client

app = Flask(__name__, static_folder="./assets", template_folder='./assets')
sio = SocketIO(app)


@app.route('/')
def index():
    print('index')
    return render_template('index.html')


if __name__ == '__main__':
    FLASK_PORT = 5001
    FLASK_HOST = '0.0.0.0'
    sio.run(app, debug=True, host=FLASK_HOST, port=FLASK_PORT)
