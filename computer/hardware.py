from time import sleep
import serial
from threading import Thread, Lock
import subprocess

# define channel numbers
NUM_CHANNELS = 2
SERVO = 0
THROT = 1

# left, middle, right
SERVO_POINTS = [47, 79, 112]
# full, idle, rev
THROT_POINTS = [47, 98, 146]

# scaling factors to turn percentages into 8-bit Arduino PWM outputs
OUTPUT_FACTORS = [
    [x[1] for x in [SERVO_POINTS, THROT_POINTS]],  # centres
    [(x[1]-x[0])/float(100) for x in [SERVO_POINTS, THROT_POINTS]],  # negative scaling
    [(x[2]-x[1])/float(100) for x in [SERVO_POINTS, THROT_POINTS]],  # positive scaling
]

# TODO change this to happening on the arduino
# limits on the pins
PIN_BOUNDS = [
    [47, 112],
    [47, 146],
]

# arduino board parameters
BOARD = "arduino:avr:uno"
PORT = "/dev/ttyACM0"
BAUD = 115200
HARDWARE_PATH = "../hardware/hardware.ino"

# message types
MSG_PWM = 0

class HardwareInterface(Thread):
    """Handles serial interfacing with the arduino.
    """

    def __init__(self):
        """Initialises the thread object. Attempts to connect to the arduino.
        """
        # init resources for threading
        super(HardwareInterface, self).__init__()
        self.daemon = True

        # make a lock for the command send queue to the arduino
        self.lock = Lock()

        # attempt to connect to serial with defatuls
        self.ser = serial.Serial(PORT, BAUD,
                timeout=0.5)

        self.flags = [None] * NUM_CHANNELS
        self.val_queue = [0] * NUM_CHANNELS

        #self.start()

    def upload_to_board(self):
        """UNTESTED
        Uploads the currently stored code to the arduino using the arduino
        IDE CLI
        """
        self.disconnect()
        completed = subprocess.run(["arduino", "--upload", "--board" + BOARD,
            "--port " + PORT, HARDWARE_PATH])
        self.connect()

    def connect(self):
        """Attempts another connection to the Arduino.
        """
        try:
            self.ser.open()
        except:
            return -1
        return 1

    def disconnect(self):
        """Disconnect from Arduino.
        """
       self.ser.close()

    def write_pwm(self, perp_id, val):
        """Send a PWM value over serial (blocking).
        """
        if val < 0:
            # val is negative
            val = OUTPUT_FACTORS[0][perp_id] + OUTPUT_FACTORS[1][perp_id] * val
        elif val == 0:
            val = OUTPUT_FACTORS[0][perp_id]
        else:
            # val is positive
            val = OUTPUT_FACTORS[0][perp_id] + OUTPUT_FACTORS[2][perp_id] * val

        # val is now a servo value, check bounds then send
        if val > PIN_BOUNDS[perp_id][0] and val < PIN_BOUNDS[perp_id][1]:
            self.ser.write(chr(int(perp_id)))
            self.ser.write(chr(int(val)))

    def run(self):
        """Thread for serial communications.
        """
        while True:
            # get the lock and check if there are values to send
            self.lock.acquire()
            flags = self.flags
            val_queue = self.val_queue
            self.flags = [None, None]
            self.lock.release()

            # write a pwm value if the value has changed
            for i in range(NUM_CHANNELS):
                if flags[i] is not None:
                    write_pwm(i, val_queue[i])

            # read a serial value
            if self.ser.inWaiting():
                self.ser.read()
                pass
                # print self.ser.read()

            sleep(0.02)
