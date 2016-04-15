import cv2 as cv

class Vision(object):
	def __init__(self, camera_id=0):
		self.cam = cv.VideoCapture(camera_id)

		self.capture()

	def capture(self):
		ret, self.current_frame = cam.read()

