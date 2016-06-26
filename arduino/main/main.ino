#include <Servo.h>

// sonar pins
#define SONAR_ECHO 0
#define SONAR_TRIG 7

// reciever pins
#define SERVO_RX 2
#define THROT_RX 3

// output pins
#define SERVO_TX 10
#define THROT_TX 11

// idle values for outputs
#define SERVO_IDLE 0
#define THROT_IDLE 0

// array values for servo and throttle
#define SERVO_ID 0
#define THROT_ID 1
#define NUM_CHANNELS 2

// define pin arrays
static const uint8_t input_pins[] = { SERVO_RX, THROT_RX };
Servo output_pins[NUM_CHANNELS];

// define pwm data caches
volatile unsigned long prev_time[NUM_CHANNELS];
volatile uint16_t pwm_val[NUM_CHANNELS];

void setup() {
  // sonar pin modes
  pinMode(SONAR_TRIG, OUTPUT);

  // reciever pin modes
  pinMode(SERVO_RX, INPUT);
  pinMode(THROT_RX, INPUT);

  // output pin modes
  output_pins[SERVO_ID].attach(SERVO_TX);
  output_pins[THROT_ID].attach(THROT_TX);
  
  output_pins[SERVO_ID].write(SERVO_IDLE);
  output_pins[THROT_ID].write(THROT_IDLE);

  Serial.begin(19200);

  attachInterrupt(digitalPinToInterrupt(SERVO_RX), handle_servo_intr, CHANGE);
  attachInterrupt(digitalPinToInterrupt(THROT_RX), handle_throt_intr, CHANGE);
}

void loop() {
  while (1) {
    // Serial.println(pwm_val[0]);
  }
}

void handle_servo_intr() {
  // pass through current pin value
  Serial.println(digitalRead(SERVO_RX));
  handle_interrupt(SERVO_ID, digitalRead(SERVO_RX));
}

void handle_throt_intr() {
  // pass through current pin value
  handle_interrupt(THROT_ID, digitalRead(THROT_RX));
}

void handle_interrupt(uint8_t pin_id, bool change) {
  if (change) {
    prev_time[pin_id] = millis();
  } else {
    pwm_val[pin_id] = millis() - prev_time[pin_id];
  }
}





























