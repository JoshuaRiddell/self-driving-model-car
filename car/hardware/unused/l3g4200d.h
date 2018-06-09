#ifndef L3G4200D_
#define L3G4200D_

// 3 axis gyroscope

#define NUM_AXES 3

typedef struct gyro_t_ {
    uint16_t values[NUM_AXES];
} gyro_t;

void gyro_init(void);
void gyro_calibrate(void);
void gyro_set_datum(gyro_t &gyro);
void gyro_read_angles(gyro_t &gyro);
void gyro_read_rates(gyro_t &gyro);

#endif // L3G4200D_