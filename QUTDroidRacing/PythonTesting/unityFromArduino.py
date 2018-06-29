import socket
import struct
import numpy
import time
import serial
from unityCamera import UnityCamera

UNITY_IP = 'localhost'
UNITY_PORT = 8005
BUFFER_SIZE = 1024

STX = "METR"
ETX = "BBL"

telemetryStruct = struct.Struct('<fffff')

class UnityCarController(object):
	def __init__(self):

		self.unitySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.unitySocket.bind((UNITY_IP, UNITY_PORT))

		self.unitySocket.listen(1)
		print "CarController: Waiting for unity"
		self.unityConnection, addr = self.unitySocket.accept()
		self.unitySocket.settimeout(1)
		print "CarController: Unity connected!"

		self.telemReceived = False
		self.buffer = ""
		self.telemString = ""

	def send_command(self, velocity, steeringAngle):
		sendData = STX + ("%f,%f" % (velocity, steeringAngle)) + ETX
		try:
			self.unityConnection.send(sendData)
		except:
			print "CarController: Unity Closed!"
			raise Exception

	def get_telem(self):
		if not self.telemReceived:
			return None
		self.telemReceived = False
		telemetry = telemetryStruct.unpack(self.telemString)
		return telemetry

	def receive_data(self):
		try:
			#print "receiving"
			data = self.unityConnection.recv(BUFFER_SIZE)
			self.buffer += data
		except:
			print "Connection closed by remote host :("
			exit()

		#check if there is an STX AND ETX in the buffer
		stxPos = self.buffer.find(STX)
		etxPos = self.buffer.find(ETX)
		if (stxPos != -1 and etxPos != -1 and stxPos < etxPos):
			self.telemString = self.buffer[stxPos+len(STX):etxPos]
			self.buffer = self.buffer[etxPos+len(ETX):]
			self.telemReceived = True


	def close(self):
		self.unityConnection.close()
		self.unitySocket.close()


if __name__ == "__main__":

	ser = serial.Serial(port="COM5", baudrate=9600, timeout=0)
	car = UnityCarController()
	actualVelocity = 30.0

	buf = ""
	angle = 0.0
	while 1:
		buf += ser.read(1)
		stxPos = buf.find("MBL")
		etxPos = buf.find("BBL")
		# print stxPos, etxPos, len(buf)
		if (stxPos != -1 and etxPos != -1 and stxPos < etxPos):
			controlString = buf[stxPos+len("MBL"):etxPos]
			buf = buf[etxPos+len("BBL"):]
			data = controlString.split(',')
			angle = (int(data[0]) - 1024/2) * 30 / 512.0
			speed = -(int(data[1]) - 1024/2) * 80 / 1024
			print "angle, speed: ", angle, speed
			car.send_command(speed, angle)

		# car.receive_data()
		# if car.telemReceived:
		# 	heading, x, y, velocity, steeringAngle =  car.get_telem()

		# 	try:
		# 		car.send_command(actualVelocity, angle)
		# 	except:
		# 		break

		# time.sleep(0.1)


	# car.close()

	


