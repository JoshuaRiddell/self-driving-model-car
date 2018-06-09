#include <Wire.h>
#include "l3g4200d.h"

#define I2C_ADDR 0x69

void gyro_init(void) {
    Wire.beginTransmission(I2C_ADDR);

    Wire.endTransmission();
}

void gyro_calibrate(void) {

}

void gyro_set_datum(gyro_t gyro) {

}

void gyro_read_angles(gyro_t gyro) {

}

void gyro_read_rates(gyro_t gyro) {

}

