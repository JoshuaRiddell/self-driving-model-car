// pwm values
//          min   mid   max
// servo:   1032  1364  1700
// throt:   1020  1556  2056

// serial paramters
#define SERIAL_BAUD 115200
#define BUFFER_SIZE 2

// buzzer parameters
#define BUZZER_PIN 8
#define BUZZ_DURATION 40000
#define SOUND_HIGH 100
#define SOUND_MIDDLE 110
#define SOUND_LOW 115

// sonar pins
#define SONAR_ECHO 6
#define SONAR_TRIG 7
#define SONAR_DELAY 60
#define SONAR_TRIGGER 70

// reciever pins
#define SERVO_RX 2
#define THROT_RX 3

// output pins
#define SERVO_TX 10
#define THROT_TX 11

// idle values for outputs
#define SERVO_IDLE 1364
#define THROT_IDLE 1546

// specific thresholds
#define SHUTDOWN_THRESH 1100  // less than this for shutdown
#define STARTUP_THRESH 1930  // larger than this for startup
#define ARM_CUTOFF 3000 // ms to wait until ar
#define STEERING_THRESH 1650 // larger than this to go into manual control mode
#define MANUAL_DELAY 20
#define MANUAL_CUTOFF 2000

// array values for servo and throttle
#define SERVO_ID 0
#define THROT_ID 1
#define NUM_CHANNELS 2
