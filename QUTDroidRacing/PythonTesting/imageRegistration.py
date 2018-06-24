
import cv2
import numpy as np
import csv 
# import matplotlib.pyplot as plt

def estimate_pose(newImage, targetImage, theta = None):
	sz = newImage.shape
	newIm_gray = cv2.cvtColor(newImage,cv2.COLOR_BGR2GRAY)
	targetIm_gray = cv2.cvtColor(targetImage,cv2.COLOR_BGR2GRAY)

	# Define the motion model
	warp_matrix = np.eye(2, 3, dtype=np.float32)
	if theta is None:
		warp_mode = cv2.MOTION_EUCLIDEAN
	else:
		warp_mode = cv2.MOTION_EUCLIDEAN
		warp_matrix = cv2.getRotationMatrix2D((sz[0]/2, sz[1] + 50), -(theta), 1).astype('float32')[0:2,:]
		# warp_matrix = np.eye(2, 3, dtype=np.float32)
	# print "initiali matrix: ", warp_matrix

	# Specify the number of iterations.
	number_of_iterations = 500;
	 
	# Specify the threshold of the increment
	# in the correlation coefficient between two iterations
	termination_eps = 100000e-10;

	# Define termination criteria
	criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
	 
	# Run the ECC algorithm. The results are stored in warp_matrix.
	
	(cc, warp_matrix) = cv2.findTransformECC (newIm_gray,targetIm_gray,warp_matrix, warp_mode, criteria)
 
 	im2_aligned = cv2.warpAffine(targetImage, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);

	return warp_matrix


def threshold_image(img):
	redChan = img[:,:,0]
	blueChan = img[:,:,1]
	greenChan = img[:,:,2]
	mask = np.logical_and(np.logical_and(greenChan < 200, blueChan < 200), redChan < 200)
	greenChan[mask] = 0 #passed by reference so shoudl auto update img
	blueChan[mask] = 0
	redChan[mask] = 0
	img /= 255.0
	# print img

def perspecitve_warp(image):
	# pts0 = np.float32([[367, 864], [1585, 864], [1234, 592], [700, 592]])
	pts0 = np.float32([[145, 703], [1773, 703], [1258, 499], [660, 499]]) #square with side length 10 in unity

	cX = 250
	cY = 270
	L = 70 / 2 # Therefore 40 pixels = 10 unity units. Conversing from pixels to unity is / 4
	pts1 = np.float32([[cX - L , cY + L], [cX + L, cY + L], [cX + L, cY - L], [cX - L, cY - L]])
	M = cv2.getPerspectiveTransform(pts0,pts1)
	newImage = cv2.warpPerspective(image,M, (500, 300))
	x = 150
	w = 200
	y = 0
	h = 250
	return newImage#newImage[y:y+h, x:x+w]

MAP_SIZE = (300, 300)

def add_to_map(im1, courseMap, theta, xCentre, yCentre):

	X_OFFSET = 1000
	Y_OFFSET = 1000

	M = construct_matrix(im1, theta, xCentre, yCentre)
	M[0,2] += X_OFFSET
	M[1,2] += Y_OFFSET
	# print M
	transformedImage = cv2.warpAffine(im1,M,dsize = MAP_SIZE)
	
	registeredImage = transformedImage.astype('float32')

	courseMapNew = courseMap + registeredImage
	courseMapNew[np.logical_and(registeredImage != 0, courseMap != 0)] /= 2
	return courseMapNew

def add_to_map_matrix(im1, courseMap, M):
	# print M[0:2,:]
	transformedImage = cv2.warpAffine(im1,M[0:2,:],dsize = MAP_SIZE)
	
	registeredImage = transformedImage.astype('float32')

	courseMapNew = courseMap + registeredImage
	courseMapNew[np.logical_and(registeredImage != 0, courseMap != 0)] /= 2
	return courseMapNew

