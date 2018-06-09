#include "power.h"

#ifdef POWER_DEBUG_MSG
    #define POWER_SERIAL_PRINT(...) Serial.print(__VA_ARGS__)
#else
    #define POWER_SERIAL_PRINT()
#endif

#define ESC_INIT() pinMode(CTL_ESC, OUTPUT); digitalWrite(CTL_ESC, LOW)
#define ESC_ON() digitalWrite(CTL_ESC, HIGH)
#define ESC_OFF() digitalWrite(CTL_ESC, LOW)

#define WALL_INIT() pinMode(CTL_WALL, OUTPUT); digitalWrite(CTL_WALL, LOW)
#define WALL_ON() digitalWrite(CTL_WALL, HIGH)
#define WALL_OFF() digitalWrite(CTL_WALL, LOW)

#define CPU_BATT_INIT() pinMode(CTL_CPU_BATT, OUTPUT); digitalWrite(CTL_CPU_BATT, HIGH)
#define CPU_BATT_ON() digitalWrite(CTL_CPU_BATT, HIGH)
#define CPU_BATT_OFF() digitalWrite(CTL_CPU_BATT, LOW)

static uint8_t power_mode = POWER_ADAPTIVE;
static volatile bool wall_connected = false;

void power_init(void) {
    POWER_SERIAL_PRINT("power: init\n");

    CPU_BATT_INIT();
    WALL_INIT();
    ESC_INIT();

    power_mode = POWER_ADAPTIVE;
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
            if (digitalRead(SENSE_WALL)) {
                // wall power is connected
                POWER_SERIAL_PRINT("power: wall power connected\n");
                WALL_ON();
                CPU_BATT_OFF();
            } else {
                // wall power is not connected
                POWER_SERIAL_PRINT("power: wall power disconnected\n");
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
    POWER_SERIAL_PRINT("power: interrupt\n");
    update_wall_power();
}