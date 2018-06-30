#include <avr/io.h>
#include <avr/interrupt.h>

#include <math.h>

#include "config.h"
#include "encoder.h"

#include "leds.h"

// adapted from:
// https://pdfs.semanticscholar.org/81a3/be4b99836b761d218fabff8a2f03c24fbf65.pdf

#define DEGREES_PER_COUNT 10
#define WHEEL_RADIUS 40
#define HALF_TRACK_WIDTH 100

#define TRIG_OFFSET 1000
#define THETA_OFFSET 1000

static int16_t last_sin;
static int16_t last_cos;
static pos_t current_pos;

static volatile uint8_t last_pin;

static volatile uint16_t encoder_l = 0;
static volatile uint16_t encoder_r = 0;

void encoder_init(void) {
    ENCODER_DDR &= ~(_BV(ENCODER_LEFT_PIN)|_BV(ENCODER_RIGHT_PIN));

    PCMSK1 = _BV(ENCODER_LEFT_INTERRUPT)|_BV(ENCODER_RIGHT_INTERRUPT);
    PCICR = _BV(ENCODER_INTERRUPT_ENABLE);

    encoder_reset_pos();
}

void encoder_reset_pos(void) {
    current_pos.x = 0;
    current_pos.y = 0;
    current_pos.theta = 1.571*THETA_OFFSET;

    last_sin = 0;
    last_cos = 0;

    cli();
    encoder_l = 0;
    encoder_r = 0;
    sei();
}

void encoder_update(void) {
    cli();
    uint16_t el = encoder_l;
    uint16_t er = encoder_r;

    encoder_l = 0;
    encoder_r = 0;
    sei();

    printf("encoders: %u:%u  ", el, er);

    if (el == er) {
        uint16_t ds = WHEEL_RADIUS * DEGREES_PER_COUNT * el;
        current_pos.x += ds * last_sin;
        current_pos.y += ds * last_cos;
    } else {
        int16_t R = (HALF_TRACK_WIDTH * (er + el));
        R /= (int16_t)(er - el);

        printf("R:%d   %d %d     ", R, HALF_TRACK_WIDTH * (er + el), ((int16_t)er - el));
        
        current_pos.theta += WHEEL_RADIUS * DEGREES_PER_COUNT / 2 * ((int16_t)er - el);

        int16_t this_sin = (int16_t) (TRIG_OFFSET *
                sin(((float)current_pos.theta) / THETA_OFFSET));
        int16_t this_cos = (int16_t) (TRIG_OFFSET *
                cos(((float)current_pos.theta) / THETA_OFFSET));

        current_pos.x += R * (this_sin - last_sin);
        current_pos.y += R * (this_cos - last_cos);

        printf("  calc: %d; %d %d   ", R, this_sin, this_cos);

        last_sin = this_sin;
        last_cos = this_cos;
    }
}

void encoder_get_pos(pos_t *pos) {
    pos->x = current_pos.x;
    pos->y = current_pos.y;
    pos->theta = current_pos.theta;
}

ISR(PCINT1_vect) {
    leds_toggle(LEDS_1);
    if ((ENCODER_PIN & _BV(ENCODER_LEFT_PIN)) ^ last_pin) {
        ++encoder_l;
    } else {
        ++encoder_r;
    }
}
