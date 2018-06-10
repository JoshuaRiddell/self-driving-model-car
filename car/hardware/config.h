// pwm values
//          min   mid   max
// servo:   1032  1364  1700
// throt:   1020  1556  2056

// debug message switches
#define POWER_DEBUG_MSG

// feature switches
// #define DISABLE_BUZZER

// input pin numbers
#define RECEIVER_DDR DDRD
#define RECEIVER_PORT PORTD
#define RECEIVER_SERVO_PIN PD2
#define RECEIVER_THROT_PIN PD3

// output pins
#define ACTUATOR_DDR DDRB
#define ACTUATOR_SERVO_PIN PB1
#define ACTAUTOR_SERVO_OCR OCR1B
#define ACTUATOR_THROT_PIN PB2
#define ACTAUTOR_THROT_OCR OCR1A






// voltage sense pins
#define SENSE_DDR DDRC
#define SENSE_PIN PINC
#define SENSE_WALL_PIN PC1
#define SENSE_CPU_BATT_PIN PC2
#define SENSE_TRACT_BATT_PIN PC3

// power control pins
#define CTL_CPU_DDR DDRC
#define CTL_CPU_PORT PORTC

#define CTL_ESC_DDR DDRB
#define CTL_ESC_PORT PORTB

#define CTL_ESC_PIN PB5
#define CTL_WALL_PIN PC4
#define CTL_CPU_BATT_PIN PC5

#define CTL_WALL_INTERRUPT PCINT9
#define CTL_WALL_INTERRUPT_ENABLE PCIE1

// serial paramters
#define SERIAL_BAUD 115200
#define BUFFER_SIZE 2

// buzzer parameters
#define BUZZER_DDR DDRC
#define BUZZER_PORT PORTC
#define BUZZER_PIN PC0

#define BUZZ_DURATION 10000
#define SOUND_HIGH 100
#define SOUND_MIDDLE 110
#define SOUND_LOW 115

// array values for accessing values
#define SERVO_ID 0
#define THROT_ID 1
#define NUM_CHANNELS 2


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

#define WHITE_PIN PD4  // on when car is in blocked flow waiting for user input
#define BLUE_PIN PD5
#define GREEN_PIN PD6  // car is currently armed and can move at any time
#define RED_PIN PD7

#define LEDS_WHITE 1
#define LEDS_BLUE 2
#define LEDS_GREEN 3
#define LEDS_RED 4