def construct_matrix(im1, theta, x, y):
	rows, cols, channels = im1.shape
	M = cv2.getRotationMatrix2D((cols/2,rows + 50), theta, 1)
	M2 = cv2.getRotationMatrix2D((cols/2,rows + 50), -theta, 1)
	M[0,2] = M2[0][0] * x + M2[0][1] * y
	M[1,2] = M2[1][0] * x + M2[1][1] * y
	return M


def get_initial_matrix(theta, img, velX = 0, velY = 0):
	rows, cols, channels = img1.shape
	M = cv2.getRotationMatrix2D((cols/2,rows + 5), theta, 1)
	return M

sigma = 5.0
def evaluate_estimate(theta, tX, tY, newImage, targetImage):
	rows, cols, channels = newImage.shape
	M = cv2.getRotationMatrix2D((cols/2,rows + 5),theta, 1) # rotation point, rotation angle, scale
	M[0,2] = tX
	M[1,2] = tY
	transformedImage = cv2.warpAffine(newImage,M,dsize = (cols,rows))
	registeredImage = transformedImage.astype('float32')
	diffBig = np.abs(targetImage - registeredImage) # TODO: Work out a way to ignore the black bits that come from the transformation. This will have all channels == 0
	# print diffBig
	pdf = np.exp(-diffBig / (2*sigma*sigma))
	# pdf = np.ones(pdf.shape)
	pdf[transformedImage == 0] = 0 # THIS COULD BE A SOLUTION, BUT THIS DOES IT FOR EACH CHANNEL. WANT TO ONLY 0 WHEN ALL CHANNELS ARE 0
	pdf[targetImage == 0] = 0 # THIS COULD BE A SOLUTION, BUT THIS DOES IT FOR EACH CHANNEL. WANT TO ONLY 0 WHEN ALL CHANNELS ARE 0
	total = np.sum(pdf)
	return total, registeredImage, pdf, M


def estimate_pose_2(img2, img1, theta = None):
	startTheta = -10.0
	dTheta = 1.0
	startX = -10
	dX = 1.0
	startY = -10
	dY = 1.0
	thetas = []
	tXs = []
	tYs = []
	totals = []
	for i in range(20):
		theta = startTheta + i * dTheta
		for j in range(20):
			tX = startX + j* dX
			for k in range(20):
				tY = startY + k * dY
				total, registeredImage, pdf, matrix = evaluate_estimate(theta, tX, tY, img2, img1)
				totals.append(total)
				thetas.append(theta)
				tXs.append(tX)
				tYs.append(tY)

				# logFile.write("%f, %f, %f, %f\n" % (theta, tX, tY, total))
	maxIndex = totals.index(max(totals))
	theta = thetas[maxIndex]
	tX = tXs[maxIndex]
	tY = tYs[maxIndex]
	total, registeredImage, pdf, matrix = evaluate_estimate(theta, tX, tY, img2, img1)
	return matrix

def estimate_pose_3(img1, img2):
	# Initiate STAR detector
	orb = cv2.ORB_create()
	# create BFMatcher object
	kp1Un, des1Un = orb.detectAndCompute(img1,None)
	kp2Un, des2Un = orb.detectAndCompute(img2,None)

	kp1 = []
	kp2 = []
	des1 = None
	des2 = None

	for i in range(len(kp1Un)):
		if (check_in_bounds(kp1Un[i].pt)):
			kp1.append(kp1Un[i])
			if des1 is None:
				des1 = des1Un[i,:]
			else:

				des1 = np.vstack((des1, des1Un[i,:]))
			# des1.append(des1Un[i])
	for i in range(len(kp2Un)):
		if (check_in_bounds(kp2Un[i].pt)):
			kp2.append(kp2Un[i])
			if des2 is None:
				des2 = des2Un[i,:]
			else:
				des2 = np.vstack((des2, des2Un[i,:]))

	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	# Match descriptors.
	matches = bf.match(des1,des2)
	# Sort them in the order of their distance.
	matches = sorted(matches, key = lambda x:x.distance)
	points1 = np.zeros((len(matches),2))
	points2 = np.zeros((len(matches),2))
	for i in range(len(matches)):
		match = matches[i]
		pt1 = kp1[match.queryIdx].pt
		pt2 = kp2[match.trainIdx].pt
		points1[i,:] = np.array([pt1[0], pt1[1]])
		points2[i,:] = np.array([pt2[0], pt2[1]])

	M, mask = cv2.findHomography(points1, points2,cv2.RANSAC,5.0)
	return M

