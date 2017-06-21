# left click to place a point on a rectangular reference
# right click to cancel point placement
# order should be:
# 1-----2
# |     |
# |     |
# 3-----4

import numpy as np
import cv2

# file to store the finished matrix in
MATRIX_FILENAME = '../perspective_matrix.txt'

# sub pixel corner algorithm
STOP_CRIT = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# pixel box to search for corner in
SEARCH_BOX = (20, 20)

# camera resolution
RES = (1280, 720)
# warped output dimensions
OUT_RES = (1800, 1280)
# warped output scale
SCALE = 0.1

# mapping from sqare test strip to output
HOR_CENT = OUT_RES[0]/2  # horizontal centreline
INC = OUT_RES[0]/4 * SCALE  # increment (how big the square will be)
VER_CENT = OUT_RES[1] - INC*2  # vertical centreline
MAP_TO = np.array((
    (HOR_CENT - INC, VER_CENT - INC),
    (HOR_CENT + INC, VER_CENT - INC),
    (HOR_CENT - INC, VER_CENT + INC),
    (HOR_CENT + INC, VER_CENT + INC)
), np.float32)

# mouse clicking globals
clicked = False  # mouse button was clicked
coordinate = (0, 0)  # coordinate of mouse click

def setup_camera():
    "Setup the camera with chosen resolution"
    cam = cv2.VideoCapture(0)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, RES[0]);
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, RES[1]);
    return cam

def get_image(cam):
    "Get an image from the camera"
    ret, img = cam.read()
    if not ret:
        return None
    else:
        return img

def handle_mouse(event, x, y, flags, param):
    "Handle mouse event, set a flag for button pressed and coordinate."
    global clicked
    global coordinate

    if event == cv2.EVENT_LBUTTONDBLCLK:
        coordinate = np.array((x, y))
        clicked = 1
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        clicked = 2

def main():
    global clicked
    global coordinate

    cam = setup_camera()

    # make window and attach callback
    cv2.namedWindow('main')
    cv2.setMouseCallback('main', handle_mouse)

    coords = [];  # array of coordiantes for rectangle
    genMatrix = False  # flag to generate matrix on next loop
    M = None  # perspecitve matrix

    # try and load a previously made coordinate array
    try:
        fd = open(MATRIX_FILENAME, 'r')

        coords = eval(fd.readline())

        # build the perspecitve matrix based on coordinates
        M = cv2.getPerspectiveTransform(
                np.array(coords, np.float32),
                MAP_TO);

        fd.close()

        print "Loaded stored perspective"
    except:
        M = None
        pass

    # frame loop for user interface
    while True:
        # get image from camera
        img = get_image(cam)
        if img is None:
            continue

        # if left mouse was clicked then add coordinate to coordinates array
        if clicked == 1:
            if len(coords) == 4:
                # if we have enough coordinates then make a new matrix
                genMatrix = True
            else:
                # add coordinates to array
                coords.append(coordinate)
                print (len(coords))

            # reset clicked flag
            clicked = False
        # if right mouse was clicked
        elif clicked == 2:
            if len(coords) > 0:
                # cancel last coordinate
                coords.pop()
                print (len(coords))

            # reset clicked flag
            clicked = False

        # display clicked coords on frame
        for coord in coords:
            cv2.circle(img, tuple(coord), 10, (255, 0, 0), -1)

        # generate new matrix if flag was set
        if genMatrix:
            # gen matrix
            M = cv2.getPerspectiveTransform(np.array(coords, np.float32), MAP_TO)

            # print it and save it to a file of format
            # (coordinates,mapping_coords,input_resolution,output_resolution)
            print M
            fd = open(MATRIX_FILENAME, 'w')
            fd.write(str(list([list(x) for x in coords])))
            fd.write("\n")
            fd.write(str(list([list(x) for x in MAP_TO])))
            fd.write("\n")
            fd.write(str(list(RES)))
            fd.write("\n")
            fd.write(str(list(OUT_RES)))
            fd.close()

            # reset coordinates array and flags
            coords = []
            genMatrix = False;

        # show undistorted image
        cv2.imshow('main', img)

        # if we have a matrix then show distorted image
        if M is not None:
            warped = cv2.warpPerspective(img, M, OUT_RES)
            cv2.imshow('warped', warped)

        # wait for a key or 10ms to pass
        cv2.waitKey(10)

if __name__ == '__main__':
    main()
