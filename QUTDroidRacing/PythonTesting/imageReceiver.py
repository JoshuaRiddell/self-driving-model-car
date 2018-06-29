#!/usr/bin/env python

import socket
import numpy as np
import cv2

TCP_IP = '127.0.0.1'#'192.168.0.2'
TCP_PORT = 8000
BUFFER_SIZE = 60000
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)

while (1) :
	try:
		data = s.recv(BUFFER_SIZE)
	except:
		print "Connection closed by remote host"
		break
	print "received data" , len(data)

	nparr = np.fromstring(data, np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	img = cv2.Canny(img,100,200)
	cv2.imshow('image', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	#image = np.frombuffer(data, dtype='uint8')
	#print image

	
s.close()