from unityCamera import UnityCamera
from imageRegistration import *

if __name__=="__main__":
	cam = UnityCamera()
	while(1):
		cam.receive()
		if cam.imageReceived:
			img, telem = cam.recv_image()
		else:
			img = None

		if img is None:
			continue
		find_path(img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
