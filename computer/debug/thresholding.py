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

def load_bounds():
    global BOUNDS
    global KERNEL_SIZE

    samples = [[]] * 3
    bounds = [[]] * 3

    # read arrays from file
    try:
        fd = open(THRESH_FILENAME, 'r')

        for i in range(len(BOUNDS)):
            bounds[i] = eval(fd.readline())

        for i in range(len(samples)):
            samples[i] = eval(fd.readline())

        fd.close()
    except:
        print "Colour thresholds could not be loaded"
        raise

    # convert bounds to numpy arrays
    BOUNDS = bounds[:][:]
    for i in range(len(BOUNDS)):
        for j in range(len(BOUNDS[i])):
            BOUNDS[i][j] = np.array(BOUNDS[i][j])
            bounds[i][j] = np.array(bounds[i][j])

    return (bounds, samples)

def apply_filters(frame):
    # do a blur and convert colour space
    # frame = cv.boxFilter(frame, -1, (KERNEL_SIZE, KERNEL_SIZE), normalize=True)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    return frame

def get_binary(frame, index, bounds=None, crop=None):
    # use default bounds if not specified
    #if bounds is None:
    #    bounds = BOUNDS

    # apply filters to image and convert colour space
    frame = apply_filters(frame)

    # threshold images
    thresh = cv.inRange(frame, *bounds[index])
#       frame[CROP[0][0][1]:CROP[0][1][1], CROP[0][0][0]:CROP[0][1][0]],

    return thresh
