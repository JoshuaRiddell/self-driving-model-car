import cv2
from flask import Flask, render_template, Response

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
        return jpeg.tobytes()

class Server(Flask):
    def __init__(self, name):
        super(Server, self).__init__(name)
        self.add_url_rule('/vid', 'vid', self.video_feed)
        self.add_url_rule('/pvid', 'pvid', self.video_feed)
        self.add_url_rule('/', 'index', self.index)

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

if __name__ == '__main__':
    app = Server(__name__)
    app.run(host='0.0.0.0', debug=True)
