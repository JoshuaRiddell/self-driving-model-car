#!/usr/bin/python2

USE_SERVER = False

import vision as vi
import hardware as hi
from threading import Thread, Lock
from time import sleep
from math import pi
if USE_SERVER:
    import server

HARDWARE_CONNECTED = True

class Main(Thread):
    """Main control thread.
    """
    def __init__(self):
        """Initialise the vision interface and hardware interface (arduino and
        camera).
        """
        super(Main, self).__init__()
        self.daemon = not USE_SERVER

        self.vision = vi.VisionInterface()
        if HARDWARE_CONNECTED:
            self.hardware = hi.HardwareInterface()

    def run(self):
        """Main control loop.
        """
        ON = 8
        OFF = 5

        while True:
            if (HARDWARE_CONNECTED and self.hardware.get_state() == hi.AUTO) or not HARDWARE_CONNECTED:
                angle = self.vision.read_frame()
                if angle != 0:
                    angle = angle - pi/2

                if HARDWARE_CONNECTED:
                    self.hardware.add_to_pwm_queue(hi.SERVO, angle * 80)
                    self.hardware.add_to_pwm_queue(hi.THROT, ON)
                    # self.hardware.add_to_pwm_queue(hi.SERVO, 47)

                print "frame processed {}".format(angle)

if __name__ == "__main__":
    # make the main thread and start it
    main = Main()

    if USE_SERVER:
        # make the frame streaming server. This gets main control flow.
        main.start()

        server.register_vision(main.vision)
        server = server.WebServer(('0.0.0.0', 5000), server.CamHandler)
        server.serve_forever()
    else:
        main.run()

