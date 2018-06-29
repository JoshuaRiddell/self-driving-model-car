
import cv2
import numpy as np
from matplotlib import pyplot as plt
from unityCamera import UnityCamera

sigma = 0.001

SHOW_FINAL = True
LOG_RESULTS = True
RUN_OPTIMIZATION = True
SHOW_ALL_PLOTS = False
SHOW_DIFF = True
SHOW_THRESHOLDED_IMAGES = False

def evaluate_estimate(theta, xCentre, yCentre, newImage, targetImage):
	rows, cols, channels = newImage.shape
	
	angleToCentre = np.rad2deg(np.arctan((rows/2)*1.0/(cols/2))) #angle from corner to centre of image

	radius = np.sqrt(cols*cols/4 + rows * rows / 4) # radius from corner to centre of image

	tX = xCentre - radius * np.cos(np.deg2rad(-theta + angleToCentre)) #coords of top left corner
	tY = yCentre - radius * np.sin(np.deg2rad(-theta + angleToCentre))

	M = cv2.getRotationMatrix2D((cols/2,rows/2),theta, 1) # rotation point, rotation angle, scale
	M[0,2] = tX
	M[1,2] = tY

	transformedImage = cv2.warpAffine(newImage,M,dsize = (cols,rows))


	registeredImage = transformedImage.astype('float32')

	# cv2.namedWindow('RegisteredImages', cv2.WINDOW_NORMAL)
	# cv2.imshow('RegisteredImages',registeredImage)
		
	# cv2.namedWindow('target', cv2.WINDOW_NORMAL)
	# cv2.imshow('target',targetImage)
	diffBig = np.abs(targetImage/255.0 - registeredImage/255.0) # TODO: Work out a way to ignore the black bits that come from the transformation. This will have all channels == 0

	# print np.sum(diffBig == 0) + np.sum(diffBig == 1)
	# cv2.namedWindow('diff', cv2.WINDOW_NORMAL)
	# cv2.imshow('diff',diffBig)

	pdf = np.exp(-diffBig / (2*sigma*sigma))
	pdf = np.ones(pdf.shape)
	pdf[transformedImage == 0] = 0 # THIS COULD BE A SOLUTION, BUT THIS DOES IT FOR EACH CHANNEL. WANT TO ONLY 0 WHEN ALL CHANNELS ARE 0
	pdf[targetImage == 0] = 0 # THIS COULD BE A SOLUTION, BUT THIS DOES IT FOR EACH CHANNEL. WANT TO ONLY 0 WHEN ALL CHANNELS ARE 0
	total = np.sum(pdf)
	# print total
	# cv2.namedWindow('pdf', cv2.WINDOW_NORMAL)
	# cv2.imshow('pdf', pdf)
	# cv2.waitKey(0) 
	# cv2.destroyAllWindows()
	# exit()

	return total, registeredImage, pdf


def estimate_pose(newImage, targetImage):

	thetaStart = 0
	xCentreStart = 0
	yCentreStart = 0

	if LOG_RESULTS:
		logFile = open("ResultsUnity2.csv", "w")
		# logFile.write("Theta, X, Y, Score\n")

	bestTheta = None
	bestX = None
	bestY = None
	bestScore = None

	nThetaTrials = 10
	nXTrials = 10
	nYTrials = 10

	thetaLimits  = (-10,10)
	xLimits = (-50, 50)
	yLimits = (-50, 50)
	for dTheta in np.linspace(thetaLimits[0],thetaLimits[1],nThetaTrials):
		print dTheta
		for dX in np.linspace(xLimits[0], xLimits[1],nXTrials):#range(-20, 20, 5):
			for dY in np.linspace(yLimits[0], yLimits[1],nYTrials):#range(-40, 40, 3):
				theta = thetaStart + dTheta
				xCentre = cols/2 + xCentreStart + dX
				yCentre = rows/2 + yCentreStart + dY

				total, a, b = evaluate_estimate(theta, xCentre, yCentre, newImage, targetImage)
				
				if bestScore is None or total > bestScore:
					bestTheta = theta
					bestX = xCentre
					bestY = yCentre
					bestScore = total
				results = "%f, %f, %f, %f\n" % (theta, xCentre, yCentre, total)
				
				if LOG_RESULTS:
					logFile.write(results)

				# print results


	theta = bestTheta
	xCentre = bestX
	yCentre = bestY
	print "theta: ", theta
	dX = xCentre - cols/2
	print "dX: ", dX
	dY = yCentre - rows/2
	print "dY: ", dY

	print "Optimal probability of %f with theta = %f, X = %f, Y = %f\n" % (bestScore, theta, xCentre, yCentre)
	return bestTheta, dX, dY, bestScore

