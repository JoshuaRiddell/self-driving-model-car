#include "state_lights.h"

void setup_lights() {
  for (int n = 0; n < 3; ++n) {
    strum_lights();
  }

  set_light(WHITE);
}

void strum_lights() {
  for (int i = 0; i < NUM_LIGHTS; ++i) {
    pinMode(lights[i], OUTPUT);
    digitalWrite(lights[i], HIGH);
    delay(30);
  }

  for (int i = 0; i < NUM_LIGHTS; ++i) {
    pinMode(lights[i], OUTPUT);
    digitalWrite(lights[i], LOW);
    delay(30);
  }
}

void set_light(int pin) {
  digitalWrite(pin, HIGH);
}

void clear_light(int pin) {
  digitalWrite(pin, LOW);
}

void clear_all_lights() {
  for (int i = 0; i < NUM_LIGHTS; ++i) {
    digitalWrite(lights[i], LOW);
  }
}

void toggle_light(int pin) {
  digitalWrite(pin, !digitalRead(pin));
}

