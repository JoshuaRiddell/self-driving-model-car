#ifndef ACTUATOR_
#define ACTUATOR_

void actuator_init(void);
void actuator_write_index(uint8_t index, uint8_t val);
void actuator_idle(void);

#endif