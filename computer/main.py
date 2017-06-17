#!/usr/bin/python2

import vision as vi
#import hardware as hi
from threading import Thread, Lock
import server
from time import sleep

class Main(Thread):
    def __init__(self):
        super(Main, self).__init__()
        self.daemon = True

        self.vis_int = vi.VisionInterface()
#        self.har_int = hi.HardwareInterface()

    def run(self):
        while True:
            self.vis_int.read_frame()

if __name__ == "__main__":
    main = Main()
    main.start()

    app = server.WebServer(__name__)
    socket = server.SocketServer(app, main.vis_int)

    socket.run(app, host='10.1.0.1', port=5000, debug=True, use_reloader=False,
            threaded=True)
