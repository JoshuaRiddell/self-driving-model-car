import cv2
import Image
import threading
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time

vis = None

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path[-1].isdigit():
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					img = vis.get_frame(int(self.path[-1]))
                                        if img is None:
                                            continue

                                        try:
                                            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                                        except:
                                            pass

					jpg = Image.fromarray(img)
					tmpFile = StringIO.StringIO()
					jpg.save(tmpFile,'JPEG')
					self.wfile.write("--jpgboundary")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(tmpFile.len))
					self.end_headers()
					jpg.save(self.wfile,'JPEG')
					time.sleep(0.1)
				except KeyboardInterrupt:
					break
			return
		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="http://127.0.0.1:8080/cam.mjpg"/>')
			self.wfile.write('</body></html>')
			return


class WebServer(ThreadingMixIn, HTTPServer):
    pass

def register_vis_int(vis_int):
    global vis
    vis = vis_int
