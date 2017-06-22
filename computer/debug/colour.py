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
KEY_N = 1048686

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

samples = [[], [], []]

minimum = [0, 0, 0]
maximum = [255, 255, 255]
bounds = [[minimum, maximum]] * 3
bounds = [[np.array(x) for x in y] for y in bounds]
bounds_index = 0

while True:
    key = cv2.waitKey(0)

    print "frame: {0}".format(image_index)
    img = cv2.imread(images[image_index])
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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
        for sample in samples:
            fd.write(str(sample))
            fd.write("\n")
        fd.close()
    elif key == KEY_N:
        print "Resetting current sample..."
        samples[bounds_index] = []
        bounds[bounds_index] = [np.array(minimum[:]),
                np.array(maximum[:])]
        clicked = False

    inc = INCREMENTS.get(key)
    if inc == None:
        inc = 0

    image_index += inc
    image_index %= num_images

    # expand if left click
    if clicked == 1 or clicked == 2:
        if clicked == 1:
            filtered = apply_filters(img)
            new_coord = list(filtered[coordinate[1]][coordinate[0]])
            print new_coord

            samples[bounds_index].append(new_coord)
        elif clicked == 2:
            if len(samples) > 0:
                samples[bounds_index].pop()

        for i in range(len(bounds[bounds_index][0])):
            bounds[bounds_index][0][i] = min(x[i] for x in samples[bounds_index])
        for i in range(len(bounds[bounds_index][1])):
            bounds[bounds_index][1][i] = max(x[i] for x in samples[bounds_index])

        clicked = False

    thresh = get_binary(img, bounds_index, bounds=bounds)
    cv2.imshow("thresh", thresh)
    cv2.imshow('main', img)

cv2.destroyAllWindows()

