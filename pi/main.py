import vision as vi

class MainApp(object):
    def __init__(self):
        self.vis_int = vi.VisionInterface(camera_id=1)

    def run(self):
        self.vis_int.start()
        while True:
            pass

def main():
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()
