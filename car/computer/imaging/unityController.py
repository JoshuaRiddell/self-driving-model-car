import socket
import struct
import numpy
import time
from unityCamera import UnityCamera
from pathFinder import *

from pathPlanner import PathPlanner, Path

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

	planner = PathPlanner()
	path = Path()
	radius = -100
	angle = 45
	path.set_arc(radius, angle)
	# path.set_line(10)
	planner.set_path(path, 0, 0, 0)

	

	car = UnityCarController()
	cam = UnityCamera()

	actualVelocity = 20.0

	lastTime = 0

	heading = 0
	x = 0 
	y = 0 
	velocity = 0
	steeringAngle = 0
	telemReceived = False

	pathPlanned = False
	segmentComplete = True
	lastPlanTime = 0.0
	planTimeout = 1.0
	while 1:
		cam.receive()
		if cam.imageReceived:
			img, telem = cam.recv_image()
			radius, pathImage = find_path(img, 200, steeringAngle)

			cv2.namedWindow('Image1', cv2.WINDOW_NORMAL)
			cv2.imshow('Image1', pathImage)
			cv2.waitKey(1)

			if telemReceived and (segmentComplete or (time.time() - lastPlanTime > planTimeout)):
				pathPlanned = True
				print "Setting Path! Radius: ", radius
				#this can be used to adjust velocity based on path
				# if abs(radius) > 200:
				# 	actualVelocity = 50.0
				# else:
				# 	actualVelocity = 5.0

				path.set_arc(radius, 60.0)
				
				#note:STEERING_ANGLE_SHRINK_RATE Trying to encourage smoother transitions between paths, but reduce oscillation. 
				planner.set_path(path, x, y, heading + STEERING_ANGLE_SHRINK_RATE*steeringAngle)
				lastPlanTime = time.time()

			
		car.receive_data()
		if car.telemReceived:
			telemReceived = True
			# print time.time() - lastTime
			lastTime = time.time()
			heading, x, y, velocity, steeringAngle = car.get_telem()
			steeringAngle *= -1
			heading *= -1
			planner.velocity = actualVelocity


			if pathPlanned:
				segmentComplete, steeringAngle = planner.calculate_steering_angle(x, y, heading)
				# print "Steering angle: ", -steeringAngle
				car.send_command(actualVelocity, -steeringAngle)
				# h, w, d = pathImage.shape
				# xP = planner.currentX
				# yP = planner.currentY
				# cv2.circle(pathImage, (int(xP) + w/2, h-int(yP)), 5,(0,255,0))
				# cv2.namedWindow('Image1', cv2.WINDOW_NORMAL)
				# cv2.imshow('Image1', pathImage)
				# cv2.waitKey(1)

			# except:
			# 	break

		# time.sleep(0.1)


	car.close()

	


