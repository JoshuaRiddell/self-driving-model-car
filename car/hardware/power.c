#include <avr/io.h>
#include <avr/interrupt.h>

#include "config.h"

#include "power.h"

#include "leds.h"

#define ESC_INIT() CTL_ESC_DDR |= _BV(CTL_ESC_PIN); ESC_OFF()
#define ESC_ON() CTL_ESC_PORT |= _BV(CTL_ESC_PIN)
#define ESC_OFF() CTL_ESC_PORT &= ~_BV(CTL_ESC_PIN)

#define WALL_INIT() CTL_WALL_DDR |= _BV(CTL_WALL_PIN); WALL_OFF()
#define WALL_ON() CTL_WALL_PORT |= _BV(CTL_WALL_PIN)
#define WALL_OFF() CTL_WALL_PORT &= ~_BV(CTL_WALL_PIN)

#define CPU_BATT_INIT() CTL_CPU_BATT_DDR |= _BV(CTL_CPU_BATT_PIN); CPU_BATT_OFF()
#define CPU_BATT_ON() CTL_CPU_BATT_PORT |= _BV(CTL_CPU_BATT_PIN)
#define CPU_BATT_OFF() CTL_CPU_BATT_PORT &= ~_BV(CTL_CPU_BATT_PIN)

#define ADMUX_BASE (_BV(REFS0))
#define ADC_TO_MV(val) ((uint32_t)(val) * 5000 / 1024)

static void update_wall_power();
static void adc_init();

static volatile uint16_t adc_readings[3];
static const uint8_t mux_vals[3] = {
    SENSE_WALL_PIN,
    SENSE_CPU_BATT_PIN,
    SENSE_TRACT_BATT_PIN,
};
static volatile uint8_t read_index = 0;

static uint8_t power_mode = POWER_ADAPTIVE;

void power_init(uint8_t mode) {
    cli();

    CPU_BATT_INIT();
    WALL_INIT();
    ESC_INIT();

    CPU_BATT_ON();

    power_mode = mode;

    update_wall_power();

    // PCMSK1 = _BV(CTL_WALL_INTERRUPT);
    // PCICR = _BV(CTL_WALL_INTERRUPT_ENABLE);

    adc_init();

    sei();
}

static void adc_init() {
    SENSE_DDR &= ~(_BV(SENSE_WALL_PIN)|
                    _BV(SENSE_CPU_BATT_PIN)|
                    _BV(SENSE_TRACT_BATT_PIN));

    ADCSRA = _BV(ADEN)|_BV(ADIE)|_BV(ADPS0)|_BV(ADPS1)|_BV(ADPS2);

    read_index = 0;

    ADMUX = ADMUX_BASE|mux_vals[read_index];
    ADCSRA |= _BV(ADSC);
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

uint16_t power_read_index(uint8_t index) {
    return ADC_TO_MV(adc_readings[index]) * 3;
}

static void update_wall_power() {
    // switch(power_mode) {
    //     case POWER_ADAPTIVE:
    //         if (SENSE_PIN&_BV(SENSE_WALL_PIN)) {
    //             // wall power is connected
    //             WALL_ON();
    //             CPU_BATT_OFF();
    //         } else {
    //             // wall power is not connected
    //             CPU_BATT_ON();
    //             WALL_OFF();
    //         }
    //         break;
    //     case POWER_WALL:
    //         // we want to force wall power
    //         WALL_ON();
    //         CPU_BATT_OFF();
    //         break;
    //     case POWER_BATTERY:
    //         // we want to force battery power
    //         CPU_BATT_ON();
    //         WALL_OFF();
    //         break;
    // }
}

// raise interrupt when wall power detected
// ISR(PCINT1_vect) {
//     update_wall_power();
// }

ISR(ADC_vect) {
    adc_readings[read_index] = ADC;
    // adc_readings[read_index] = read_index;
    // adc_readings[read_index] = 1;

    ++read_index;
    read_index %= 3;

    ADMUX = ADMUX_BASE|mux_vals[read_index];
    ADCSRA |= _BV(ADSC);
}

