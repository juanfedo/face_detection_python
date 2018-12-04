#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response,request
from recognize_faces_video import VideoCamera


# import camera driver
# if os.environ.get('CAMERA'):
#     Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#     #from camera import Camera
#     from recognize_faces_video import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frames = camera.frames()
        for frame in frames:
            yield (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        print('REMOTE ADDRESS: ' + request.environ['REMOTE_ADDR'])
    else:
        print('REMOTE ADDRESS: ' + request.environ['HTTP_X_FORWARDED_FOR']) 
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
