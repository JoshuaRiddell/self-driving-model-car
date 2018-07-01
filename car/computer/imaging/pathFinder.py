
import cv2
import numpy as np
import time

PIXEL_TO_UNITY = 1.0/7.0

def threshold_image(img):
	redChan = img[:,:,0]
	blueChan = img[:,:,1]
	greenChan = img[:,:,2]
	#passed by reference so should auto update img
	redChan[redChan < 200] = 0
	blueChan[blueChan < 210] = 0
	greenChan[greenChan < 200] = 0 
	img /= 255.0

def perspecitve_warp(image, inverse=False):
	# pts0 = np.float32([[367, 864], [1585, 864], [1234, 592], [700, 592]])
	pts0 = np.float32([[145, 703], [1773, 703], [1258, 499], [660, 499]]) #square with side length 10 in unity

	cX = 250
	cY = 270
	L = 70 / 2 
	pts1 = np.float32([[cX - L , cY + L], [cX + L, cY + L], [cX + L, cY - L], [cX - L, cY - L]])
	if inverse:
		M = cv2.getPerspectiveTransform(pts1,pts0)
		newImage = cv2.warpPerspective(image,M, (1800, 1200))
	else:
		M = cv2.getPerspectiveTransform(pts0,pts1)
		newImage = cv2.warpPerspective(image,M, (500, 300))
	x = 150
	w = 200
	y = 0
	h = 250
	return newImage

def show_image(image):
	cv2.namedWindow('Image2', cv2.WINDOW_NORMAL)
	cv2.imshow('Image2', image)
	cv2.waitKey(0)


def fit_circle_2d(x, y, w=[]):
    
    A = np.array([x, y, np.ones(len(x))]).T
    b = x**2 + y**2
    
    # Modify A,b for weighted least squares
    if len(w) == len(x):
        W = np.diag(w)
        A = np.dot(W,A)
        b = np.dot(W,b)
    
    # Solve by method of least squares
    c = np.linalg.lstsq(A,b)[0]
    
    # Get circle parameters from solution c
    xc = c[0]/2
    yc = c[1]/2
    r = np.sqrt(c[2] + xc**2 + yc**2)
    return xc, yc, r

def threshold_obstacles(img):
	redChan = img[:,:,0]
	blueChan = img[:,:,1]
	greenChan = img[:,:,2]
	#passed by reference so should auto update img
	redExpected = 117 #expected purple colour for obstacles
	blueExpected = 44
	greenExpected = 69
	redThresh = 30
	blueThresh = 30
	greenThresh = 30
	mask = np.logical_or(np.logical_or(np.logical_or(redChan < redExpected - redThresh, redChan > redExpected + redThresh), 
										np.logical_or(blueChan < blueExpected - blueThresh, blueChan > blueExpected + blueThresh)), 
										np.logical_or(greenChan < greenExpected - greenThresh, greenChan > greenExpected + greenThresh))
	redChan[mask] = 0
	blueChan[mask] = 0
	greenChan[mask] = 0 
	img /= 255.0

