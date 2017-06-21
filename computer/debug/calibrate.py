# uses chessboard to find a perspecive transform matrix

import numpy as np
import cv2
import glob

# termination criteria for sub pixel corner detection
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# size of the chessboard
size = (7,5)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((size[0]*size[1],3), np.float32)
objp[:,:2] = np.mgrid[0:size[0],0:size[1]].T.reshape(-1,2)

# camera resolution to use
resolution = (1920, 1080)

# setup camera
cam = cv2.VideoCapture(0)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920);
cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080);

# loop indefinitely for continuous camera feed
while True:
    # get a frame and convert to grayscale
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, size, flags=cv2.CALIB_CB_FAST_CHECK)

    # if found, add object points, image points (after refining them)
    if ret == True:
        # get chessboard corners with sub pixel accuracy
        ret, corners = cv2.findChessboardCorners(gray, size, flags=cv2.CALIB_CB_ADAPTIVE_THRESH)
        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

        # perpare arrays for mapping between chessboard and rectangle
        rectangle = np.array([corners[x] for x in (-7, 0, -1, 6)])
        dest = np.array([[670, 450], [1250, 450], [670, 970], [1250, 970]], dtype=np.float32)
        print rectangle

        # get the perspective matrix
        M = cv2.getPerspectiveTransform(rectangle, dest)
        warped = cv2.warpPerspective(img, M, resolution)

        # draw the chessboard corners on the image and display the warped image
        cv2.drawChessboardCorners(img, size, corners, ret)
        cv2.imshow('warped', warped)

    # show non-warped image
    cv2.imshow('img', img)

    # wait for 100ms or a key
    cv2.waitKey(100)

cv2.destroyAllWindows()
