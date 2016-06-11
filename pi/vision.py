import cv2 as cv
import numpy as np
# from threading import Thread, Lock

NUM_COLOURS = 2

BOUNDS = [
    [[19, 28, 117], [26, 255, 209]], # yellow
    [[0,0,0], [255,255,255]], # blue
]

CROP = [
    [[466, 135], [633, 377]],  # yellow crop
    [[0, 0], [100, 100]], # blue crop
]

for i in range(len(BOUNDS)):
    for j in range(len(BOUNDS[i])):
        BOUNDS[i][j] = np.array(BOUNDS[i][j])

KERNEL_SIZE = 5

class VisionInterface(object):
    def __init__(self, camera_id=0):
        # super(VisionInterface, self).__init__()

        # self.lock = Lock()
        self.cam = cv.VideoCapture(camera_id)

    def read_frame(self):
        # get the current frame
        ret, frame = self.cam.read()

        # do a blur and convert colour space
        frame = cv.boxFilter(frame, -1, (KERNEL_SIZE, KERNEL_SIZE))
        frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # threshold images
        thresh = []
        for i in range(NUM_COLOURS):
            thresh.append(cv.inRange(
                frame[CROP[i][0][1]:CROP[i][1][1], CROP[i][0][0]:CROP[i][1][0]],
                *BOUNDS[i]))
