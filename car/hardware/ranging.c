#include "ranging.h"

// define ultrasonic sensor storage
uint8_t last_send = 0;
uint8_t last_reading = 0;
uint8_t current_ping = 0;
NewPing sonar(SONAR_TRIG, SONAR_ECHO, SONAR_TRIGGER);

int get_sonar() {
  current_ping = sonar.ping_cm();
  if (current_ping && !last_send) {
    // inside range
    if (last_reading) {
      Serial.print(1);
      last_send = 1;
    }
    last_reading = 1;
  } else if (!current_ping && last_send) {
    // outside range
    if (!last_reading) {
      last_send = 0;
    }
    last_reading = 0;
  }
}

