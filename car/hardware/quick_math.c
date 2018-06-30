#include <stdbool.h>
// #include <stdio.h>

#include "quick_math.h"

#include "lookup_sin.h"

#define NUM_SAMPLES 255
#define ANGLE_MAX 36000
#define ANGLE_MAX_QUARTER 9000
#define ANGLE_MAX_HALF 18000
#define ANGLE_MAX_THREE_QUARTER 27000

int16_t quick_math_sin_cos(uint16_t theta, bool is_cos) {
    uint8_t quadrant;
    uint16_t theta_orig;
    int16_t retval;

    // 0us

    theta %= ANGLE_MAX;
    // 2us

    if (theta <= ANGLE_MAX_QUARTER) {
        quadrant = 0;
    } else if (theta <= ANGLE_MAX_HALF) {
        quadrant = 1;
    } else if (theta <= ANGLE_MAX_THREE_QUARTER) {
        quadrant = 2;
    } else {
        quadrant = 3;
    }
    // 1us

    if (is_cos) {
        ++quadrant;
        quadrant %= 4;
    }
    // 0us

    theta_orig = theta;
    // 0us

    theta %= ANGLE_MAX_QUARTER;
    // 16us

    if (theta == 0) {
        switch ((theta_orig / ANGLE_MAX_QUARTER) % 4) {
            case 0:
            case 2:
                retval = 0;
                break;
            case 1:
                retval = 1 * QUICK_MATH_MULTIPLIER;
                break;
            case 3:
                retval = -1 * QUICK_MATH_MULTIPLIER;
                break;
        }
        return retval;
    }
    // 0us

    if (quadrant == 1 || quadrant == 3) {
        theta = ANGLE_MAX_QUARTER - theta;
    }
    // 0us

    // uint32_t before_divide = (uint32_t)(theta) * NUM_SAMPLES;
    // uint16_t index = before_divide / ANGLE_MAX_QUARTER;
    // uint16_t rem = before_divide % ANGLE_MAX_QUARTER;

    // uint16_t const *lowerp = lookup_sin + index;

    // uint16_t lower = *(lowerp);
    // uint16_t upper = *(lowerp+1);

    // retval = lower + (upper - lower) * rem / ANGLE_MAX_QUARTER;

    retval = lookup_sin[(uint32_t)(theta) * NUM_SAMPLES / ANGLE_MAX_QUARTER];
    // 68us

    if (quadrant >= 2) {
        retval = -retval;
    }
    // 1us

    return retval;
}