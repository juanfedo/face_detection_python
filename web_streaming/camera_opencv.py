import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture('video.mp4',cv2.CAP_FFMPEG)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            try:
                # read current frame
                _, img = camera.read()
                # encode as a jpeg image and return it
                ret, im_thresh = cv2.threshold( img, 128, 255, cv2.THRESH_BINARY )
                yield cv2.imencode('.jpg', im_thresh)[1].tobytes()
            except:
                print 'error'

