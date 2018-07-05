#ifndef RECEIVER_
#define RECEIVER_

#include "config.h"

// input pin numbers
#define SERVO_RX 2
#define THROT_RX 3

void receiver_init(void);
void receiver_receiver_get_pwm(uint8_t index);

#endif  // RECEIVER_
