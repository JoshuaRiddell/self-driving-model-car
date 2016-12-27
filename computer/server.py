import cv2

from flask import Flask, render_template, Response
from threading import Lock

#    def get_frame(self):
#        success, image = self.video.read()
#        ret, jpeg = cv2.imencode('.jpg', image,
#                [int(cv2.IMWRITE_JPEG_QUALITY), 50])
#        return jpeg.tobytes()

class WebData(object):
    def __init__(self):
        self.lock = Lock()

        self.frame  # current raw frame
        self.pframe  # current processed frame

    def set_frame(self, frane, processed):
        self.lock.acquire()
        if processed:
            self.pframe = frame.copy()
        else:
            self.frame = frame.copy()
        self.lock.release()

    def get_frame(self, processed):
        self.lock.acquire()
        if processed:
            ret = self.pframe
        else:
            ret = self.frame
        self.lock.release()

class Server(Flask):
    def __init__(self, name):
        super(Server, self).__init__(name)

        self.add_url_rule('/vid', 'vid', self.video_feed)
        self.add_url_rule('/pvid', 'pvid', self.video_feed)
        self.add_url_rule('/', 'index', self.index)

        self.lock = Lock()
        self.add_url_rule('/heartbeat', 'heartbeat', self.heartbeat)

        self.run(host='0.0.0.0', debug=True)

    def heartbeat(self):
        return None

    def index(self):
        return render_template('index.html')

    def gen(self, camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    def video_feed(self):
        return Response(self.gen(VideoCamera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

