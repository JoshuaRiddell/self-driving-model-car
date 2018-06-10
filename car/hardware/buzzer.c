#include <avr/io.h>
#include <util/delay.h>

#include "buzzer.h"

static void delay_us(uint16_t delay);

void buzzer_init() {
#ifndef DISABLE_BUZZER
  BUZZER_DDR |= _BV(BUZZER_PIN);
#else
  BUZZER_DDR &= ~_BV(BUZZER_PIN);
#endif

  buzzer_play_sound(SOUND_LOW);
}

void buzzer_play_sound(uint16_t frequency) {
  for (uint16_t i = 0; i < BUZZ_DURATION/frequency; i++) {
    BUZZER_PORT |= _BV(BUZZER_PIN);
    delay_us(frequency);
    BUZZER_PORT &= ~_BV(BUZZER_PIN);
    delay_us(frequency);
    BUZZER_PORT |= _BV(BUZZER_PIN);
    delay_us(frequency);
    BUZZER_PORT &= ~_BV(BUZZER_PIN);
    delay_us(frequency);
  }
}

static void delay_us(uint16_t delay) {
  delay = delay/5;
  for (uint16_t i = 0; i < delay; ++i) {
    _delay_us(5);
  }
}