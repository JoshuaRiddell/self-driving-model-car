import cv2 as cv
import numpy as np
# from threading import Thread, Lock

# turn
# right, straight, left
# 120,   200,      230

NUM_COLOURS = 2

BOUNDS = [
    [[ 26,  28, 178], [ 30, 238, 230]], # yellow
    [[0,0,0], [255,255,255]], # blue
]

CROP = [
    [[466, 150], [633, 377]],  # yellow crop
    [[0, 0], [100, 100]], # blue crop
]

for i in range(len(BOUNDS)):
    for j in range(len(BOUNDS[i])):
        BOUNDS[i][j] = np.array(BOUNDS[i][j])

KERNEL_SIZE = 5

class VisionInterface(object):
    def __init__(self, camera_id=0):
        self.cam = cv.VideoCapture(camera_id)

    def read_frame(self):
        # get the current frame
        ret, frame = self.cam.read()

        # do a blur and convert colour space
        frame = cv.boxFilter(frame, -1, (KERNEL_SIZE, KERNEL_SIZE))
        frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # threshold images
        thresh = cv.inRange(
            frame[CROP[0][0][1]:CROP[0][1][1], CROP[0][0][0]:CROP[0][1][0]],
            *BOUNDS[0])

        contours, heirarchy = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        rows, cols = thresh.shape[:2]

        if len(contours) == 0:
            return None

        line_params = cv.fitLine(contours[0], cv.cv.CV_DIST_L2, 0, 0.01, 0.01)
        vx, vy, x, y = [x[0] for x in line_params]

        righty = int(((cols-x)*vy/vx)+y)
        angle = int(round((rightY-202)/35*100))
        print angle
        return angle

        # line_frame = cv.line(thresh,(cols-1,righty),(0,lefty),(0,255,0),2)


        # cv.imshow('frame', frame)
        # cv.imshow('thresh', thresh)
        # # cv.imshow('line', line_frame[0])
        # cv.waitKey(0)
