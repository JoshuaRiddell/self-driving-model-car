import cv2
import Image
import threading
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time

# vision interface obeject
# TODO get rid of this dirty global
vision = None

# maximum dimension of sent frame (smaller is faster)
MAX_DIM = 700

class CamHandler(BaseHTTPRequestHandler):
    """Handles http request for camera frames.
    """

    def do_GET(self):
        """Http get request callback. Replies with the relevant frame if a
        frame was requested.
        """
        # if it ends in a digit then we'll reply with a frame
        if self.path[-1].isdigit():
            # send a header
            self.send_response(200)
            self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()

            # video loop
            while True:
                try:
                    # get a frame from the vision stream
                    img = vision.get_frame(int(self.path[-1]))
                    if img is None:
                        continue

                    try:
                        # scale the frame to save memory
                        scale = MAX_DIM / float(max([img.shape[0], img.shape[1]]))
                        img = cv2.resize(img,
                                (int(img.shape[1]*scale), int(img.shape[0]*scale)),
                                interpolation=cv2.cv.CV_INTER_AREA)

                        if (img[0][0][0] != img[0][0][1] != img[0][0][2]):
                            # try converting to rgb, won't work for grayscale images
                            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                    except:
                        img = None
                        pass

                    if img is None:
                        continue

                    # make a jpeg and send it
                    jpg = Image.fromarray(img)
                    tmpFile = StringIO.StringIO()
                    jpg.save(tmpFile,'JPEG')
                    self.wfile.write("--jpgboundary")
                    self.send_header('Content-type','image/jpeg')
                    self.send_header('Content-length',str(tmpFile.len))
                    self.end_headers()
                    jpg.save(self.wfile,'JPEG')

                    # small delay so we have reasonable frame rate
                    time.sleep(0.1)

                except KeyboardInterrupt:
                    # I think this is suppose to let me keyboard interrupt
                    # from terminal - doesn't seem to work.
                    break
            return

class WebServer(ThreadingMixIn, HTTPServer):
    """Make a threaded http server.
    """
    pass

def register_vision(vision_interface):
    """Register a the vision interface object in the library.
    """
    global vision
    vision = vision_interface
