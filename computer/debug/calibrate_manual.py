import numpy as np
import cv2
import glob

# sub pixel corner algorithm
STOP_CRIT = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# pixel box to search for corner in
SEARCH_BOX = (20, 20)

# camera resolution
RES = (1280, 720)
# warped output dimensions
OUT_RES = (720, 1280)
# warped output scale
SCALE = 1

# mapping from sqare test strip to output
VER_CENT = OUT_RES[0]*3/4
HOR_CENT = OUT_RES[0]/2
INC = OUT_RES[0]/4 * SCALE
MAP_TO = np.array((
    (HOR_CENT - INC, VER_CENT - INC),
    (HOR_CENT + INC, VER_CENT - INC),
    (HOR_CENT - INC, VER_CENT + INC),
    (HOR_CENT + INC, VER_CENT + INC)
), np.float32)

# mouse clicking globals
clicked = False
coordinate = (0, 0)

def setup_camera():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, RES[0]);
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, RES[1]);
    return cam

def get_image(cam):
    ret, img = cam.read()
    if not ret:
        return ret
    else:
        return img

def handle_mouse(event, x, y, flags, param):
    global clicked
    global coordinate

    if event == cv2.EVENT_LBUTTONDBLCLK:
        coordinate = np.array((x, y))
        clicked = 1
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        clicked = 2

def main():
    global coordinate
    global clicked

    cam = setup_camera()

    cv2.namedWindow('main')
    cv2.setMouseCallback('main', handle_mouse)

    coords = [];
    genMatrix = False
    M = None

    while True:
        img = get_image(cam)
        if not img.any():
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if clicked == 1:
            if len(coords) == 4:
                genMatrix = True
            else:
                coords.append(coordinate)
                print (len(coords))
            clicked = False
        elif clicked == 2:
            if len(coords) > 0:
                coords.pop()
            clicked = False

        # print clicked coords
        for coord in coords:
            cv2.circle(img, tuple(coord), 10, (255, 0, 0), -1)

        if genMatrix:
            M = cv2.getPerspectiveTransform(np.array(coords, np.float32), MAP_TO)

            print M

            coords = []
            genMatrix = False;

        cv2.imshow('main', img)
        if M is not None:
            warped = cv2.warpPerspective(img, M, OUT_RES)
            cv2.imshow('warped', warped)

        cv2.waitKey(10)

if __name__ == '__main__':
    main()
