#include "buzzer.h"



void setup_buzzer() {
  pinMode(BUZZER_PIN, OUTPUT);
}

void play_sound(uint16_t frequency) {
#ifdef BUZZER
  
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
