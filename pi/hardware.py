import pigpio as pig

PI = pig.pi()

STEER_PIN = 15
THROTTLE_PIN = 14


class HardwareInterface(object):
	def __init__(self):
		self.pi = pig.pi()
		self.pwm_inputs = [PwmReader(self.pi, THROTTLE_PIN),
			PwmReader(self.pi, STEER_PIN)]

	def read_pwm(self):
		pwm_values = []
		for pwm_input in self.pwm_inputs:
			pwm_values.append(pwm_input.read_pwm())
		return pwm_values


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



