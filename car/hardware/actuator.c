#include <avr/io.h>

#include <stdio.h>

#include "actuator.h"

#include "config.h"

void actuator_init(void) {
  ACTUATOR_DDR |= _BV(ACTUATOR_SERVO_PIN)|_BV(ACTUATOR_THROT_PIN);

  TCCR1A = _BV(WGM11)|_BV(COM1A1)|_BV(COM1B1);
  TCCR1B = _BV(WGM13)|_BV(WGM12)|_BV(CS11);

  ICR1 = 39999;  // 50Hz frequency
  ACTAUTOR_SERVO_OCR = 0;
  ACTAUTOR_THROT_OCR = 0;

  actuator_idle();
}

void actuator_write_servo(uint16_t width) {
  ACTAUTOR_SERVO_OCR = width * 2;
  // printf("ACTUATOR: servo: %u\n", width);
}

void actuator_write_throt(uint16_t width) {
  ACTAUTOR_THROT_OCR = width * 2;
  // printf("ACTUATOR: throt: %u\n", width);
}

uint16_t actuator_read_servo(void) {
  return (ACTAUTOR_SERVO_OCR + 1)/2;
}

uint16_t actuator_read_throt(void) {
  return (ACTAUTOR_THROT_OCR + 1)/2;
}

// idle throttle and centre steering
void actuator_idle(void) {
  actuator_write_servo(SERVO_IDLE);
  actuator_write_throt(THROT_IDLE);
}