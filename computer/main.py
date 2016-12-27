import vision as vi
import hardware as hi
import server

from time import sleep

class MainApp(object):
    def __init__(self):
        self.vis_int = vi.VisionInterface()
        self.har_int = hi.HardwareInterface()

    def run(self):
	while True:
		



        sleep(5)
        self.har_int.write_pwm(hi.THROT, 0)
        sleep(2)


        print "starting"

        for i in range(9):
            self.har_int.write_pwm(hi.THROT, i)
            sleep(0.1)

        sleep(1.5)

        while True:
            steer = self.vis_int.read_frame()

            # print steer

            if steer is None:
                self.har_int.write_pwm(hi.SERVO, 40)
                continue

            self.har_int.write_pwm(hi.SERVO, steer)

        # while True:
        #     sleep(1)
        #     self.har_int.write_pwm(SERVO, -50)
        #     sleep(1)
        #     self.har_int.write_pwm(SERVO, 0)
        #     sleep(1)
        #     self.har_int.write_pwm(SERVO, 50)


def main():
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()