def estimate_pose_2(newImage, targetImage):
	sz = newImage.shape
	im1_gray = cv2.cvtColor(newImage,cv2.COLOR_BGR2GRAY)
	im2_gray = cv2.cvtColor(targetImage,cv2.COLOR_BGR2GRAY)
 # 	cv2.imshow("Image 1r", newImage[:,:,0])
 # 	cv2.imshow("Image 1g", newImage[:,:,1])
 # 	cv2.imshow("Image 1b", newImage[:,:,2])
	# cv2.imshow("Image 2", im2_gray)

	# cv2.waitKey(0)

	# Define the motion model
	warp_mode = cv2.MOTION_EUCLIDEAN
	warp_matrix = np.eye(2, 3, dtype=np.float32)
	# Specify the number of iterations.
	number_of_iterations = 500;
	 
	# Specify the threshold of the increment
	# in the correlation coefficient between two iterations
	termination_eps = 1e-10;

	# Define termination criteria
	criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
	 
	# Run the ECC algorithm. The results are stored in warp_matrix.
	(cc, warp_matrix) = cv2.findTransformECC (im1_gray,im2_gray,warp_matrix, warp_mode, criteria)
 
 	im2_aligned = cv2.warpAffine(targetImage, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);
 # 	cv2.imshow("Image 1", newImage)
	# cv2.imshow("Image 2", targetImage)
	# im2_aligned += newImage
	# im2_aligned /= 2
 # 	cv2.imshow("Aligned Image 2", im2_aligned)
	# cv2.waitKey(0)
	return warp_matrix

def perspecitve_warp(image):
	# pts0 = np.float32([[367, 864], [1585, 864], [1234, 592], [700, 592]])
	pts0 = np.float32([[145, 703], [1773, 703], [1258, 499], [660, 499]]) #square with side length 10 in unity

	cX = 250
	cY = 270
	L = 70 / 2 # Therefore 40 pixels = 10 unity units. Conversing from pixels to unity is / 4
	pts1 = np.float32([[cX - L , cY + L], [cX + L, cY + L], [cX + L, cY - L], [cX - L, cY - L]])
	M = cv2.getPerspectiveTransform(pts0,pts1)

	return cv2.warpPerspective(image,M, (500, 300))

def stitch_images(im1, courseMap, theta, xCentre, yCentre):
	rows, cols, channels = im1.shape
	print "Theta, x, y, :",  theta, xCentre, yCentre
	angleToCentre = np.rad2deg(np.arctan((rows/2)*1.0/(cols/2))) #angle from corner to centre of image

	radius = np.sqrt(cols*cols/4 + rows * rows / 4) # radius from corner to centre of image

	tX = xCentre - radius * np.cos(np.deg2rad(-theta + angleToCentre)) #coords of top left corner
	tY = yCentre - radius * np.sin(np.deg2rad(-theta + angleToCentre))

	M = cv2.getRotationMatrix2D((cols/2,rows/2),theta, 1) # rotation point, rotation angle, scale
	
	X_OFFSET = 500
	Y_OFFSET = 500
	OUTPUT_SIZE = (1000,1000)

	M[0,2] = tX + X_OFFSET
	M[1,2] = tY + Y_OFFSET
	print M
	transformedImage = cv2.warpAffine(im1,M,dsize = OUTPUT_SIZE)
	
	


	registeredImage = transformedImage.astype('float32')


	# alpha = 0.5
	# beta = ( 1.0 - alpha );
	# imgToShow = cv2.addWeighted( registeredImage, alpha, courseMap, beta, 0.0)
	courseMap = courseMap + registeredImage
	courseMap[registeredImage != 0] /= 2
	imgToShow = courseMap
	cv2.namedWindow('RegisteredImages', cv2.WINDOW_NORMAL)
	cv2.imshow('RegisteredImages',imgToShow)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	# exit()

