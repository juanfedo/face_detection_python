import cv2


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0) 

    def __del__(self):
        self.video.release()

    def get_frame(self):
        while True:
            _, img = self.video.read()            
            return cv2.imencode('.jpg', img)[1].tobytes()