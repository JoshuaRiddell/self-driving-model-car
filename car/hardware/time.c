#include <avr/io.h>
#include <avr/interrupt.h>

#include <stdio.h>

#include "time.h"

static volatile uint32_t timer_0_overflow_count;

void time_init(void) {
    cli();

    timer_0_overflow_count = 0;

    TCCR0B = _BV(CS00)|_BV(CS01);     // 1/64 scaler
    TIMSK0 = _BV(OCIE0A);  // set interrupt on compa

    sei();         //enable interrupts
}

uint32_t time_millis(void) {
    return timer_0_overflow_count
            + (timer_0_overflow_count*24/1000)
            + TCNT0;
}

uint32_t time_micros(void) {
    return ((timer_0_overflow_count << 8) + TCNT0) << 2;
}

ISR (TIMER0_COMPA_vect) {
    // update the counters
    ++timer_0_overflow_count;
}

