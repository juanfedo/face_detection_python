#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response,request
from recognize_faces_video import VideoCamera
from multiprocessing.pool import ThreadPool
import os
os.system("taskset -a -p {}".format(os.getpid()))

class App_Singleton:
    __application = None

    @staticmethod
    def getApplication():
        if App_Singleton.__application == None:
            App_Singleton.__application = VideoCamera()
        return App_Singleton.__application

app = Flask(__name__)
pool = ThreadPool(processes=4)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    print('OS PID::::{}'.format(os.getpid()))
    while True:
        frames = App_Singleton.getApplication().frames()
        for frame in frames:
            yield (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        print('REMOTE ADDRESS: ' + request.environ['REMOTE_ADDR'])
    else:
        print('REMOTE ADDRESS: ' + request.environ['HTTP_X_FORWARDED_FOR'])
    async_result = pool.apply_async(gen)
    return Response(async_result.get(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
