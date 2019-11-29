#ifndef ACTUATOR_
#define ACTUATOR_

#include "actuator.h"

void actuator_init(void);
void actuator_write_index(uint8_t index, uint16_t val);
void actuator_write_index_byte(uint8_t index, uint8_t val);
void actuator_idle(void);

#endif