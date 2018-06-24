import cv2
import numpy as np
from imageManipulation import *
import csv

MAP_SIZE = (1000, 1000)
def construct_map(im1, courseMap, theta, xCentre, yCentre):
	rows, cols, channels = im1.shape
	#xCentre += 500/2
	#yCentre += 300/2
	print "theta, x , y: ", theta, xCentre, yCentre

	angleToCentre = np.rad2deg(np.arctan((rows/2)*1.0/(cols/2))) #angle from corner to centre of image

	radius = np.sqrt(cols*cols/4 + rows * rows / 4) # radius from corner to centre of image

	tX = xCentre - radius * np.cos(np.deg2rad(-theta + angleToCentre)) #coords of top left corner
	tY = yCentre - radius * np.sin(np.deg2rad(-theta + angleToCentre))

	M = cv2.getRotationMatrix2D((cols/2,rows/2),theta, 1) # rotation point, rotation angle, scale
	
	X_OFFSET = 300
	Y_OFFSET = 550  

	M[0,2] = tX + X_OFFSET
	M[1,2] = tY + Y_OFFSET
	print M
	transformedImage = cv2.warpAffine(im1,M,dsize = MAP_SIZE)
	
	registeredImage = transformedImage.astype('float32')


	# alpha = 0.5
	# beta = ( 1.0 - alpha );
	# imgToShow = cv2.addWeighted( registeredImage, alpha, courseMap, beta, 0.0)
	courseMapNew = courseMap + registeredImage
	courseMapNew[np.logical_and(registeredImage != 0, courseMap != 0)] /= 2
	return courseMapNew

if __name__ == "__main__":
	courseMap = np.zeros( (MAP_SIZE[0], MAP_SIZE[1], 3))

	with open('ImageTransformResultsLong2.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')

		lastTheta = 0
		lastX = 0
		lastY = 0

		mapInit = 0
		for row in reader:
			imageNumber = int(row[0])
			if mapInit == 0:
				im1Path = 'unityTestImages/img_%04d.jpg' % (imageNumber - 1)
				img = cv2.imread(im1Path, cv2.IMREAD_COLOR).astype('float32')
				img = perspecitve_warp(img)

				courseMap = construct_map(img/255, courseMap, 0, 500/2, 300/2)
				mapInit = 1
			im1Path = 'unityTestImages/img_%04d.jpg' % (imageNumber)
			img = cv2.imread(im1Path, cv2.IMREAD_COLOR).astype('float32')
			img = perspecitve_warp(img)

			theta = -float(row[1]) + lastTheta# + 12
			xCentre = -float(row[2]) + lastX# + 12
			yCentre = -float(row[3]) + lastY# - 42
			courseMap = construct_map(img/255, courseMap, theta, xCentre + 500/2, yCentre + 300/2)
			lastX = xCentre
			lastY = yCentre
			lastTheta = theta

		# cv2.namedWindow('RegisteredImages', cv2.WINDOW_NORMAL)
		cv2.imshow('RegisteredImages', courseMap)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		