#include <avr/io.h>
#include <util/delay.h>

#include "leds.h"
#include "config.h"

#define NUM_LIGHTS 4

#define ALL_LEDS (_BV(WHITE_PIN)|_BV(BLUE_PIN)|_BV(GREEN_PIN)|_BV(RED_PIN))

const uint8_t lights[] = { WHITE_PIN, BLUE_PIN, GREEN_PIN, RED_PIN };

// set up light pin modes and set to default state
void leds_init() {
  // setup lights pinmode
  LEDS_DDR = ALL_LEDS;

  // strum the lights 3 times for added jazz
  for (uint8_t n = 0; n < 3; ++n) {
    leds_strum();
  }

  leds_set(LEDS_WHITE);
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
  LEDS_PORT |= _BV(lights[pin]);
}

// clear a light
void leds_clear(uint8_t pin) {
  LEDS_PORT &= ~_BV(lights[pin]);
}

// clear all lights
void leds_clear_all() {
  LEDS_PORT &= ~(ALL_LEDS);
}

// toggle a light value
void leds_toggle(uint8_t pin) {
  LEDS_PORT ^= _BV(lights[pin]);
}

