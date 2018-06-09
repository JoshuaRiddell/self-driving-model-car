#include <avr/io.h>
#include <avr/interrupt.h>

#include <stdio.h>

#include "time.h"

#define PRESCALER 8  //1/8
#define TIMER_PERIOD 1  //ms
#define OCR_VAL (TIMER_PERIOD * F_CPU / PRESCALER / 1000)
#define COUNT_TO_MICROS(val) ((val + 1) / 2) // PRESCALER / (F_CPU / 1000000))
#define COUNT_TO_MILLIS(val) ((val + 1000) / 2000) // PRESCALER / 1000 / (F_CPU / 1000000))

static uint32_t millis;

void time_init(void) {
    millis = 0;

    TCCR1A = 0;    // CTC mode
    TCCR1B = _BV(CS11)|_BV(WGM12);     // 1/8 scaler
    TIMSK1 = _BV(OCIE1A);  // set interrupt on compa
    OCR1A = (uint16_t)OCR_VAL;        // count up to timer period

    sei();         //enable interrupts
}

uint32_t time_millis(void) {
    return millis + COUNT_TO_MILLIS(TCNT1);
}

uint32_t time_micros(void) {
    // millis*1000 (no overflow) + residual from timer
    return ( (millis % ((UINT32_MAX+500)/1000)) * 1000)
            + COUNT_TO_MICROS(TCNT1);
}

ISR (TIMER1_COMPA_vect) {
    // update the counters
    millis += TIMER_PERIOD;
}

