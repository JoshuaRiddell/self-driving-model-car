#!/usr/bin/python2

import numpy as np
import cv2
import glob
from thresholding import load_bounds, apply_filters, get_binary, THRESH_FILENAME

RIGHT_ARROW = 1113939
LEFT_ARROW = 1113937
RIGHT_BRACKET = 1048669
LEFT_BRACKET = 1048667

KEY_Q = 1048689
KEY_S = 1048691

KEY_1 = 1048625
KEY_2 = 1048626
KEY_3 = 1048627

INCREMENTS = {
    RIGHT_ARROW: 10,
    LEFT_ARROW: -10,
    RIGHT_BRACKET: 1,
    LEFT_BRACKET: -1
}

clicked = False
coordinate = (0, 0)

def handle_mouse(event, x, y, flags, param):
    "Handle mouse event, set a flag for button pressed and coordinate."
    global clicked
    global coordinate

    if event == cv2.EVENT_LBUTTONDBLCLK:
        coordinate = np.array((x, y))
        clicked = 1
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        clicked = 2

folder_name = raw_input("Image folder name: ")
if len(folder_name) == 0:
    folder_name = "test0"

path = "../images/" + folder_name
# termination criteria
images = glob.glob(path + '/*.jpg')
num_images = len(images)
image_index = 0

# make window and attach callback
cv2.namedWindow('main')
cv2.namedWindow('thresh')
cv2.setMouseCallback('main', handle_mouse)
cv2.setMouseCallback('thresh', handle_mouse)

bounds = load_bounds()
bounds_index = 0

while True:
    print "frame: {0}".format(image_index)
    img = cv2.imread(images[image_index])
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cv2.imshow('main', img)
    key = cv2.waitKey(0)

    if key == KEY_Q:
        break
    elif key == KEY_1:
        print "Editing left track"
        bounds_index = 0
    elif key == KEY_2:
        print "Editing right track"
        bounds_index = 1
    elif key == KEY_3:
        print "Editing obstacle track"
        bounds_index = 2
    elif key == KEY_S:
        print "Saving..."

        fd = open(THRESH_FILENAME, 'w')
        for bound in bounds:
            fd.write(str([list(x) for x in bound]))
            fd.write("\n")
        fd.close()

    inc = INCREMENTS.get(key)
    if inc == None:
        inc = 0

    image_index += inc
    image_index %= num_images

    # expand if left click
    if clicked == 1 or clicked == 2:
        img = apply_filters(img)
        new_coord = list(img[coordinate[1]][coordinate[0]])
        print new_coord

        if clicked == 1:
            for i in range(len(bounds[bounds_index][0])):
                if bounds[bounds_index][0][i] > new_coord[i]:
                    bounds[bounds_index][0][i] = new_coord[i]
            for i in range(len(bounds[bounds_index][1])):
                if bounds[bounds_index][1][i] < new_coord[i]:
                    bounds[bounds_index][1][i] = new_coord[i]
        if clicked == 2:
            for i in range(len(bounds[bounds_index][0])):
                if bounds[bounds_index][0][i] < new_coord[i]:
                    bounds[bounds_index][0][i] = new_coord[i]
            for i in range(len(bounds[bounds_index][1])):
                if bounds[bounds_index][1][i] > new_coord[i]:
                    bounds[bounds_index][1][i] = new_coord[i]

        clicked = False

    thresh = get_binary(img, bounds_index, bounds=bounds)
    cv2.imshow("thresh", thresh)

cv2.destroyAllWindows()








