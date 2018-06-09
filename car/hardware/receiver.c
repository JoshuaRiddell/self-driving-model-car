#include <avr/io.h>
#include <avr/interrupt.h>

#include <stdbool.h>

#include "config.h"
#include "receiver.h"

#include "time.h"

#include "leds.h"


volatile uint32_t prev_time[NUM_CHANNELS];
volatile uint16_t pwm_val[NUM_CHANNELS];

void handle_servo_intr(void);
void handle_throt_intr(void);
inline void handle_interrupt(uint8_t pin_id, bool change);

void receiver_init(void) {
  // reciever pin modes
  RECEIVER_DDR &= ~(_BV(RECEIVER_SERVO_PIN)|_BV(RECEIVER_THROT_PIN));
  RECEIVER_PORT |= _BV(RECEIVER_SERVO_PIN)|_BV(RECEIVER_THROT_PIN); // pullups

  // attach unique pin interrupts for throttle and servo
  EICRA = _BV(ISC10)|_BV(ISC00);
  EIMSK = _BV(INT0)|_BV(INT1);

  sei();
}

uint16_t receiver_get_pwm(uint8_t index) {
  return pwm_val[index];
}

inline void handle_interrupt(uint8_t pin_id, bool change) {
  // handle the pwm counters
  uint32_t micros = time_micros();
  if (change) {
    prev_time[pin_id] = micros;
  } else {
    if (micros < prev_time[pin_id]) {
      // overflow happened
      pwm_val[pin_id] = (UINT32_MAX - prev_time[pin_id]) + time_micros();
    } else {
      pwm_val[pin_id] = time_micros() - prev_time[pin_id];
    }
  }
}

ISR(INT0_vect) {
  handle_interrupt(SERVO_ID, PIND&_BV(PIND2));
}

ISR(INT1_vect) {
  handle_interrupt(THROT_ID, PIND&_BV(PIND3));
}