if __name__ == "__main__":
	resultsFile = open("ImageTransformResultsLong2.csv", "w", 0)
	# resultsFile.write("Image, theta, x, y, score\n")
	for imageCounter in range(48, 66):
		#img = cv2.imread('star20_100_100.jpg', cv2.IMREAD_COLOR)
		im1Path = 'unityTestImages/img_%04d.jpg' % (imageCounter)
		im2Path = 'unityTestImages/img_%04d.jpg' % (imageCounter + 1)
		print im1Path
		img = cv2.imread(im1Path, cv2.IMREAD_COLOR)
		# img = cv2.resize(img, (0,0), fx=0.2, fy=0.2)
		# img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		img = perspecitve_warp(img)
		
		imgOrig = img.copy().astype('float32')

		# cv2.imwrite('afterHomography.jpg', img)
		# cv2.namedWindow('Image 1', cv2.WINDOW_NORMAL)
		# cv2.imshow('Image 1', img)

		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
		# exit()
		# a, img = cv2.threshold(img[:,:,0],110,255,cv2.THRESH_BINARY)
		redChan = img[:,:,0]
		blueChan = img[:,:,1]
		greenChan = img[:,:,2]
		greenChan[greenChan < 200] = 0 #passed by reference so shoudl auto update img
		blueChan[blueChan < 200] = 0
		redChan[redChan < 200] = 0
		# img = redChan
		if SHOW_THRESHOLDED_IMAGES:
			cv2.namedWindow('Image 1', cv2.WINDOW_NORMAL)
			cv2.imshow('Image 1', img)

		img = img.astype('float32')


		rows,cols,chans = img.shape

		# img2 = cv2.imread('star.jpg', cv2.IMREAD_COLOR)
		img2 = cv2.imread(im2Path, cv2.IMREAD_COLOR)
		# img = cv2.resize(img, (0,0), fx=0.2, fy=0.2)
		# img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
		img2 = perspecitve_warp(img2)
		img2Orig = img2.copy().astype('float32')
		redChan = img2[:,:,0]
		blueChan = img2[:,:,1]
		greenChan = img2[:,:,2]
		greenChan[greenChan < 200] = 0 #passed by reference so shoudl auto update img
		blueChan[blueChan < 200] = 0
		redChan[redChan < 200] = 0

		# cv2.imwrite('afterHomography.jpg', img)
		a, img2 = cv2.threshold(img2,100,150,cv2.THRESH_BINARY)
		if SHOW_THRESHOLDED_IMAGES:
			cv2.namedWindow('Image 2', cv2.WINDOW_NORMAL)
			cv2.imshow('Image 2', img2)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
			exit()
		img2 = img2.astype('float32')

		try:
			warp_matrix = estimate_pose_2(img, img2)
		except:
			print "Error: could not converge"
			continue
		print warp_matrix
		targetImage = img2Orig/255
		registeredImage = cv2.warpAffine(imgOrig/255,warp_matrix,dsize = (cols,rows))
		cv2.namedWindow('Image reg', cv2.WINDOW_NORMAL)
		cv2.imshow('Image reg', registeredImage)
		cv2.namedWindow('Image un', cv2.WINDOW_NORMAL)
		cv2.imshow('Image un', targetImage)
		combined = targetImage.copy()
		combined = (combined + registeredImage) / 2
		cv2.namedWindow('Image com', cv2.WINDOW_NORMAL)
		cv2.imshow('Image com', combined)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		tX = warp_matrix[0][2] - 500
		tY = warp_matrix[1][2] - 500
		theta = -np.rad2deg(np.arccos(warp_matrix[0][0]))

		rows, cols, channels = combined.shape
		angleToCentre = np.rad2deg(np.arctan((rows/2)*1.0/(cols/2))) #angle from corner to centre of image

		radius = np.sqrt(cols*cols/4 + rows * rows / 4) # radius from corner to centre of image

		xCentre = tX + radius * np.cos(np.deg2rad(-theta + angleToCentre))  #coords of top left corner
		yCentre = tY + radius * np.sin(np.deg2rad(-theta + angleToCentre))


		score = 0
		print "theta, x, y, ", theta, xCentre, yCentre
		resultsFile.write("%d, %f, %f, %f, %f\n" % (imageCounter + 1, theta, xCentre, yCentre, score))
			
		# continue
		# exit()

		# print img.shape 
		# if RUN_OPTIMIZATION:
		# 	theta, xCentre, yCentre, score = estimate_pose(img, img2)
		# 	resultsFile.write("%d, %f, %f, %f, %f\n" % (imageCounter + 1, theta, xCentre, yCentre, score))
		# 	continue
		# else:
		# 	theta = -3.33
		# 	xCentre  = cols/2 + 5.555
		# 	yCentre = rows/2 + 38.8888


		if SHOW_FINAL:

			# # total, dst, diff = evaluate_estimate(theta, xCentre - cols/2, yCentre - rows/2, imgOrig/255, img2Orig/255)
			# # total, b, diff = evaluate_estimate(theta, xCentre-cols/2, yCentre-rows/2, img, img2)
			# print "Score: ", total
			print rows, cols
			courseMap = np.zeros((1000,1000,3))

			M2 = cv2.getRotationMatrix2D((cols/2,rows/2),0, 1)
			M2[0,2] = 0 + 500
			M2[1,2] = 0 + 500
			courseMap += cv2.warpAffine(img2Orig/255,M2,dsize =(1000,1000))
			stitch_images(imgOrig/255, courseMap, theta, xCentre + cols/2, yCentre+rows/2)
			continue
			# needed_multi_channel_img = np.zeros((img.shape[0], img.shape[1], 3))

			# needed_multi_channel_img [:,:,0] = (dst[:,:,0]*1.0/255/3 + dst[:,:,1]*1.0/255/3 + dst[:,:,2]*1.0/255/3)
			# needed_multi_channel_img [:,:,2] = (img2[:,:,0]*1.0/255/3 + img2[:,:,1]*1.0/255/3 + img2[:,:,2]*1.0/255/3)
			# imgToShow = needed_multi_channel_img
			alpha = 0.5
			beta = ( 1.0 - alpha );
	 		imgToShow = cv2.addWeighted( dst, alpha, img2Orig/255, beta, 0.0)
			
			if SHOW_ALL_PLOTS:
				plt.subplot(131),plt.imshow(img2.astype('uint8'),'gray'),plt.title('Target')
				plt.axis('off')
				plt.subplot(132),plt.imshow(img.astype('uint8'),'gray'),plt.title('New')
				plt.axis('off')
				plt.subplot(133),plt.imshow(imgToShow,'gray'),plt.title('Registered')
				plt.axis('off')
				plt.tight_layout()
				plt.show()
			elif SHOW_DIFF:
				cv2.namedWindow('Diff', cv2.WINDOW_NORMAL)
				cv2.imshow('Diff',diff)
				# cv2.waitKey(0)
				# cv2.destroyAllWindows()
			cv2.namedWindow('Orig1', cv2.WINDOW_NORMAL)
			cv2.imshow('Orig1', imgOrig/255)
			cv2.namedWindow('Orig2', cv2.WINDOW_NORMAL)
			cv2.imshow('Orig2', img2Orig/255)
			cv2.namedWindow('RegisteredImages', cv2.WINDOW_NORMAL)
			cv2.imshow('RegisteredImages',imgToShow)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
					

			# cv2.namedWindow('newImage', cv2.WINDOW_NORMAL)
			# cv2.imshow('newImage',img.astype('uint8'))

			# cv2.namedWindow('targetImage', cv2.WINDOW_NORMAL)
			# cv2.imshow('targetImage',img2.astype('uint8'))
			