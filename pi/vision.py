import cv2 as cv

class VisionInterface(object):
    def __init__(self, camera_id=0):
        self.cam = cv.VideoCapture(camera_id)

        self.capture()

    def capture(self):
        ret, self.current_frame = self.cam.read()

    def get_current_frame(self):
        return self.current_frame

    def save_current_frame(self, filename):
        cv.imwrite(filename, self.current_frame)