def check_in_bounds(pt):
	x = pt[0]
	y = pt[1]
	x0, y0 = (0, 100)
	x1, y1 = (205, 299)
	x2, y2 = (295, 299)
	x3, y3 = (499, 100)
	
	m1 = (y1- y0) * 1.0 / (x1 - x0)
	c1 = y1 - m1 * x1

	m2 = (y3 - y2) * 1.0 / (x3 - x2)
	c2 = y2 - m2 * x2

	
	if (y > m1 * x + c1):
		return False
	if (y > m2 * x + c2):
		return False

	return True



def find_path(img):
	scale = 1.0
	img1 = perspecitve_warp(img)
	img1 = cv2.resize(img1, (0,0), fx=scale, fy=scale)
	img1Orig = img1.copy().astype('float32')/255
	img1 = img1.astype('float32')
	threshold_image(img1)
	imgGray = np.sum(img1, 2)/3.0

	h, w, d = img1.shape
	# cv2.namedWindow('ImageGray', cv2.WINDOW_NORMAL)
	# cv2.imshow('ImageGray', imgGray)
	a = np.transpose(np.nonzero(imgGray))
		# print a
	points = []
	for i in range(0, img1.shape[0]):
		nonZeroIndexes = a[a[:,0] == i][:,1]
		if nonZeroIndexes.shape[0]:
			points.append([i, np.average(nonZeroIndexes)])
			# print i, np.average(nonZeroIndexes)
		else:
			pass# print i, "No"

	goodPoints = []
	for pt in points:
		if np.all(img1[int(pt[0]), int(pt[1]), :] == 0.0):
			y = pt[0]
			x = pt[1]
			goodPoints.append([x - w/2, h-y])
			img1[int(pt[0]), int(pt[1]), :] = 1.0

	minScore = -1
	numeratorSum = 0
	denominatorSum = 0
	xs = []
	ys = []
	for pt in goodPoints:

		x = pt[0]
		y = pt[1]
		xs.append(x)
		ys.append(y)
		numeratorSum += (x*x*x + y*y*x)
		denominatorSum += (x*x)


	if denominatorSum < 10:
		radius = 500
	else:
		radius = abs(0.5 * numeratorSum/denominatorSum)

		scorePositive = 0
		scoreNegative = 0
		r = radius
		for pt in goodPoints:
			x = pt[0]
			y = pt[1]
			scorePositive += (x*x + 2*x*r + y*y) * (x*x + 2*x*r + y*y)
			scoreNegative += (x*x - 2*x*r + y*y) * (x*x - 2*x*r + y*y)
		print scorePositive, scoreNegative
		if scoreNegative < scorePositive:
			radius *= -1
	radius *= -1

	if (abs(radius) < 200):
		radius = 10000
	print "Radius: ", radius
	
	cv2.circle(img1, (int(w/2 + radius), h), int(abs(radius)),(0,0,255)) 
	cv2.namedWindow('Image1', cv2.WINDOW_NORMAL)
	cv2.imshow('Image1', img1)
	# plt.plot(xs, ys, '.')
	# plt.show()
	cv2.waitKey(1)
	return radius


SHOW_IMG_1 = True
SHOW_IMG_2 = True
SHOW_IMG_2_TRANS = False
SHOW_IMG_COMBINED = True
SHOW_IMG_PDF = True

