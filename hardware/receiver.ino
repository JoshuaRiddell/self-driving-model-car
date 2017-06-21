#include "receiver.h"
#include "state_lights.h"

// define pwm data caches
volatile unsigned long prev_time[NUM_CHANNELS];
volatile uint16_t pwm_val[NUM_CHANNELS];

void handle_servo_intr();
void handle_throt_intr();
void handle_interrupt(uint8_t pin_id, bool change);

void setup_receiver() {
  // reciever pin modes
  pinMode(SERVO_RX, INPUT);
  pinMode(THROT_RX, INPUT);

  // attach unique pin interrupts for throttle and servo
  attachInterrupt(digitalPinToInterrupt(SERVO_RX), handle_servo_intr, CHANGE);
  attachInterrupt(digitalPinToInterrupt(THROT_RX), handle_throt_intr, CHANGE);
}

uint16_t get_pwm(int index) {
  return pwm_val[index];
}

void handle_servo_intr() {
  handle_interrupt(SERVO_ID, digitalRead(SERVO_RX));
}

void handle_throt_intr() {
  handle_interrupt(THROT_ID, digitalRead(THROT_RX));
}

void handle_interrupt(uint8_t pin_id, bool change) {
  // handle the pwm counters
  if (change) {
    prev_time[pin_id] = micros();
  } else {
    pwm_val[pin_id] = micros() - prev_time[pin_id];
  }
}
