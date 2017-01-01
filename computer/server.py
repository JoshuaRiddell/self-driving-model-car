from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from PIL import Image
from StringIO import StringIO
import base64

DEFAULT_QUALITY = 50

class WebServer(Flask):
    def __init__(self, name):
        super(WebServer, self).__init__(name)
        self.add_url_rule('/', 'index', self.index)
        self.add_url_rule('/vid/<int:vid_id>', 'video', self.video)

    def index(self):
        return render_template('index.html')

    def video(self, vid_id):
        return render_template('video.html', vid_id=vid_id)

class SocketServer(SocketIO):
    def __init__(self, app, vis):
        super(SocketServer, self).__init__(app)
        self.stream_quality = DEFAULT_QUALITY
        self.vis = vis

        self.on_event('stream', self.stream_frame)

    def stream_frame(self, data):
        frame = self.vis.get_frame(data['vid_id'])
        image = Image.fromarray(frame)
        buf = StringIO()
        image.save(buf, 'JPEG', quality=30)

        data = {
            "raw": 'data:image/jpeg;base64,' +
                base64.b64encode(buf.getvalue())
        }
        emit('stream', data)