if __name__=="__main__":


	for imageCounter in range(3, 400 ):
		im1Path = 'unityTestImages2/img_%04d.jpg' % (imageCounter)
		scale = 1.0

		img1 = cv2.imread(im1Path, cv2.IMREAD_COLOR)
		find_path(img1)
		# cv2.d 




	# for imageCounter in range(23, 300):
	# 	# imageCounter = 23
	# 	gap = 1
	# 	im1Path = 'unityTestImages2/img_%04d.jpg' % (imageCounter - gap)
	# 	im2Path = 'unityTestImages2/img_%04d.jpg' % (imageCounter)
	# 	scale = 1.0

	# 	img1 = cv2.imread(im1Path, cv2.IMREAD_COLOR)
	# 	img1 = perspecitve_warp(img1)
	# 	img1 = cv2.resize(img1, (0,0), fx=scale, fy=scale)
	# 	img1Orig = img1.copy().astype('float32')/255
	# 	# img1 = img1.astype('float32')
	# 	# threshold_image(img1)
		
	# 	# rows,cols,chans = img1.shape

	# 	img2 = cv2.imread(im2Path, cv2.IMREAD_COLOR)
	# 	img2 = perspecitve_warp(img2)
	# 	img2 = cv2.resize(img2, (0,0), fx=scale, fy=scale)
	# 	img2Orig = img2.copy().astype('float32')/255
	# 	# img2 = img2.astype('float32')
	# 	# threshold_image(img2)
		
	# 	M = estimate_pose_3(img1, img2)	
	# 	rows,cols,chans = img1.shape
	# 	# M[2,0] = 0
	# 	# M[2,1] = 0

	# 	registeredImage = cv2.warpPerspective(img1Orig,M,dsize = (cols,rows))
	# 	combined = img2Orig.copy()
	# 	combined = (combined + registeredImage) / 2
	# 	cv2.namedWindow('ImageBoth', cv2.WINDOW_NORMAL)
	# 	cv2.imshow('ImageBoth', combined)

	# 	# Draw first 10 matches.

	# 	# img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:20], None, flags=2)

	# 	# cv2.namedWindow('Image3', cv2.WINDOW_NORMAL)
	# 	# cv2.imshow('Image3', img3)
	# 	cv2.waitKey(0)
	# 	# cv2.d 

	# if SHOW_IMG_1:
	# 	cv2.namedWindow('Image1', cv2.WINDOW_NORMAL)
	# 	cv2.imshow('Image1', img1)
	# if SHOW_IMG_2:
	# 	cv2.namedWindow('Image2', cv2.WINDOW_NORMAL)
	# 	cv2.imshow('Image2', img2)

	# logFile = open("logFile.csv", "w")
	# startTheta = -10.0
	# dTheta = 1.0
	# startX = -25
	# dX = 1.0
	# startY = -25
	# dY = 1.0
	# thetas = []
	# tXs = []
	# tYs = []
	# totals = []
	# for i in range(20):
	# 	theta = startTheta + i * dTheta
	# 	for j in range(50):
	# 		tX = startX + j* dX
	# 		for k in range(50):
	# 			tY = startY + k * dY
	# 			total, registeredImage, pdf, matrix = evaluate_estimate(theta, tX, tY, img2, img1)
	# 			totals.append(total)
	# 			thetas.append(theta)
	# 			tXs.append(tX)
	# 			tYs.append(tY)

	# 			logFile.write("%f, %f, %f, %f\n" % (theta, tX, tY, total))
	# maxIndex = totals.index(max(totals))
	# theta = thetas[maxIndex]
	# tX = tXs[maxIndex]
	# tY = tYs[maxIndex]
	# total, registeredImage, pdf, matrix = evaluate_estimate(theta, tX, tY, img2, img1)


	# rows, cols, channels = img2Orig.shape
	# registeredImage = cv2.warpAffine(img2Orig, matrix,dsize = (cols,rows))
	
	# print total

	# if SHOW_IMG_PDF:
	# 	cv2.namedWindow('PDF', cv2.WINDOW_NORMAL)
	# 	cv2.imshow('PDF', pdf)

	# # M = get_initial_matrix(0, img2Orig)

	# # print img2Orig.shape
	# # transformedImage = cv2.warpAffine(img2Orig,M, dsize = (50,30))

	# # if SHOW_IMG_2_TRANS:
	# # 	cv2.namedWindow('Image2Transformed', cv2.WINDOW_NORMAL)
	# # 	cv2.imshow('Image2Transformed', transformedImage)

	# combined = img1Orig.copy()
	# combined = (combined + registeredImage) / 2
	# if SHOW_IMG_COMBINED:
	# 	cv2.namedWindow('Combined', cv2.WINDOW_NORMAL)
	# 	cv2.imshow('Combined', combined)

	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	# exit()





	# currentMap = np.zeros((MAP_SIZE[0], MAP_SIZE[1], 3))
	# firstImage = True
	# oldTheta = 0
	# oldX = 0
	# oldY = 0

	# currentMatrix = np.eye(3)
	# currentMatrix[0,2] = 50
	# currentMatrix[1,2] = 100
	
	# gap = 1

	# # imNumbers = []
	# # thetas = []
	# # xs = []
	# # ys = []
	# # zs = []
	# # with open('unityTestImages2/telmetry.csv', 'rb') as csvfile:
	# # 	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	# # 	for row in reader:
	# # 		# imNumbers.append(int(row[0]))
	# # 		t = float(row[1])
	# # 		if (t > 180):
	# # 			t -= 360
	# # 		thetas.append(t)
	# # 		xs.append(float(row[2]))
	# # 		ys.append(float(row[3]))
	# # 		zs.append(float(row[4]))


	# baseImageStr = "unityTestImages2/registrations/img_%04d.jpg"
	# for imageCounter in range(3,300,gap):
	# 	# currentIndex = imNumbers.index(imageCounter)

	# 	im1Path = 'unityTestImages2/img_%04d.jpg' % (imageCounter - gap)
	# 	im2Path = 'unityTestImages2/img_%04d.jpg' % (imageCounter)
	# 	# print im1Path
	# 	img1 = cv2.imread(im1Path, cv2.IMREAD_COLOR)

	# 	img1 = perspecitve_warp(img1)
	# 	scale = 0.1
	# 	img1 = cv2.resize(img1, (0,0), fx=scale, fy=scale)
	# 	img1Orig = img1.copy().astype('float32')
	# 	img1 = img1.astype('float32')
	# 	threshold_image(img1)
		

	# 	rows,cols,chans = img1.shape

	# 	img2 = cv2.imread(im2Path, cv2.IMREAD_COLOR)
	# 	img2 = perspecitve_warp(img2)
	# 	img2 = cv2.resize(img2, (0,0), fx=scale, fy=scale)
	# 	img2Orig = img2.copy().astype('float32')
	# 	img2 = img2.astype('float32')
	# 	threshold_image(img2)
		

	# 	# try:
	# 		# dTheta = thetas[currentIndex] - thetas[currentIndex - gap]
	# 		# if dTheta < -180:
	# 		# 	dTheta += 360
	# 		# elif dTheta > 180:
	# 		# 	dTheta -= 360
	# 		# print "Theta: ", dTheta
	# 	warp_matrix = estimate_pose_2(img2, img1, 0)
	# 	print warp_matrix
	# 	gap = 1
	# 	# except:
	# 	# 	sz = img1.shape
	# 	# 	# warp_matrix = cv2.getRotationMatrix2D((sz[0]/2, sz[1]/2), -(dTheta), 1).astype('float32')[0:2,:]
	# 	# 	warp_matrix[0,2] = lastMatrix[0,2]
	# 	# 	warp_matrix[1,2] = lastMatrix[1,2]
	# 	# 	# print lastMatrix
	# 	# 	# gap += 1
	# 	# 	print "Error: could not converge"
	# 		# continue
	# 		# use the same warp matrix again

	# 	# print warp_matrix
	# 	targetImage = img1Orig/255

	# 	# registeredImage = cv2.warpAffine(img2Orig/255,warp_matrix,dsize = (cols,rows))
	# 	# combined = targetImage.copy()
	# 	# combined = (combined + registeredImage) / 2
	# 	# cv2.namedWindow('ImageBoth', cv2.WINDOW_NORMAL)
	# 	# cv2.imshow('ImageBoth', combined)
	# 	# print "saving image: ", baseImageStr % (imageCounter)
	# 	# # print combined
	# 	# cv2.imwrite(baseImageStr % (imageCounter), combined*255)
	# 	if firstImage:
	# 		currentMap = add_to_map_matrix(targetImage, currentMap, currentMatrix)
	# 		# currentMap = add_to_map(targetImage, currentMap, 0, 0, 0)
	# 		firstImage = False

	# 	matrix = np.eye(3)
	# 	matrix[0:2,:] = warp_matrix

	# 	currentMatrix = np.matmul(currentMatrix, matrix)
	# 	lastMatrix = matrix
	# 	# print warp_matrix

	# 	currentMap = add_to_map_matrix(img2Orig/255, currentMap, currentMatrix)
	# 	# print theta, tX, tY
	# 	# currentMap = add_to_map(img2Orig/255, currentMap, theta, tX, tY)

	# 	# oldX = tX
	# 	# oldY = tY
	# 	# oldTheta = theta

	# 	cv2.namedWindow('Map', cv2.WINDOW_NORMAL)
	# 	cv2.imshow('Map', currentMap)
	# 	cv2.waitKey(5)
	# 	# exit()
	# 	# cv2.destroyAllWindows()
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()











