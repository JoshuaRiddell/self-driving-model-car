# shared file between debug and main program to get binary image
import cv2 as cv
import numpy as np

# bounds of colours (hsv) values
BOUNDS = [
    [[ 26,  28, 178], [ 30, 238, 230]], # yellow
    [[0,0,0], [255,255,255]], # blue
]

# crops to isolate different colours
CROP = [
    [[466, 150], [633, 377]],  # yellow crop
    [[0, 0], [100, 100]], # blue crop
]

# kernel size for blur filter
KERNEL_SIZE = 5

# transform bounds into easy to use format
for i in range(len(BOUNDS)):
    for j in range(len(BOUNDS[i])):
        BOUNDS[i][j] = np.array(BOUNDS[i][j])

def get_binary(frame, crop, bounds):
    # do a blur and convert colour space
    frame = cv.boxFilter(frame, -1, (KERNEL_SIZE, KERNEL_SIZE))
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # threshold images
    thresh = cv.inRange(
        frame[CROP[0][0][1]:CROP[0][1][1], CROP[0][0][0]:CROP[0][1][0]],
        *BOUNDS[0])

    return thresh
