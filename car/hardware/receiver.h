#ifndef RECEIVER_
#define RECEIVER_

#include <stdbool.h>

#include "config.h"

void receiver_init(void);
uint16_t receiver_get_pwm(uint8_t index);
void receiver_passthrough(bool pass);

#define receiver_passthrough_set() receiver_passthrough(true)
#define receiver_passthrough_clear() receiver_passthrough(false)

#endif  // RECEIVER_
