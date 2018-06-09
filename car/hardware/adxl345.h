#ifndef ADXL345_
#define ADXL345_

// 3 axis accelerometer

#define NUM_AXES 3

typedef uint16_t accel_vals_t[NUM_AXES];

void accel_init(void);
void accel_calibrate(void);
void accel_set_datum(accel_vals_t accel_vals);
void accel_read_angles(accel_vals_t accel_vals);
void accel_read_rates(accel_vals_t accel_vals);

#endif // ADXL345_