# if __name__=="__main__":
# 	imageCounter = 48
# 	im1Path = 'unityTestImages/img_%04d.jpg' % (imageCounter)
# 	im2Path = 'unityTestImages/img_%04d.jpg' % (imageCounter + 1)
# 	print im1Path
# 	img1 = cv2.imread(im1Path, cv2.IMREAD_COLOR)

# 	img1 = perspecitve_warp(img1)

# 	img1Orig = img1.copy().astype('float32')
# 	threshold_image(img1)
# 	img1 = img1.astype('float32')

# 	rows,cols,chans = img1.shape

# 	img2 = cv2.imread(im2Path, cv2.IMREAD_COLOR)
# 	img2 = perspecitve_warp(img2)
# 	img2Orig = img2.copy().astype('float32')
# 	threshold_image(img2)
# 	img2 = img2.astype('float32')

# 	try:
# 		warp_matrix = estimate_pose(img1, img2)
# 	except:
# 		print "Error: could not converge"
# 		exit()

# 	print warp_matrix
# 	targetImage = img2Orig/255

# 	# registeredImage = cv2.warpAffine(img1Orig/255,warp_matrix,dsize = (cols,rows))

# 	# cv2.namedWindow('ImageReg', cv2.WINDOW_NORMAL)
# 	# cv2.imshow('ImageReg', registeredImage)

# 	# cv2.namedWindow('ImageTarget', cv2.WINDOW_NORMAL)
# 	# cv2.imshow('ImageTarget', targetImage)

# 	# combined = targetImage.copy()
# 	# combined = (combined + registeredImage) / 2
# 	# cv2.namedWindow('ImageBoth', cv2.WINDOW_NORMAL)
# 	# cv2.imshow('ImageBoth', combined)

# 	tX = warp_matrix[0][2]
# 	tY = warp_matrix[1][2]
# 	theta = -np.rad2deg(np.arccos(warp_matrix[0][0]))

# 	currentMap = np.zeros((MAP_SIZE[0], MAP_SIZE[1], 3))
# 	currentMap = add_to_map(targetImage, currentMap, 0, 0, 0)
# 	currentMap = add_to_map(img1Orig/255, currentMap, theta, tX, tY)
# 	cv2.namedWindow('Map', cv2.WINDOW_NORMAL)
# 	cv2.imshow('Map', currentMap)
# 	cv2.waitKey(0)
# 	cv2.destroyAllWindows()