#include <avr/io.h>
#include <avr/interrupt.h>

#include "config.h"

#include "power.h"

#define ESC_INIT() CTL_ESC_DDR |= _BV(CTL_ESC_PIN); ESC_OFF()
#define ESC_ON() CTL_ESC_PORT |= _BV(CTL_ESC_PIN)
#define ESC_OFF() CTL_ESC_PORT &= ~_BV(CTL_ESC_PIN)

#define WALL_INIT() CTL_CPU_DDR |= _BV(CTL_WALL_PIN); WALL_OFF()
#define WALL_ON() CTL_CPU_PORT |= _BV(CTL_WALL_PIN)
#define WALL_OFF() CTL_CPU_PORT &= ~_BV(CTL_WALL_PIN)

#define CPU_BATT_INIT() CTL_CPU_DDR |= _BV(CTL_CPU_BATT_PIN); CPU_BATT_OFF()
#define CPU_BATT_ON() CTL_CPU_PORT |= _BV(CTL_CPU_BATT_PIN)
#define CPU_BATT_OFF() CTL_CPU_PORT &= ~_BV(CTL_CPU_BATT_PIN)

static void update_wall_power();

static uint8_t power_mode = POWER_ADAPTIVE;

void power_init(uint8_t mode) {
    CPU_BATT_INIT();
    WALL_INIT();
    ESC_INIT();

    SENSE_DDR &= ~(_BV(SENSE_WALL_PIN)|
                    _BV(SENSE_CPU_BATT_PIN)|
                    _BV(SENSE_TRACT_BATT_PIN));

    power_mode = mode;

    update_wall_power();

    PCMSK1 = _BV(CTL_WALL_INTERRUPT);
    PCICR = _BV(CTL_WALL_INTERRUPT_ENABLE);

    sei();
}

void power_esc_set(bool val) {
    if (val) {
        ESC_ON();
    } else {
        ESC_OFF();
    }
}

void power_set_cpu_mode(uint8_t mode) {
    power_mode = mode;
    update_wall_power();
}

static void update_wall_power() {
    switch(power_mode) {
        case POWER_ADAPTIVE:
            if (SENSE_PIN&_BV(SENSE_WALL_PIN)) {
                // wall power is connected
                WALL_ON();
                CPU_BATT_OFF();
            } else {
                // wall power is not connected
                CPU_BATT_ON();
                WALL_OFF();
            }
            break;
        case POWER_WALL:
            // we want to force wall power
            WALL_ON();
            CPU_BATT_OFF();
            break;
        case POWER_BATTERY:
            // we want to force battery power
            CPU_BATT_ON();
            WALL_OFF();
            break;
    }
}

// raise interrupt when wall power detected
ISR(PCINT1_vect) {
    update_wall_power();
}