// #include "power.h"

// static uint8_t power_mode = POWER_ADAPTIVE;

// void power_init(void) {
//     power_mode = POWER_ADAPTIVE;

//     pinMode(SENSE_WALL, INPUT);
//     pinMode(SENSE_CPU_BATT, INPUT);
//     pinMode(SENSE_TRACT_BATT, INPUT);

//     PCMSK = (1<<PCINT9);
//     PCICR = (1<<PCIE1);

//     sei();
// }

// void power_esc_set(bool val) {

// }

// void power_set_cpu_mode(uint8_t mode) {

// }

// // raise interrupt when wall power detected
// ISR(PCINT1_vect) {
//     if (PINC & _BV(PC1)) {
//         // power is connected
//     } else {
//         // power is disconnected
//     }
// }