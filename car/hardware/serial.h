#ifndef SERIAL_
#define SERIAL_

#include <stdbool.h>

void serial_init(long baud);
bool serial_available(void);
void serial_clear_input(void);
int serial_get_char(FILE* stream);

#endif // SERIAL_