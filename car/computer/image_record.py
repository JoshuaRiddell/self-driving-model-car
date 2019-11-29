#!/usr/bin/python2

import vision as vi
import hardware as hi
from threading import Thread, Lock
import server
from time import sleep
from os import mkdir
from shutil import rmtree

class Main(Thread):
    """Main control thread.
    """

    def __init__(self, path):
        """Initialise the vision interface and hardware interface (arduino and
        camera).
        """
        super(Main, self).__init__()
        self.daemon = True

        self.vision = vi.VisionInterface()
        self.hardware = hi.HardwareInterface()

        path_id = 0
        overwrite = -1

        while True:
            self.path = "/home/ubuntu/images2018/" + path + str(path_id)
            try:
                mkdir(self.path)
                break
            except OSError:
                if overwrite == -1:
                    char = raw_input("Already exists, overwite (y/n): ")
                    if char == 'y' or char == 'Y':
                        overwrite = True
                        rmtree(self.path)
                        break
                    else:
                        overwrite = False

                path_id += 1

    def run(self):
        """Main control loop.
        """

        started = False
        frame_count = 0

        while True:
            self.vision.read_frame()

            if self.hardware.get_state() == hi.MANUAL:
                if not started:
                    print "Recording..."
                    started = True

                self.vision.save_frame(2, self.path)
                frame_count += 1
            else:
                if started:
                    print "Stopped."
                    print "{0} frames saved.".format(frame_count)
                    started = False
                    frame_count = 0

            sleep(0.1)

if __name__ == "__main__":
    path = raw_input("Please enter path: ")

    if len(path) == 0:
        path = "test"
    # make the main thread and start it
    main = Main(path)
    main.start()
    # make the frame streaming server. This gets main control flow.
    server.register_vision(main.vision)
    server = server.WebServer(('0.0.0.0', 5000), server.CamHandler)
    server.serve_forever()

