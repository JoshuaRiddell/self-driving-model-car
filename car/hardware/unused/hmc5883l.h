#ifndef HMC5883L_
#define HMC5883L_

// 3 axis compass

#define NUM_AXES 3

typedef uint16_t compass_vals_t[NUM_AXES];

void compass_init(void);
void compass_calibrate(void);
void compass_set_datum(compass_vals_t compass_vals);
void compass_read_angles(compass_vals_t compass_vals);
void compass_read_rates(compass_vals_t compass_vals);

#endif // HMC5883L_