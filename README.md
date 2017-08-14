# UQ Robotics - QUT Droid Racing Challenge Entry

Here lies the main repository for resources concerning our entry to the QUT DRC.

# Features

- [ ] Hot-swappable battery and wall charging
- [ ] Single board power management and control PCB
- [ ] Internet connection passthrough/github commit passthrough
- [ ] Quicken arm/disarm process for better switching between manual and automatic control
- [ ] Clear indicator of automatic/manual control
- [ ] Option for automatic steering but manual throttle (for extra debugging)
- [ ] Shell/Case for all electronics
- [ ] Better mount of Jetson and Router
- [ ] Remove suspension lockers/thicker oil/test robustness of camera angle to hard braking/acceleration
  - [ ] Add accelerometer for compensation of camera angle changes if needed
- [ ] Make storage and transport box
- [ ] Make backpack attachment for mounting car
- [ ] Make code execution more streamline
  - [ ] Always running background process
  - [ ] General command line interface
  - [ ] Dynamic code loading / easy restart script / easy restart button
  - [ ] Web GUI with mobile compatitbility
  - [ ] Bluetooth remote control (LoRa maybe)
  - [ ] Nice interface for recording and sorting through data
- [ ] Make setup documentation
- [ ] Add setup script to install OpenCV from clean
- [ ] Pole/switch/sensor for detecting finish line
- [ ] Recording of data while car is in operation for insight into what went wrong
- [x] Get better 12V power supply

# Algorithm Ideas

- [ ] Port current code to cpp
- [ ] Add CUDA support for quicker execution times
- [ ] Optimise perspective transformation to reduce execution time (only transform pixels we need)
- [ ] Adaptive thresholding for sides of track
- [ ] Weighted and time variant filtering of track output
- [ ] Add support for obstacle avoidance

# PCBs
## Low Level Electronics PCB

- [ ] 32-bit microcontroller
- [ ] FTDI chip
- [ ] ISP header
- [ ] 2x PWM output
- [ ] 2x PWM input
- [ ] 4x LED array output
- [ ] 1x piezo buzzer output
- [ ] Power switching from battery to wall power (allows servo to work off wall power)
- [ ] 1x ultrasonic sensor input

## Power Distribution PCB

- [ ] Relays for switching between battery and wall power
- [ ] Smoothing capacitors for switching noise
- [ ] 2x battery charger
- [ ] 2x battery balancer
- [ ] 2x battery voltage/current indicators
- [ ] 2x XT60 sensetive electronics output (~4A) + alternative connectors
- [ ] 1x XT60 high power electronics output (~30A) + alternative connectors

## Pogo Pin PCB

- [ ] Stepped pogo pin array
- [ ] High current output ~10A
- [ ] 3 wire interface to power distribution board
- [ ] Holes to mount magnets
