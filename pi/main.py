import hardware_interface as hi
import vision

class MainApp(object):
	def __init__(self):
		self.vision_interface = vision.VisionInterface()

	def run(self):
		self.vision_interface.save_current_frame("hello world.png")

def main():
	app = MainApp()
	app.run()

if __name__ == "__main__":
	main()
