# Connecting to the car

Options:
- Through ethernet on the router.
- Through the wifi network hot_snot_rod, password: 0904410178

# Router details

- IP: 10.1.0.138
- Username: admin
- Password: test1234

# Power

- The car has 2 power inputs. One for the ESC and one for the computers. They are isolated apart from tied grounds. When running the computers should run off the ~12V 3cells and the car should run off the 2cells (2cell to try and reduce the speed as much as possible).
- There is a power cable in the box with 2 XT60s on the end that can plug into the 2 XT60s on the car. There is a wall socket adapter but it's probably better to use a bench supply as it's a bit underpowered and has started to make a crackling sound.
- DO NOT TURN THE ESC ON WHEN USING THE UMBILICAL CORD - it'll make power surges that just make the Jetson shut down. Using the servo is fine.
- The RC receiver is powered by the ESC. There is a small red cable coming from the radio receiver (labelled "AUX") that can be used to power the receiver from the arduino when the esc is turned off. The car is currently in AUX power mode for the receiver. There is a lone pin which is not connected that can be use the hold the wire when not using aux power. When using aux power the ESC cable should be unplugged (labelled "ESC").

# Jetson Details

- Static IP of 10.1.0.1 (set by router)
- Username: ubuntu
- Password: ubuntu
- i.e. ssh ubuntu@10.1.0.1
- Repo is cloned in the symlink ~/car
- Is connected to router via ethernet and has a wifi card. If you need internet on it you'll need to connect to eduroam via wifi card. nm-connection-editor starts network manager gui - that's how I did it.

# Code

## Arduino
- Arduino code located in hardware/
- Use arduino_upload.sh to upload it to the arduino using the jetson.
- arduino_serial.sh is screen command for arduino serial.

## Computer
- Computer code runs on the jetson
- It's currently all in python. I was originally planning to use tensorflow but I didn't - now because I'm using python, opencv is only running on a single thread of the CPU which is pretty crappy. I am regretting python.
- 3 main components - hardware.py interfaces with the arduino, server.py runs a server to stream frames over 10.1.0.1:5000/[frame_id] where frame_id is just a number, and vision.py which does cv.
