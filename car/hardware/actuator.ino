#include <Servo.h>

#include "actuator.h"

// define pin arrays
Servo output_pins[NUM_CHANNELS];

void actuator_init(void) {
  output_pins[SERVO_ID].attach(SERVO_TX);
  output_pins[THROT_ID].attach(THROT_TX);

  output_pins[SERVO_ID].writeMicroseconds(SERVO_IDLE);
  output_pins[THROT_ID].writeMicroseconds(THROT_IDLE);
}

void actuator_write_index(uint8_t index, uint16_t val) {
    output_pins[index].writeMicroseconds(val);
}

// idle throttle and centre steering
void actuator_idle(void) {
  output_pins[SERVO_ID].writeMicroseconds(SERVO_IDLE);
  output_pins[THROT_ID].writeMicroseconds(THROT_IDLE);
}