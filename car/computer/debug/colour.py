#!/usr/bin/python2

import numpy as np
import cv2
import glob
from thresholding import load_bounds, apply_filters, get_binary, THRESH_FILENAME, apply_morph, downsample, generate_direction
import getpass
from math import cos, sin

user = getpass.getuser()

if user == "ubuntu":
    RIGHT_ARROW = 1113939
    LEFT_ARROW = 1113937
    RIGHT_BRACKET = 1048669
    LEFT_BRACKET = 1048667

    KEY_Q = 1048689
    KEY_S = 1048691
    KEY_N = 1048686
    KEY_M = 0

    KEY_1 = 1048625
    KEY_2 = 1048626
    KEY_3 = 1048627
elif user == "josh":
    RIGHT_ARROW = 65363
    LEFT_ARROW = 65361
    RIGHT_BRACKET = 93
    LEFT_BRACKET = 91

    KEY_Q = 113
    KEY_S = 115
    KEY_N = 110
    KEY_M = 109

    KEY_1 = 49
    KEY_2 = 50
    KEY_3 = 51
else:
    raise Exception("No user registered")

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

path = "/home/" + user + "/car/computer/images/" + folder_name
# termination criteria
images = sorted(glob.glob(path + '/*.jpg'))
num_images = len(images)
image_index = 0

# make window and attach callback
cv2.namedWindow('main')
cv2.namedWindow('thresh')
cv2.setMouseCallback('main', handle_mouse)
cv2.setMouseCallback('thresh', handle_mouse)

bounds, samples = load_bounds()
bounds_index = 0

minimum = [0, 0, 0]
maximum = [255, 255, 255]

do_morph = True

while True:
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
    elif key == KEY_M:
        print "Toggling morph..."
        do_morph = not do_morph

    inc = INCREMENTS.get(key)
    if inc == None:
        inc = 0

    # expand if left click
    if clicked == 1 or clicked == 2:
        if clicked == 1:
            filtered = apply_filters(img)
            new_coord = list(filtered[coordinate[1]][coordinate[0]])
            print new_coord

            samples[bounds_index].append(new_coord)
        elif clicked == 2:
            print "Sample popped, using {0} samples".format(len(samples[bounds_index]))
            if len(samples[bounds_index]) > 0:
                samples[bounds_index].pop()

        if len(samples[bounds_index]) == 0:
            continue

        for i in range(len(bounds[bounds_index][0])):
            bounds[bounds_index][0][i] = min(x[i] for x in samples[bounds_index])
        for i in range(len(bounds[bounds_index][1])):
            bounds[bounds_index][1][i] = max(x[i] for x in samples[bounds_index])

        clicked = False

    image_index += inc
    image_index %= num_images

    img = cv2.imread(images[image_index])

    print "frame: {0}".format(image_index)

    threshs = get_binary(img, bounds=bounds)
    if do_morph:
        threshs = apply_morph(threshs)

    matrices = downsample(threshs)

    position = (threshs[0].shape[1]/2, threshs[0].shape[0])
    vect = [0, 0]

    (comb, debug) = generate_direction([matrices[0].shape[0]/2, 0], matrices)

    angle = comb[0]
    mag = comb[1]

    print ">> {0} {1}".format(angle, mag)

    start_point = tuple([int(x) for x in position])
    end_point = (start_point[0] - int(100 * cos(angle)), start_point[1] - int(100 * sin(angle)))

    cv2.line(img, start_point, end_point, (0, 255, 0), 2)

    cv2.imshow("thresh", threshs[bounds_index])
    cv2.imshow('main', img)
    cv2.imshow('mat', matrices[bounds_index])

cv2.destroyAllWindows()

