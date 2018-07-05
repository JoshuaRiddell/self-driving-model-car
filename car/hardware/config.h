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
#define ACTAUTOR_SERVO_OCR OCR1A
#define ACTUATOR_THROT_PIN PB2
#define ACTAUTOR_THROT_OCR OCR1B

// voltage sense pins
#define SENSE_DDR DDRC
#define SENSE_PIN PINC
#define SENSE_WALL_PIN PC5
#define SENSE_CPU_BATT_PIN PC4
#define SENSE_TRACT_BATT_PIN PC3

// power control pins
#define CTL_CPU_BATT_PIN PD4
#define CTL_CPU_BATT_PORT PORTD
#define CTL_CPU_BATT_DDR DDRD

#define CTL_WALL_PIN PD5
#define CTL_WALL_PORT PORTD
#define CTL_WALL_DDR DDRD

#define CTL_ESC_PIN PB5
#define CTL_ESC_PORT PORTB
#define CTL_ESC_DDR DDRB

// serial paramters
#define SERIAL_BAUD 9600
#define BUFFER_SIZE 2

// buzzer parameters
#define BUZZER_PIN PD6
#define BUZZER_PORT PORTD
#define BUZZER_DDR DDRD

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
#define LEDS_1_PIN PC2
#define LEDS_1_PORT PORTC
#define LEDS_1_DDR DDRC

#define LEDS_2_PIN PD7
#define LEDS_2_PORT PORTD
#define LEDS_2_DDR DDRD

#define LEDS_EXT_PIN PB3
#define LEDS_EXT_PORT PORTB
#define LEDS_EXT_DDR DDRB

#define SONAR_ECHO_PIN PB4
#define SONAR_ECHO_PORT PORTB
#define SONAR_ECHO_DDR DDRB

#define SONAR_TRIG_PIN PB0
#define SONAR_TRIG_PORT PORTB
#define SONAR_TRIG_DDR DDRB

#define ENCODER_PIN PINC
#define ENCODER_DDR DDRC

#define ENCODER_LEFT_PIN PC0
#define ENCODER_RIGHT_PIN PC1

#define ENCODER_INTERRUPT_ENABLE PCIE1
#define ENCODER_LEFT_INTERRUPT PCINT9
#define ENCODER_RIGHT_INTERRUPT PCINT8