#ifndef ACTUATOR_
#define ACTUATOR_

void actuator_init(void);
void actuator_write_servo(uint16_t width);
void actuator_write_throt(uint16_t width);
void actuator_idle(void);

#endif