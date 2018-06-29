import socket
import numpy as np
import cv2
import struct

IP_ADDR = '127.0.0.1'
PORT = 8000
BUFFER_SIZE = 600000
MESSAGE = "hi"

STX = "QUTQUT"
ETX = "BBLBBL"
telemetryStruct = struct.Struct('<ffff')
class UnityCamera(object):
	def __init__(self):

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((IP_ADDR, PORT))
		self.sock.send(MESSAGE)

		# while(1):
		# 	self.recv_image()

		self.imageReceived = False
		self.buffer = ""
		self.imageString = ""
	def receive(self):
		try:
			#print "receiving"
			data = self.sock.recv(BUFFER_SIZE)
			self.buffer += data
		except:
			print "Connection closed by remote host"
			exit()

		#check if there is an STX AND ETX in the buffer
		stxPos = self.buffer.find(STX)
		etxPos = self.buffer.find(ETX)
		if (stxPos != -1 and etxPos != -1 and stxPos < etxPos):
			self.imageString = self.buffer[stxPos+len(STX):etxPos]
			self.buffer = self.buffer[etxPos+len(ETX):]
			self.imageReceived = True


	def recv_image(self):
		self.imageReceived = False
		telemData = self.imageString[0:16]
		imageData = self.imageString[16:]
		telemetry = telemetryStruct.unpack(telemData)
		imageArray = np.fromstring(imageData, np.uint8)
		img = cv2.imdecode(imageArray, cv2.IMREAD_COLOR)
		return img, telemetry

		# print "Received %d byte" % (len(data))
		# if len(data) == 16:
		# 	#telemetry packet
		# 	telemetry = telemetryStruct.unpack(data)
		# 	print telemetry
		# 	return telemetry
		# elif len(data) < 100000:
		# 	return None
		# else:
		# 	#image
		# 	imageArray = np.fromstring(data, np.uint8)
		# 	img = cv2.imdecode(imageArray, cv2.IMREAD_COLOR)

		# 	return img

	def close(self):
		self.sock.close()


if __name__ == "__main__":
	# Save images from unity

	SAVE_IMAGES = True
	cam = UnityCamera()
	directoryStr = "unityTestImages2\\"
	baseImageStr = directoryStr + "img_%04d.jpg"
	# telemetryFile = open(directoryStr + "telmetry.csv", "w")
	# telemetryFile.write("i, Theta, X, Y, Z\n")
	i = 0

	while(1):
		cam.receive()
		if cam.imageReceived:
			img, telem = cam.recv_image()
			cv2.imshow('image', img)
			print telem
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		# img = cam.recv_image()
		# if img is None:
		# 	continue
		
		# if SAVE_IMAGES:
		# 	if len(img) == 4:
		# 		telemetryFile.write("%d, %f, %f, %f, %f\n" % (i, img[0], img[1], img[2], img[3]))
		# 		continue
		# 	print "saving image: ", baseImageStr % (i)
		# 	cv2.imwrite(baseImageStr % (i), img)
		# 	i += 1	
		# else:
		# 	cv2.imshow('image', img)
		# 	if cv2.waitKey(1) & 0xFF == ord('q'):
		# 		break

	exit()
