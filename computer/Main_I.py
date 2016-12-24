import DRC_I as vi
import hardware as hi
from time import sleep

SERVO = 0  # takes -100% to 100% value corresponding to left and right
THROT = 1  # takes -100% to 100% value corresponding to reverse and forward

class MainApp(object):
    def __init__(self):
        self.v = vi.HoughVision(0)
        self.h = hi.HardwareInterface()

    def run(self):
        self.har_int.write_pwm(THROT, 0)
        self.har_int.write_pwm(SERVO, 0)
    
    def Control(self):
        while(1):
            self.v.Get()
            self.v.Thresh()
            if self.v.PointThresh() == (0,1):
                self.har_int.write_pwm(SERVO, 0)
            else self.v.PointThresh() == (0,0):
                self.har_int.write_pwm(SERVO, 15)

                
        


def main():
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()
