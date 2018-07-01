import matplotlib.pyplot as plt
import numpy as np

PATH_COMPLETE_THRESHOLD = 3.0

class Path(object):
	def __init__(self, radius = 0, angle = 0, straight = True, length = 5):
		if not straight:
			self.set_arc(radius, angle)
		else:
			self.set_line(length)

	def set_arc(self, radius, angle):
		self.straight = False
		self.radius = radius
		self.angle = angle
		if self.radius > 0:
			#TURN RIGHT
			self.endX = -self.radius * ( np.cos(np.deg2rad(self.angle)) - 1)
			self.endY = self.radius * ( np.sin(np.deg2rad(self.angle)))
		else:
			#TURN LEFT
			self.endX = -self.radius * ( np.cos(np.deg2rad(self.angle)) - 1)
			self.endY = -self.radius * ( np.sin(np.deg2rad(self.angle)))

		print "Finished coords: ", self.endX, self.endY

	def set_line(self, length):
		self.length = length
		self.straight = True
		self.endX = 0
		self.endY = length

	def get_path_error(self, x, y, theta):

		if self.straight:
			thetaPath = 0
			distError = x

		else:

			if y > abs(self.radius):
				thetaPath = 90.0
			elif y < -abs(self.radius):
				thetaPath = -90.0
			else:
				thetaPath = np.rad2deg(np.arcsin(y*1.0/abs(self.radius)))


			if self.radius > 0:
				#TURN RIGHT
				pathX = -self.radius * ( np.cos(np.deg2rad(thetaPath)) - 1)
				pathY = self.radius * ( np.sin(np.deg2rad(thetaPath)))
				thetaPath *= -1
			else:
				#TURN LEFT
				pathX = -self.radius * ( np.cos(np.deg2rad(thetaPath)) - 1)
				pathY = -self.radius * ( np.sin(np.deg2rad(thetaPath)))

			distError = np.sqrt((x - pathX) * (x - pathX) + (y - pathY) * (y - pathY))
			if (x < pathX):
				distError *= -1

		# print thetaPath, theta, distError
		return thetaPath - theta, distError

class PathPlanner(object):
	def __init__(self):
		self.startX = 0
		self.startY = 0
		self.startTheta = 0

		self.currentX = 0
		self.currentY = 0
		self.currentTheta = 0

		self.steeringAngle = 0
		self.velocity = 0

		self.path = None

		self.kPSteering = 1.0

		self.startMatrix = np.eye(3)
		self.startTheta = 0
		self.startX = 0
		self.startY = 0

	def set_pose(self, x, y, theta):
		# newCoords = np.matmul(self.startMatrix, np.array([x,y,1]))
		x = x - self.startX#newCoords[0]
		y = y - self.startY#newCoords[1]
		self.currentTheta = theta - self.startTheta
		self.currentTheta = self.currentTheta % 360
		if self.currentTheta > 180:
			self.currentTheta -= 360
		# print self.currentTheta
		angle = -np.deg2rad(self.startTheta)


		self.currentX = x * np.cos(angle) - y * np.sin(angle)
		self.currentY = x * np.sin(angle) + y * np.cos(angle) 
		
		# print "Current: ", self.currentX, self.currentY

	def set_path(self, path, startX, startY, startTheta):
		self.startTheta = startTheta
		# theta = np.deg2rad(startTheta)
		# self.set_pose(startX, startY, startTheta)
		self.startX = startX
		self.startY = startY

		# print "Start: ", startX, startY, startTheta

		# self.startMatrix = np.array([[np.cos(theta), -np.sin(theta), -startX],
		# 							 [np.sin(theta), np.cos(theta), -startY], 
		# 							 [0,0,1]])

		# print self.startMatrix
		self.path = path

	def calculate_steering_angle(self, x, y, heading):
		self.set_pose(x, y, heading)

		thetaE, distError = self.path.get_path_error(self.currentX, self.currentY, self.currentTheta)
		if self.velocity == 0:
			self.steeringAngle = 0
		else:
			self.steeringAngle = thetaE + np.rad2deg(np.arctan(self.kPSteering * distError / self.velocity))

			self.steeringAngle = self.steeringAngle % 360
			if self.steeringAngle > 180:
				self.steeringAngle -= 360
		finishedSegment = np.sqrt((self.currentX - self.path.endX) * (self.currentX - self.path.endX) + 
									(self.currentY - self.path.endY) * (self.currentY - self.path.endY)) < PATH_COMPLETE_THRESHOLD

		if (self.currentY > self.path.endY):
			print "WARNING: y is greater than end Y", self.currentY, self.path.endY
		return finishedSegment, self.steeringAngle

	def draw_current_path(self, carX, carY, theta, steeringAngle, drawCar = False):
		if self.path.straight:
			#path is a straight line
			x = [0,0]
			y = [0 , self.path.length]
		else:
			angle = np.arange(0, self.path.angle)

			if self.path.radius > 0:
				#TURN RIGHT
				x = -self.path.radius * ( np.cos(np.deg2rad(angle)) - 1)
				y = self.path.radius * ( np.sin(np.deg2rad(angle)))
			else:
				#TURN LEFT
				x = -self.path.radius * ( np.cos(np.deg2rad(angle)) - 1)
				y = -self.path.radius * ( np.sin(np.deg2rad(angle)))

		plt.plot(x, y)

		if drawCar:
			steeringAngle += theta
			# carX = self.currentX
			# carY = self.currentY
			arrowLength = 1
			plt.plot([carX], [carY], 'o',ms=10.0 )
			plt.arrow(carX,carY,arrowLength * np.sin(np.deg2rad(theta)),arrowLength * np.cos (np.deg2rad(theta)), head_width = 0.1*arrowLength)
			plt.arrow(carX,carY,arrowLength * np.sin(np.deg2rad(-steeringAngle)),arrowLength * np.cos (np.deg2rad(-steeringAngle)), 
				head_width = 0.1*arrowLength, fc='r', ec='r')

		plt.xlim((-10, 10))
		plt.ylim((-10,10))
		plt.show()

if __name__ == "__main__":
	planner = PathPlanner()
	path = Path()
	path.set_arc(10, 45)
	planner.set_path(path, 0, 0, 0)
	planner.velocity = 10
	x = 0
	y = 2
	heading = 0
	finished, steeringAngle = planner.calculate_steering_angle(x, y, heading)
	print steeringAngle
	planner.draw_current_path(x, y, heading, steeringAngle, drawCar = True)