#include "buzzer.h"

void buzzer_init() {
#ifndef BUZZER_DISABLE
  pinMode(BUZZER_PIN, OUTPUT);

  buzzer_play_sound(SOUND_LOW);
#endif
}

void buzzer_play_sound(uint16_t frequency) {
#ifndef BUZZER_DISABLE
  for (uint16_t i = 0; i < BUZZ_DURATION/frequency; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delayMicroseconds(frequency);
    digitalWrite(BUZZER_PIN, LOW);
    delayMicroseconds(frequency);
    digitalWrite(BUZZER_PIN, HIGH);
    delayMicroseconds(frequency);
    digitalWrite(BUZZER_PIN, LOW);
    delayMicroseconds(frequency);
  }

#endif
}
