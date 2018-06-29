#include <avr/io.h>
#include <util/delay.h>

#include "leds.h"
#include "config.h"

#define NUM_LIGHTS 2

const uint8_t lights[] = { LEDS_1_PIN, LEDS_2_PIN };

// set up light pin modes and set to default state
void leds_init() {
  // setup lights pinmode
  LEDS_1_DDR |= _BV(LEDS_1_PIN);
  LEDS_2_DDR |= _BV(LEDS_2_PIN);

  // strum the lights 3 times for added jazz
  for (uint8_t n = 0; n < 3; ++n) {
    leds_strum();
  }
}

// "wave" effect going through the light colours
void leds_strum() {
  for (uint8_t i = 0; i < NUM_LIGHTS; ++i) {
    leds_set(i);
    _delay_ms(30);
  }

  for (uint8_t i = 0; i < NUM_LIGHTS; ++i) {
    leds_clear(i);
    _delay_ms(30);
  }
}

// set a light
void leds_set(uint8_t pin) {
  switch (pin) {
    case LEDS_1:
      LEDS_1_PORT |= _BV(lights[pin]);
      break;
    case LEDS_2:
      LEDS_1_PORT |= _BV(lights[pin]);
      break;
  }
}

// clear a light
void leds_clear(uint8_t pin) {
  switch (pin) {
    case LEDS_1:
      LEDS_1_PORT &= ~_BV(lights[pin]);
      break;
    case LEDS_2:
      LEDS_2_PORT &= ~_BV(lights[pin]);
      break;
  }
}

// clear all lights
void leds_clear_all() {
  LEDS_1_PORT &= ~_BV(LEDS_1_PIN);
  LEDS_2_PORT &= ~_BV(LEDS_2_PIN);
}

// toggle a light value
void leds_toggle(uint8_t pin) {
  switch (pin) {
    case LEDS_1:
      LEDS_1_PORT ^= _BV(lights[pin]);
      break;
    case LEDS_2:
      LEDS_2_PORT ^= _BV(lights[pin]);
      break;
  }
}

