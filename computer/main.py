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

        self.vision = vi.VisionInterface()
#        self.hardware = hi.HardwareInterface()

    def run(self):
        while True:
            self.vision.read_frame()

if __name__ == "__main__":
    main = Main()
    main.start()

    server.register_vis_int(main.vis_int)
    server = server.WebServer(('0.0.0.0', 5000), server.CamHandler)
    server.serve_forever()