STEERING_ANGLE_SHRINK_RATE = 0.2
def find_path(img, trackWidth = None, steeringAngle = 0):
	
	#warp the image to top down
	img1 = perspecitve_warp(img)
	h, w, d = img1.shape

	M = cv2.getRotationMatrix2D((w/2,h),STEERING_ANGLE_SHRINK_RATE*steeringAngle, 1)
	img1 = cv2.warpAffine(img1,M,dsize = (w,h))
	img1 = img1.astype('float32')
	obstacleImage = img1.copy()
	# print obstacleImage[150,250,:]
	# exit()
	threshold_obstacles(obstacleImage)
	obstacleImageGray = np.sum(obstacleImage, axis = 2)/3.0
	#get seperate images for the two lines
	threshold_image(img1)
	blueLineImage = img1[:,:,0]
	yellowLineImage = img1[:,:,1]
	
	
	
	# NOTE: THIS SECTION IS BY FAR THE SLOWEST PART
	
	#construct grid of indexes from 0 to h with width w
	blueIndexGrid = np.transpose(np.mgrid[0:w,0:h][0]).astype('float32') # takes approx 2ms
	# where the image has colour, leave the index, otherwise set it to nan
	blueIndexGrid[blueLineImage == 0] = np.nan # takes approx 0.4 ms
	# Take the median of all values with colour
	# This should be the center of the line for that row
	blueMedians = np.nanmedian(blueIndexGrid, axis = 1) # takes approx 5 ms

	yellowIndexGrid = np.transpose(np.mgrid[0:w,0:h][0]).astype('float32')
	yellowIndexGrid[yellowLineImage == 0] = np.nan
	yellowMedians = np.nanmedian(yellowIndexGrid, axis = 1)

	obstacleIndexGrid = np.transpose(np.mgrid[0:w,0:h][0]).astype('float32')
	obstacleIndexGrid[obstacleImageGray == 0] = 0
	rightObstacleSides = np.nanmax(obstacleIndexGrid, axis = 1)
	obstacleIndexGrid[obstacleImageGray == 0] = np.nan
	leftObstacleSides = np.nanmin(obstacleIndexGrid, axis = 1)

	# SLOW SECTION ENDS HERE

	points = []
	#probably a numpy way to avoid this for loop
	for i in range(0, img1.shape[0]): # for each row in the image
		#reverse the index so iterating bottom to top of image
		# i = img1.shape[0] - i - 1
		
		blueValue = blueMedians[i]
		yellowValue = yellowMedians[i]
		if np.isnan(blueValue):
			blueValue = None
		if np.isnan(yellowValue):
			yellowValue = None

		rightObstacleValue = rightObstacleSides[i]
		leftObstacleValue = leftObstacleSides[i]

		obstacleClearance = 20
		MIN_PATH_WIDTH = 50
		if rightObstacleValue != 0:
			#there is an obstacle on this section of track
			if blueValue is None and yellowValue is None:
				print "Both were none but obstacle detected"
				#do something here
			else:
				if blueValue is None:
					#the obstacle is covering the blue line
					blueValue = rightObstacleValue + obstacleClearance
					if (yellowValue - blueValue) < MIN_PATH_WIDTH:
						yellowValue = leftObstacleValue - obstacleClearance
						blueValue = None
					pass
				elif yellowValue is None:
					#the obstacle is covering the yellow line
					yellowValue = leftObstacleValue - obstacleClearance
					
					if (yellowValue - blueValue) < MIN_PATH_WIDTH:
						blueValue = rightObstacleValue + obstacleClearance
						yellowValue = None
					
				elif (yellowValue - rightObstacleValue) > (leftObstacleValue - blueValue):
					#there is more room to the right of the obstacle
					blueValue = rightObstacleValue + obstacleClearance
				else:
					#more room to left
					yellowValue = leftObstacleValue - obstacleClearance


		if blueValue is not None and yellowValue is not None:
			#if both found append the average of the two
			pt = (blueValue + yellowValue ) / 2.0
			#set the track width so we can extrapolate with it later
			trackWidth = yellowValue - blueValue

		elif trackWidth is not None:
			#if they are not both found but there is a track width, extrapolate using the previous trakWidth
			if blueValue is not None:
				pt = blueValue + trackWidth / 2.0
			elif yellowValue is not None:
				pt = yellowValue - trackWidth / 2.0
			else:
				continue
		else:
			#no point was added
			continue

		#if there are points not on the image ignore them. 
		#This can happen due to extrapolation with track width
		if pt < 0 or pt >= img1.shape[1]:
			continue

		#Convert the points from pixel to an x,y
		#origin is it at front of car, y positive up, x positive right
		y = i
		x = pt
		points.append([x - w/2, h-y])
		img1[int(y), int(x), :] = 1.0 # colour the point on the image to show path
	
	#if no points could be found, return straight
	if len(points) == 0:
		return 10000, img1
	#this is an analytic solution for fitting a circle to some points when 
	#we know the circle goes through the origin and the center is on the
	#x axis
	points = np.array(points)
	# numeratorSum = np.sum(np.power(points[:,0], 3) + np.power(points[:,1],2) * points[:,0])
	# denominatorSum = np.sum(np.power(points[:,0],2))

	numerator = np.power(points[:,0], 2) + np.power(points[:,1],2)
	numeratorSum = np.sum(numerator)
	denominatorSum = np.sum(points[:,0])
	radius = 0.5 * numeratorSum/denominatorSum

	# xc, yc, r = fit_circle_2d(points[:,0], points[:,1])
	# cv2.circle(img1, (int(w/2 + xc), h - int(yc)), int(abs(r)),(0,255,0))
	if abs(radius) < 100:
		radius = 10000
	#draw on the circular path
	img1 += obstacleImage
	cv2.circle(img1, (int(w/2 + radius), h), int(abs(radius)),(0,0,255)) 

	return radius * PIXEL_TO_UNITY, img1

if __name__=="__main__":

	for imageCounter in range(3, 4):
		im1Path = 'C:/Projects/self-driving-model-car/QUTDroidRacing/PythonTesting/unityTestImages2/img_%04d.jpg' % (imageCounter)
		scale = 1.0

		img1 = cv2.imread(im1Path, cv2.IMREAD_COLOR)
		start = time.clock()
		radius, image = find_path(img1)
		
		# image = perspecitve_warp(image, True)
		cv2.namedWindow('Image1', cv2.WINDOW_NORMAL)
		cv2.imshow('Image1', image)
		cv2.waitKey(0)
		