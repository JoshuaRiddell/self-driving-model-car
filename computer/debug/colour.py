#!/usr/bin/python2

import numpy as np
import cv2
import glob
from thresholding import get_binary

RIGHT_ARROW = 1113939
LEFT_ARROW = 1113937
RIGHT_BRACKET = 1048669
LEFT_BRACKET = 1048667

KEY_Q = 1048689

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
cv2.setMouseCallback('main', handle_mouse)

samples = []
bounds = [[0, 0, 0], [0, 0, 0]]

while True:
    print "frame: {0}".format(image_index)
    img = cv2.imread(images[image_index])
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cv2.imshow('main', img)
    key = cv2.waitKey(0)

    if key == KEY_Q:
        break

    inc = INCREMENTS.get(key)
    if inc == None:
        inc = 0

    image_index += inc
    image_index %= num_images

    if clicked == 1:
        new_coord = list(img[coordinate[1]][coordinate[0]])
        samples.append(new_coord)

        clicked = 0
    elif clicked == 2:
        if len(samples) > 1:
            samples.pop()

        clicked = 0


    thresh = get_binary(img, 0, 0)
    cv2.imshow("thresh", thresh)

cv2.destroyAllWindows()








