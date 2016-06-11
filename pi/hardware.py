import pigpio as pig

PI = pig.pi()

INPUT_PINS = [20, 21]
OUPTUT_PINS = [14, 15]

# left, middle, right
STEERING = [1045, 1380, 1715]

# full, idle, rev
THROTTLE = [2055, 1555, 1020]

PIN_BOUNDS = [
    [1045, 1715],
    [1555, 1555],
]

class HardwareInterface(object):
    def __init__(self, pwm_read=False):
        self.pi = pig.pi()
        # reading from pwm can be disabled to increase performance
        if pwm_read:
            self.pwm_inputs = [PwmReader(self.pi, x) for x in INPUT_PINS]
        self.pwm_outputs = [PwmWriter(self.pi, x) for x in OUPTUT_PINS]

    def read_pwm(self):
        pwm_values = []
        for pwm_input in self.pwm_inputs:
            pwm_values.append(pwm_input.read_pwm())
        return pwm_values

    def write_pwm(self, perp_id, val):
        if val > PIN_BOUNDS[perp_id][0] and val < PIN_BOUNDS[perp_id][1]:
            self.pwm_outputs[perp_id].set_pwm(val)


class PwmReader(object):
    def __init__(self, pi, pin):
        self.pi = pi
        self.pin = pin

        pi.set_mode(self.pin, pig.INPUT)  # set pin to input
        pi.callback(self.pin, pig.EITHER_EDGE, self.edge)  # add callback for when logic level is changed

        # initialise start and end variables
        self.on_start_temp = 0
        self.on_start = 0
        self.on_end = 0
    
    def read_pwm(self):
        return self.on_end - self.on_start

    def edge(self, gpio_pin, new_edge, tick):
        if new_edge == 1:
            self.on_start_temp = tick
        else:
            self.on_end = tick
            self.on_start = self.on_start_temp

class PwmWriter(object):
    def __init__(self, pi, pin):
        self.pi = pi
        self.pin = pin

        pi.set_mode(self.pin, pig.OUTPUT)  # set pin to input

        self.set_pwm = lambda x: pi.set_servo_pulsewidth(pin, x)
