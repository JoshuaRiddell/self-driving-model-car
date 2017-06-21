#include "state_lights.h"

// set up light pin modes and set to default state
void setup_lights() {
  // setup lights pinmode
  for (int i = 0; i < NUM_LIGHTS; ++i) {
    pinMode(lights[i], OUTPUT);
  }

  // strum the lights 3 times for added jazz
  for (int n = 0; n < 3; ++n) {
    strum_lights();
  }

  set_light(WHITE);
}

// "wave" effect going through the light colours
void strum_lights() {
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
void set_light(int pin) {
  digitalWrite(pin, HIGH);
}

// clear a light
void clear_light(int pin) {
  digitalWrite(pin, LOW);
}

// clear all lights
void clear_all_lights() {
  for (int i = 0; i < NUM_LIGHTS; ++i) {
    digitalWrite(lights[i], LOW);
  }
}

// toggle a light value
void toggle_light(int pin) {
  digitalWrite(pin, !digitalRead(pin));
}

