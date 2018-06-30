#ifndef QUICK_MATH_
#define QUICK_MATH_

#include <stdint.h>

#define QUICK_MATH_MULTIPLIER 2000

#define quick_math_sin(theta) quick_math_sin_cos(theta, false)
#define quick_math_cos(theta) quick_math_sin_cos(theta, true)

int16_t quick_math_sin_cos(uint16_t theta, bool is_cos);

#endif  // QUICK_MATH_