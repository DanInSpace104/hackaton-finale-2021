import pickle
import cv2 as cv
from pymemcache.client.base import Client
import capconfig
import time

if __name__ == '__main__':
    cap = cv.VideoCapture(capconfig.RTSP_PATH)
    if not cap.isOpened():
        print("RTSP Error, switch on camera") 
        cap.release()
        exit()
    framerate = cap.get(5)
    width  = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    print("RTSP Connect",framerate,width,height)  
    client = Client('localhost')
    ret, frame = cap.read()
    while ret:
        client.set('latest_frame', pickle.dumps(frame))
        client.set('ret', ret)
        ret, frame = cap.read()
        time.sleep(1)
    cap.release()
