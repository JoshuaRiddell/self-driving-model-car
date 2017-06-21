#!/usr/bin/python2

import numpy as np
import cv2
import glob

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

folder_name = raw_input("Image folder name: ")
if len(folder_name) == 0:
    folder_name = "test0"

path = "../images/" + folder_name
# termination criteria
images = glob.glob(path + '/*.jpg')
num_images = len(images)
image_index = 0

while True:
    print "frame: {0}".format(image_index)
    img = cv2.imread(images[image_index])

    cv2.imshow('main', img)
    key = cv2.waitKey(0)

    if key == KEY_Q:
        break

    inc = INCREMENTS.get(key)
    if inc == None:
        inc = 0

    image_index += inc
    image_index %= num_images

cv2.destroyAllWindows()

