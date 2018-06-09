#ifndef LEDS_
#define LEDS_

// COMBINATIONS
// white only: car is disarmed and waiting for arming by pulling the trigger back
// white + blue: car is disarmed and indicating that the trigger is pulled
// white + blue + red: car is disarmed and waiting for trigger release
// white + green: car is armed and waiting for a single trigger pull to start autonomous mode
// green only: car is armed and in autonomous mode, reading from serial input
// green + blue: car is armed and in manual mode, reading from the radio receiver

void leds_init();
void leds_strum();
void leds_set(uint8_t pin);
void leds_clear(uint8_t pin);
void leds_clear_all();
void leds_toggle(uint8_t pin);

#endif  // LEDS_

