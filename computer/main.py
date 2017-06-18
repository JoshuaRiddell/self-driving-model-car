#!/usr/bin/python2

import vision as vi
#import hardware as hi
from threading import Thread, Lock
import server
from time import sleep

class Main(Thread):
    """Main control thread.
    """

    def __init__(self):
        """Initialise the vision interface and hardware interface (arduino and
        camera).
        """
        super(Main, self).__init__()
        self.daemon = True

        self.vision = vi.VisionInterface()
#        self.hardware = hi.HardwareInterface()

    def run(self):
        """Main control loop.
        """

        while True:
            self.vision.read_frame()

if __name__ == "__main__":
    # make the main thread and start it
    main = Main()
    main.start()

    # make the frame streaming server. This gets main control flow.
    server.register_vision(main.vision)
    server = server.WebServer(('0.0.0.0', 5000), server.CamHandler)
    server.serve_forever()

