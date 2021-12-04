import pickle

import cv2 as cv
from pymemcache.client.base import Client

if __name__ == '__main__':

    cap = cv.VideoCapture(0)
    client = Client('localhost')
    ret, frame = cap.read()
    while ret:
        client.set('latest_frame', pickle.dumps(frame))
        client.set('ret', ret)
        ret, frame = cap.read()
    cap.release()
