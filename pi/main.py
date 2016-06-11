import vision as vi
import hardware as hi
from time import sleep

STEERING = 0
THROTTLE = 1

class MainApp(object):
    def __init__(self):
        self.vis_int = vi.VisionInterface()
        self.har_int = hi.HardwareInterface()

    def run(self):
        self.har_int.write_pwm(THROTTLE, 1555)

        while True:
            pass


def main():
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()
