import vision as vi
import hardware as hi
from time import sleep

SERVO = 0  # takes -100% to 100% value corresponding to left and right
THROT = 1  # takes -100% to 100% value corresponding to reverse and forward

class MainApp(object):
    def __init__(self):
        self.vis_int = vi.VisionInterface()
        self.har_int = hi.HardwareInterface()

    def run(self):
        self.har_int.write_pwm(THROT, 0)
        self.har_int.write_pwm(SERVO, 0)

        while True:
            sleep(1)
            self.har_int.write_pwm(SERVO, -50)
            sleep(1)
            self.har_int.write_pwm(SERVO, 0)
            sleep(1)
            self.har_int.write_pwm(SERVO, 50)


def main():
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()
