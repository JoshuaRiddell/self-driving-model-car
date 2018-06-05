#ifndef POWER_
#define POWER_

#include <stdbool.h>

#define POWER_ADAPTIVE 0
#define POWER_WALL 1
#define POWER_BATTERY 2

void power_init(void);
void power_esc_set(bool val);
void power_set_cpu_mode(uint8_t mode);

#endif  // POWER_
