import cv2 as cv
import numpy as np
from threading import Lock

# turn
# right, straight, left
# 120,   200,      230

# get perspective matrix
MATRIX_FILENAME = "perspective_matrix.txt"

# number of colours to store
NUM_COLOURS = 2
# number of frames to store for streaming
NUM_FRAMES = 3
# kernel size for blur filter
KERNEL_SIZE = 5

# use a projection for topdown perspective
USE_PERSPECTIVE = True

# will be overriden by projection matrix information if it's activated
DEFAULT_RESOLUTION = (1920, 1080)

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

# transform bounds into easy to use format
for i in range(len(BOUNDS)):
    for j in range(len(BOUNDS[i])):
        BOUNDS[i][j] = np.array(BOUNDS[i][j])

class VisionInterface(object):
    """Contains all interfaces with the webcam.
    """

    def __init__(self, camera_id=0):
        """Import perspective matrix or set resolutions. Set up the camera.
        Setup some default initial frames.
        """
        self.get_perspective_matrix()

        # set up camera
        self.cam = cv.VideoCapture(camera_id)
        self.cam.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, self.cam_res[0]);
        self.cam.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, self.cam_res[1]);

        # read initial frames and set up locks for them to be pulled by the
        # networking thread
        ret, initial_frame = self.cam.read()
        self.frames = [initial_frame.copy()] * NUM_FRAMES
        self.flags = [False] * NUM_FRAMES
        self.locks = [Lock()] * NUM_FRAMES

    def get_perspective_matrix(self):
        """Loads a perspective matrix from file to transform perspective to
        overhead view. If not available will just set the resolution.
        """
        try:
            if USE_PERSPECTIVE:
                # load perspective file
                fd = open(MATRIX_FILENAME, 'r')

                coords = eval(fd.readline())
                map_to = eval(fd.readline())
                self.cam_res = tuple(eval(fd.readline()))
                self.res = tuple(eval(fd.readline()))

                self.M = cv.getPerspectiveTransform(
                        np.array(coords, np.float32),
                        np.array(map_to, np.float32))

                fd.close()

                print "Perspective loaded"
            else:
                raise Exception("NULL")

        except:
            # set regular resolution
            self.cam_res = DEFAULT_RESOLUTION
            self.res = DEFAULT_RESOLUTION

            print "Perspective failed to load"

    def get_frame(self, frame_id):
        """Threadsafe function to get a frame from a given frame stream.
        """
        if frame_id < 0 or frame_id > NUM_FRAMES - 1:
            return None
        self.locks[frame_id].acquire()
        if self.flags[frame_id]:
            frame = self.frames[frame_id]
            self.flags[frame_id] = False
        else:
            frame = None
        self.locks[frame_id].release()
        return frame

    def update_frame(self, frame_id, frame):
        """Threadsafe function to update a frame in the frame stream.
        """
        self.locks[frame_id].acquire()
        self.frames[frame_id] = frame.copy()
        self.flags[frame_id] = True
        self.locks[frame_id].release()

    def read_frame(self):
        """Reads a frame and performs most of the cv logic. Updates the
        relevant frame buffers.
        """
        # get the current frame
        ret, frame = self.cam.read()
        self.update_frame(0, frame)

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        self.update_frame(1, gray)

        # warped = cv.warpPerspective(frame, self.M, self.res)
        warped = img
        self.update_frame(2, warped)


#        # do a blur and convert colour space
#        frame = cv.boxFilter(frame, -1, (KERNEL_SIZE, KERNEL_SIZE))
#        frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
#
#        # threshold images
#        thresh = cv.inRange(
#            frame[CROP[0][0][1]:CROP[0][1][1], CROP[0][0][0]:CROP[0][1][0]],
#            *BOUNDS[0])
#
#        contours, heirarchy = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#
#        rows, cols = thresh.shape[:2]
#
#        if len(contours) == 0:
#            return None
#
#        line_params = cv.fitLine(contours[0], cv.cv.CV_DIST_L2, 0, 0.01, 0.01)
#        vx, vy, x, y = [x[0] for x in line_params]
#
#        righty = int(((cols-x)*vy/vx)+y)
#        angle = int(round((rightY-202)/35*100))
#        print angle
#        return angle
#
#        # line_frame = cv.line(thresh,(cols-1,righty),(0,lefty),(0,255,0),2)
#
#
#        # cv.imshow('frame', frame)
#        # cv.imshow('thresh', thresh)
#        # # cv.imshow('line', line_frame[0])
#        # cv.waitKey(0)
