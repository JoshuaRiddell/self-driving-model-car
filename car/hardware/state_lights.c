#include "state_lights.h"

#define NUM_LIGHTS 4

const byte lights[] = { WHITE, BLUE, GREEN, RED };

// set up light pin modes and set to default state
void state_lights_init() {
  // setup lights pinmode
  for (int i = 0; i < NUM_LIGHTS; ++i) {
    pinMode(lights[i], OUTPUT);
  }

  // strum the lights 3 times for added jazz
  for (int n = 0; n < 3; ++n) {
    state_lights_strum();
  }

  state_lights_set(WHITE);
}

// "wave" effect going through the light colours
void state_lights_strum() {
  for (int i = 0; i < NUM_LIGHTS; ++i) {
    digitalWrite(lights[i], HIGH);
    delay(30);
  }

  for (int i = 0; i < NUM_LIGHTS; ++i) {
    digitalWrite(lights[i], LOW);
    delay(30);
  }
}

// set a light
void state_lights_set(int pin) {
  digitalWrite(pin, HIGH);
}

// clear a light
void state_lights_clear(int pin) {
  digitalWrite(pin, LOW);
}

// clear all lights
void state_lights_clear_all() {
  for (int i = 0; i < NUM_LIGHTS; ++i) {
    digitalWrite(lights[i], LOW);
  }
}

// toggle a light value
void state_lights_toggle(int pin) {
  digitalWrite(pin, !digitalRead(pin));
}

