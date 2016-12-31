import cv2
from flask import Flask, render_template, Response
from threading import Lock, Thread

DEFAULT_JPG_QUALITY = 50

class FrameStream(object):
    def __init__(self, cam, frame_id, quality):
        self.cam = cam
        self.frame_id = frame_id
        self.quality = quality

    def get_frame(self):
        return self.cam.get_frame(self.frame_id)

    @staticmethod
    def gen(frame_stream):
        while True:
            frame = frame_stream.get_frame()
            ret, jpg = cv2.imencode('.jpg', frame,
                [int(cv2.IMWRITE_JPEG_QUALITY), frame_stream.quality])
            frame = jpg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

class Server(Flask):
    def __init__(self, name):
        super(Server, self).__init__(name)
        self.jpg_quality = DEFAULT_JPG_QUALITY

        self.add_url_rule('/', 'index', self.index)
        self.add_url_rule('/test', 'test', self.test)
        self.add_url_rule('/vid/<int:vid_id>', 'vid', self.vid)

    def vid(self, vid_id):
        num_frames = self.cam.get_number_frames()
        if vid_id < 0 or vid_id > num_frames-1:
            return 'Video stream not found'
        return Response(FrameStream.gen(
            FrameStream(self.cam, vid_id, self.jpg_quality)),
                mimetype='multipart/x-mixed-replace; boundary=frame')

    def add_main(self, main):
        self.main = main
        self.cam = main.vis_int

    def run(self):
        return super(Server, self).run(host='0.0.0.0', debug=True,
                use_reloader=False)

    def index(self):
        return render_template('index.html')

    def test(self):
        return "The number is " + str(self.main.x)

