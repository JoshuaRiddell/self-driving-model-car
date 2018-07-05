#include <avr/io.h>
#include <avr/interrupt.h>

#include <util/delay.h>

#include "config.h"

#include "power.h"

#include "leds.h"
#include "time.h"

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
#define ADC_TO_MV(val) ((uint32_t)(val) * 1875 / 128)
#define MV_TO_ADC(val) ((uint32_t)(val) * 128 / 1875)

#define WALL_INDEX 0
#define CPU_BATT_INDEX 1
#define TRACT_BATT_INDEX 2

#define DEBOUNCE_TIME 500

static void update_wall_power();
static void adc_init();

static volatile uint32_t last_change_ms = 0;
static volatile uint16_t adc_readings[3];
static const uint8_t mux_vals[3] = {
    SENSE_WALL_PIN,
    SENSE_CPU_BATT_PIN,
    SENSE_TRACT_BATT_PIN,
};
static volatile uint8_t read_index = 0;

static uint8_t power_mode = POWER_ADAPTIVE;
static uint8_t cpu_power_state = WALL_INDEX;

inline static void power_set_cpu(uint8_t index);

void power_init(uint8_t mode) {
    // cli();

    CPU_BATT_INIT();
    WALL_INIT();
    ESC_INIT();

    power_set_cpu_mode(CPU_BATT_INDEX);

    // CPU_BATT_ON();

    // power_mode = mode;

    // update_wall_power();

    // adc_init();

    // sei();
}

// static void adc_init() {
//     SENSE_DDR &= ~(_BV(SENSE_WALL_PIN)|
//                     _BV(SENSE_CPU_BATT_PIN)|
//                     _BV(SENSE_TRACT_BATT_PIN));

//     ADCSRA = _BV(ADEN)|_BV(ADIE)|_BV(ADPS0)|_BV(ADPS1)|_BV(ADPS2);

//     read_index = 0;

//     ADMUX = ADMUX_BASE|mux_vals[read_index];
//     ADCSRA |= _BV(ADSC);
// }

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
    return ADC_TO_MV(adc_readings[index]);
}

static void update_wall_power() {
    if (time_millis() - last_change_ms < DEBOUNCE_TIME) {
        return;
    }

    switch(power_mode) {
        case POWER_ADAPTIVE:
            if (adc_readings[WALL_INDEX] > adc_readings[CPU_BATT_INDEX]) {
                // wall power is connected
                power_set_cpu(WALL_INDEX);
            } else {
                // wall power is not connected
                power_set_cpu(CPU_BATT_INDEX);
            }
            break;
        case POWER_WALL:
            // we want to force wall power
            power_set_cpu(WALL_INDEX);
            break;
        case POWER_BATTERY:
            // we want to force battery power
            power_set_cpu(CPU_BATT_INDEX);
            break;
    }
}

inline static void power_set_cpu(uint8_t index) {
    if (index != cpu_power_state) {
        // update time of last change
        last_change_ms = time_millis();
        cpu_power_state = index;

        // change the state
        if (index == WALL_INDEX) {
            leds_clear(LEDS_2);
            CPU_BATT_OFF();
            WALL_ON();
        } else if (index == CPU_BATT_INDEX) {
            leds_set(LEDS_2);
            WALL_OFF();
            CPU_BATT_ON();
        }
    }
}

// ISR(ADC_vect) {
//     adc_readings[read_index] = ADC;

//     if (read_index == 0) {
//         update_wall_power();
//     }

//     ++read_index;
//     read_index %= 3;

//     ADMUX = ADMUX_BASE|mux_vals[read_index];
//     ADCSRA |= _BV(ADSC);
// }

