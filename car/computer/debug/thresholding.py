# shared file between debug and main program to get binary image
import cv2 as cv
import numpy as np
import getpass
from math import atan2, sqrt, pi

user = getpass.getuser()

# crops to isolate different colours
#CROP = [
#    [[466, 150], [633, 377]],  # yellow crop
#    [[0, 0], [100, 100]], # blue crop
#]

THRESH_FILENAME = "/home/" + user + "/rsync_car/car/computer/debug/thresholds.txt"
if user == 'BBL':
    THRESH_FILENAME = "/Users/BBL/Projects/self-driving-model-car/car/computer/debug/thresholds.txt"
# bounds of colours (hsv) values (left track, right track, obstacle)
NUM_BOUNDS = 3
BOUNDS = [None] * NUM_BOUNDS

# kernel size for blur filter
KERNEL_SIZE = 2
KERNEL = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)

# kernel size to downsample at the end
DOWNSAMPLE_SIZE = 15
SUM_SCALE = DOWNSAMPLE_SIZE**2
SUM_THRESHOLD = (DOWNSAMPLE_SIZE**2) * 255 * 0.5

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

def get_binary(frame, index=None, bounds=None, crop=None):
    # use default bounds if not specified
    if bounds is None:
        bounds = BOUNDS

    # apply filters to image and convert colour space
    new_frame = apply_filters(frame)

    # threshold images
    threshs = []
    # print bounds
    for bound in bounds:
        print bound
        threshs.append(cv.inRange(new_frame, *bound))
#           frame[CROP[0][0][1]:CROP[0][1][1], CROP[0][0][0]:CROP[0][1][0]],
    print len(threshs)
    return threshs

def apply_morph(threshs):
    for i in range(len(threshs)):
        threshs[i] = cv.erode(threshs[i], KERNEL, iterations = 1)
    return threshs

def downsample(threshs):
    # width = threshs[0].shape[0] / DOWNSAMPLE_SIZE
    # height = threshs[0].shape[1] / DOWNSAMPLE_SIZE

    # unit = [[0] * height] * width
    # matrices = [unit] * NUM_BOUNDS
    # for i in range(len(matrices)):
    #     matrices[i] = np.array(matrices[i], np.uint8)

    #     matrices[i] = np.zeros((width, height))

    # for i in range(len(matrices)):
    #     for j in range(width):
    #         for k in range(height):
    #             matrices[i][j][k] = np.sum(threshs[i][
    #                 j*DOWNSAMPLE_SIZE:(j+1)*DOWNSAMPLE_SIZE,
    #                 k*DOWNSAMPLE_SIZE:(k+1)*DOWNSAMPLE_SIZE]) \
    #                 / SUM_SCALE

    bblMatrices = []
    for i in range(len(threshs)):

        small = cv.resize(threshs[i], (0,0), fx=1.0/DOWNSAMPLE_SIZE, fy=1.0/DOWNSAMPLE_SIZE)  #resize image to hald
        bblMatrices.append(small)

    return bblMatrices

DISTANCE_SCALE = 1
INTENSITY_SCALE = 1 / float(254)
CALC_THRESHOLD = 30

def get_vector(pos, matrix):
    width = matrix.shape[0]
    height = matrix.shape[1]

    vect = [0, 0]

    bblMatrix = matrix.copy()
    bblMatrix[bblMatrix <= CALC_THRESHOLD] = 0

    xIndexGrid = np.transpose(np.mgrid[0:height,0:width][0]).astype('float32') # X positions of pixels
    yIndexGrid = np.mgrid[0:width,0:height][0].astype('float32') # y positions of pixels
    
    xIndexGrid = xIndexGrid - pos[0] #translate by centroid
    yIndexGrid = yIndexGrid - pos[1]

    xIndexGrid[bblMatrix == 0] = 0
    yIndexGrid[bblMatrix == 0] = 0

    dist = np.abs(xIndexGrid) + np.abs(yIndexGrid)
    zeroDists = dist == 0

    dist[dist == 0] = 1
    scale = DISTANCE_SCALE / dist * bblMatrix * INTENSITY_SCALE
    scale[zeroDists] = 0
    xIndexGrid = xIndexGrid * scale
    yIndexGrid = yIndexGrid * scale

    return np.array([np.sum(xIndexGrid), np.sum(yIndexGrid)], dtype = np.float)


    #pos is the starting position in pixels
    # for i in range(width):
    #     for j in range(height):
    #         if matrix[i][j] > CALC_THRESHOLD:
    #             x_diff = j - pos[0] 
    #             y_diff = i - pos[1]

    #             dist = abs(x_diff) + abs(y_diff)

    #             if dist == 0:
    #                 continue

    #             scale = DISTANCE_SCALE / float(dist) * \
    #                     matrix[i][j] * INTENSITY_SCALE

    #             vect[0] += x_diff * scale
    #             vect[1] += y_diff * scale
    #             # print "coord ({0}, {1}) ({2}, {3}) - {4} - {5}".format(i, j, x_diff, y_diff, matrix[i][j], scale)

    # print vect
    return np.array(vect, np.float)

def generate_direction(position, matrices):
    left = get_vector(position, matrices[0])
    right = get_vector(position, matrices[1])
    obstacle = get_vector(position, matrices[2])


    vectors = [left, right]

    angles = [pi - atan2(x[1], x[0]) for x in vectors]
    mags = [sqrt(x[0]**2 + x[1]**2) for x in vectors]

    angles[0] = angles[0] + 2*pi/12
    angles[1] = angles[1] - 4*pi/12

    comb_mags = sum(mags)
    if comb_mags == 0:
        return ((0, 0), (0, 0))

    comb_angle = sum([x * y for x, y in zip(angles, mags)]) / comb_mags
    return ((comb_angle, comb_mags), (angles, mags))

if __name__ == "__main__":
    cam = cv.VideoCapture(0)

    # read initial frames and set up locks for them to be pulled by the
    # networking thread
    for i in range(10):
        ret, initial_frame = cam.read()
    initial_frame = (np.sum(initial_frame, axis=2)/3.0).astype('uint8')
    # print initial_frame
    
    bblFrames = downsample([initial_frame, initial_frame, initial_frame])

    cv.imshow('frame', bblFrames[0])
    cv.waitKey(0)
    pos = [bblFrames[0][0].shape[0]/2, 0]
    print generate_direction(pos, bblFrames)
