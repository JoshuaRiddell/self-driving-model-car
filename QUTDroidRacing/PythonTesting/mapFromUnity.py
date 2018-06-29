from unityCamera import UnityCamera
from imageRegistration import *
MAP_SIZE = (300, 300)

if __name__=="__main__":
	currentMap = np.zeros((MAP_SIZE[0], MAP_SIZE[1], 3))
	firstImage = True
	oldTheta = 0
	oldX = 0
	oldY = 0

	cam = UnityCamera()

	oldImage = None
	oldAngle = None
	angle = None
	image = None

	currentMatrix = np.eye(3)
	currentMatrix[0,2] = 50
	currentMatrix[1,2] = 100
	gap = 1

	imNumbers = []
	thetas = []
	xs = []
	ys = []
	zs = []

	while(1):
		cam.receive()
		if cam.imageReceived:
			img, telem = cam.recv_image()
		else:
			img = None

		if img is None:
			continue

		if angle is not None:
			oldAngle = angle
		angle = telem[0]
		print angle
		
		if oldImage is not None:

			img1 = perspecitve_warp(oldImage)
			scale = 0.1
			img1 = cv2.resize(img1, (0,0), fx=scale, fy=scale)
			img1Orig = img1.copy().astype('float32')
			img1 = img1.astype('float32')
			threshold_image(img1)
			img1 *= 255

			rows,cols,chans = img1.shape

			img2 = perspecitve_warp(img)
			img2 = cv2.resize(img2, (0,0), fx=scale, fy=scale)
			img2Orig = img2.copy().astype('float32')
			img2 = img2.astype('float32')
			threshold_image(img2)
			img2  *= 255
			

			try:
				dTheta = angle - oldAngle
				if dTheta < -180:
					dTheta += 360
				elif dTheta > 180:
					dTheta -= 360
				# print "Theta: ", dTheta
				warp_matrix = estimate_pose(img2, img1, dTheta)
				gap = 1
			except:
				sz = img1.shape
				warp_matrix = cv2.getRotationMatrix2D((sz[0]/2, sz[1]/2), -(dTheta), 1).astype('float32')[0:2,:]
				warp_matrix[0,2] = lastMatrix[0,2]
				warp_matrix[1,2] = lastMatrix[1,2]
				# print lastMatrix
				# gap += 1
				print "Error: could not converge"
			targetImage = img1Orig/255

			# registeredImage = cv2.warpAffine(img2Orig/255,warp_matrix,dsize = (cols,rows))
			# combined = targetImage.copy()
			# combined = (combined + registeredImage) / 2
			# cv2.namedWindow('ImageBoth', cv2.WINDOW_NORMAL)
			# cv2.imshow('ImageBoth', combined)

			if firstImage:
				currentMap = add_to_map_matrix(targetImage, currentMap, currentMatrix)
				firstImage = False

			matrix = np.eye(3)
			matrix[0:2,:] = warp_matrix

			currentMatrix = np.matmul(currentMatrix, matrix)
			lastMatrix = matrix
			
			currentMap = add_to_map_matrix(img2Orig/255, currentMap, currentMatrix)

			cv2.namedWindow('Map', cv2.WINDOW_NORMAL)
			cv2.imshow('Map', currentMap)
			cv2.waitKey(1)

		oldImage = image
		image = img
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
