from time import sleep
import serial
import threading

# left, middle, right
SERVO_POINTS = [47, 79, 112]
# full, idle, rev
THROT_POINTS = [47, 98, 146]

OUTPUT_FACTORS = [
    [x[1] for x in [SERVO_POINTS, THROT_POINTS]],  # centres
    [(x[1]-x[0])/float(100) for x in [SERVO_POINTS, THROT_POINTS]],  # negative scaling
    [(x[2]-x[1])/float(100) for x in [SERVO_POINTS, THROT_POINTS]],  # positive scaling
]

PIN_BOUNDS = [
    [47, 112],
    [47, 146],
]

NUM_CHANNELS = 2

DEVICE_PORT = "/dev/ttyACM0"
DEVICE_BAUD = 115200


class HardwareInterface(threading.Thread):
    def __init__(self):
        super(HardwareInterface, self).__init__()
        self.lock = threading.Lock()
        self.daemon = True

        self.connect_serial()

        self.flags = [None, None]
        self.val_queue = [0, 0]

        self.start()

    def connect_serial(self):
        self.ser = serial.Serial(DEVICE_PORT, DEVICE_BAUD, timeout=0.5)

    def write_pwm(self, perp_id, val):
        if val < 0:
            # val is negative
            val = OUTPUT_FACTORS[0][perp_id] + OUTPUT_FACTORS[1][perp_id] * val
        elif val == 0:
            val = OUTPUT_FACTORS[0][perp_id]
        else:
            # val is positive
            val = OUTPUT_FACTORS[0][perp_id] + OUTPUT_FACTORS[2][perp_id] * val

        # val is now a servo value, check bounds
        if val > PIN_BOUNDS[perp_id][0] and val < PIN_BOUNDS[perp_id][1]:
            self.ser.write(chr(int(perp_id)))
            self.ser.write(chr(int(val)))


    def run(self):
        while True:
            self.lock.acquire()
            flags = self.flags
            val_queue = self.val_queue
            self.flags = [None, None]
            self.lock.release()

            for i in range(NUM_CHANNELS):
                if flags[i] is not None:
                    write_pwm(i, val_queue[i])

            if self.ser.inWaiting():
                self.ser.read()
                pass
                # print self.ser.read()

            sleep(0.02)
