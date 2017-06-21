# shared file between debug and main program to get binary image
import cv2 as cv
import numpy as np

# crops to isolate different colours
#CROP = [
#    [[466, 150], [633, 377]],  # yellow crop
#    [[0, 0], [100, 100]], # blue crop
#]

THRESH_FILENAME = "/home/ubuntu/car/computer/debug/thresholds.txt"

# bounds of colours (hsv) values (left track, right track, obstacle)
BOUNDS = [None] * 3

# kernel size for blur filter
KERNEL_SIZE = 5

def load_binary():
    global BOUNDS
    global KERNEL_SIZE

    # read arrays from file
    try:
        fd = open(THRESH_FILENAME)

        for i in range(len(BOUNDS)):
            BOUNDS[i] = eval(fd.readline())

        fd.close()
    except:
        print "Colour thresholds could not be loaded"
        raise

    # transform bounds into easy to use format
    for i in range(len(BOUNDS)):
        for j in range(len(BOUNDS[i])):
            BOUNDS[i][j] = np.array(BOUNDS[i][j])

def get_binary(frame, crop, bounds):
    # do a blur and convert colour space
    frame = cv.boxFilter(frame, -1, (KERNEL_SIZE, KERNEL_SIZE))
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # threshold images
    thresh = cv.inRange(frame, *BOUNDS[0])

#       frame[CROP[0][0][1]:CROP[0][1][1], CROP[0][0][0]:CROP[0][1][0]],

    return thresh
