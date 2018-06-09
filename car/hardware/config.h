// pwm values
//          min   mid   max
// servo:   1032  1364  1700
// throt:   1020  1556  2056

// debug message switches
#define POWER_DEBUG_MSG



// input pin numbers
#define SERVO_RX 2
#define THROT_RX 3



// voltage sense pins
#define SENSE_WALL 15
#define SENSE_CPU_BATT 16
#define SENSE_TRACT_BATT 17

// power control pins
#define CTL_ESC 13
#define CTL_WALL 18
#define CTL_CPU_BATT 19

#define CTL_WALL_INTERRUPT PCINT9
#define CTL_WALL_INTERRUPT_ENABLE PCIE1

// serial paramters
#define SERIAL_BAUD 115200
#define BUFFER_SIZE 2

// buzzer parameters
#define BUZZER_PIN 14
#define BUZZ_DURATION 10000
#define SOUND_HIGH 100
#define SOUND_MIDDLE 110
#define SOUND_LOW 115

// array values for accessing values
#define SERVO_ID 0
#define THROT_ID 1
#define NUM_CHANNELS 2

// output pins
#define SERVO_TX 10
#define THROT_TX 11

// idle values for outputs
#define SERVO_IDLE 1364
#define THROT_IDLE 1546
#define IDLE_ERROR 10

// specific thresholds
#define SHUTDOWN_THRESH 1100  // less than this for shutdown
#define STARTUP_THRESH 1930  // larger than this for startup
#define ARM_CUTOFF 700 // ms to wait until arm
#define STEERING_THRESH 1650 // larger than this to go into manual control mode
#define THROTTLE_IDLE 1570
#define MANUAL_DELAY 20
#define MANUAL_CUTOFF 2000

// serial signals (bytes)
#define SERIAL_DISARMED '0'
#define SERIAL_ARMED '1'
#define SERIAL_AUTO '2'
#define SERIAL_MANUAL '3'

// define pins
#define LEDS_PORT PORTD
#define LEDS_DDR DDRD

#define WHITE_PIN PIND4  // on when car is in blocked flow waiting for user input
#define BLUE_PIN PIND5
#define GREEN_PIN PIND6  // car is currently armed and can move at any time
#define RED_PIN PIND7

#define LEDS_WHITE 1
#define LEDS_BLUE 2
#define LEDS_GREEN 3
#define LEDS_RED 4