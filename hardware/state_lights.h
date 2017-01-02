#ifndef STATE_LIGHTS_
#define STATE_LIGHTS_

// define pins
#define WHITE 14  // on when car is in blocked flow waiting for user input
#define BLUE 15
#define GREEN 16  // car is currently armed and can move at any time
#define RED 17

// COMBINATIONS
// white only: car is disarmed and waiting for arming by pulling the trigger back
// white + blue: car is disarmed and indicating that the trigger is pulled
// white + blue + red: car is disarmed and waiting for trigger release
// white + green: car is armed and waiting for a single trigger pull to start autonomous mode
// green only: car is armed and in autonomous mode, reading from serial input
// green + blue: car is armed and in manual mode, reading from the radio receiver

#define NUM_LIGHTS 4

const byte lights[] = { WHITE, BLUE, GREEN, RED };

#endif  // STATE_LIGHTS_
