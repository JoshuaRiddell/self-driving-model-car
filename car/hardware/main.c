#include <stdio.h>

#include <util/delay.h>

#include "config.h"
// #include "ranging.h"
#include "leds.h"
#include "receiver.h"
#include "power.h"
#include "serial.h"
#include "config.h"
#include "time.h"
#include "buzzer.h"
#include "actuator.h"

#include <avr/io.h>


// TODO
// add proper tones
// arg checking on serial input
// wall, cpu, tract voltage sensing

// define flow control states
// void wait_for_arm(void);
// void wait_for_start(void);
// void manual_control(void);

void hardware_init(void);

int main() {
  hardware_init();

  printf(">>>STARTUP<<<\n");

  leds_set(LEDS_1);

  power_esc_on();

  receiver_passthrough_set();
  while (1) {
    printf("vals: %X; %u %u %u\n",
        PINC,
        power_read_index(0),
        power_read_index(1),
        power_read_index(2));
    _delay_ms(1000);
  }

  return 0;
}

void hardware_init(void) {
  time_init();
  serial_init(SERIAL_BAUD);
  leds_init();
  receiver_init();
  buzzer_init();
  power_init(POWER_ADAPTIVE);
  actuator_init();
}

// // setup peripherals
// void setup() {
//   power_init();
//   serial_init(SERIAL_BAUD);
//   leds_init();
//   receiver_init();
//   buzzer_init();
//   sonar_init();
//   actuator_init();
// }
// 
// void loop() {
//   // disarmed state - brake applied and 1 layer of protection before automatic
//   // driving starts. To move to next stage pull trigger for 2 seconds then
//   // release.
//   Serial.write(SERIAL_DISARMED);
//   wait_for_arm();

//   // armed state - a single pull of the trigger will start the car
//   Serial.write(SERIAL_ARMED);
//   wait_for_start();

//   // in automatic mode - send serial to the pc to trigger serial commands
//   Serial.write(SERIAL_AUTO);

// #ifdef SONAR
//   unsigned long last_sonar = 0;  // the time that the sonar was last read
// #endif

//   // main automatic control loop
//   while (true) {
//     if (receiver_get_pwm(THROT_ID) < SHUTDOWN_THRESH) {
//       // return manual control if sitck pushed forward
//       Serial.write(SERIAL_MANUAL);
//       manual_control();
//       break;
//     }

//     // TODO read sonar here

//     // take pwm value serial input from the computer
//     if (Serial.available()) {
//       // read two bytes of input
//       Serial.readBytes(incomingBuffer, BUFFER_SIZE);
//       // write command to peripheral
//       actuator_write_index(incomingBuffer[0], incomingBuffer[1]);
//     }
//   }
// }

// // sequence for initial arming. Waits for the trigger to be pulled
// // for 2 seconds then to be released before it progresses
// void wait_for_arm() {
//   // set white light
//   leds_clear_all();
//   leds_set(WHITE);

//   // wait for the trigger to be pressed for more than 2 seconds
//   uint8_t timer_counter = 0;
//   while (true) {
//     if (receiver_get_pwm(THROT_ID) > STARTUP_THRESH) {
//       // if trigger is pulled then increment timer
//       timer_counter += 1;
//       if (timer_counter == 1) {
//         // if trigger was only just pulled then set a light and play sound
//         leds_set(BLUE);
//         buzzer_play_sound(SOUND_LOW);
//       } else if (timer_counter > ARM_CUTOFF / 50) {
//         // if we exceeded time about then continue
//         break;
//       }
//     } else {
//       // if trigger was released then reset counter and clear blue light
//       leds_clear(BLUE);
//       timer_counter = 0;
//     }
//     delay(50);
//   }

//   // set red armed light and play a sound
//   leds_set(RED);
//   buzzer_play_sound(SOUND_HIGH);
//   delay(100);
//   buzzer_play_sound(SOUND_HIGH);

//   // wait for trigger to be released
//   while (receiver_get_pwm(THROT_ID) > STARTUP_THRESH) {
//     ;
//   }

//   // play a and set leds to armed mode state
//   buzzer_play_sound(SOUND_LOW);
//   leds_set(GREEN);
//   leds_clear(BLUE);
//   leds_clear(RED);
//   // currently lit: white + green
//   delay(100);
// }

// // sequence for starting. Waits for the remote trigger to be pressed.
// void wait_for_start() {
//   // set lights to armed state
//   leds_clear_all();
//   leds_set(WHITE);
//   leds_set(GREEN);

//   // wait for trigger to be pressed
//   while (receiver_get_pwm(THROT_ID) < STARTUP_THRESH) {
//     ;
//   }

//   // play a sound and set to auto mode lights
//   buzzer_play_sound(SOUND_HIGH);
//   leds_clear(WHITE);
//   // currently lit: green
// }

// // move to manual control loop feeding input from remote to output pins
// void manual_control() {
//   // set throttle to neutral and steering to neutral
//   actuator_idle();

//   // set lights to manual control
//   leds_clear_all();
//   leds_set(BLUE);
//   leds_set(GREEN);
//   buzzer_play_sound(SOUND_HIGH);

//   // delay to allow user to remove finger from brake to prevent a reverse
//   delay(1000);

//   // main manual control loop
//   uint8_t timer_counter = 0;
//   while (true) {
//     // set outputs to the remote inputs
//     actuator_write_index(THROT_ID, receiver_get_pwm(THROT_ID));
//     actuator_write_index(SERVO_ID, receiver_get_pwm(SERVO_ID));

//     // check if the throttle is at idle and steering servo at full right to
//     // exit full auto mode.
//     if (receiver_get_pwm(THROT_ID) < THROTTLE_IDLE &&
//         receiver_get_pwm(SERVO_ID) > STEERING_THRESH) {
//       timer_counter += 1;
//       if (timer_counter > MANUAL_CUTOFF / MANUAL_DELAY) {
//         // if we were in the above conditions for enough time then
//         // exit manual mode
//         buzzer_play_sound(SOUND_HIGH);
//         break;
//       }
//     } else {
//       // reset counter if not in above conditions
//       timer_counter = 0;
//     }

//     delay(MANUAL_DELAY);
//   }

//   // idle throttle and centre steering again
//   actuator_idle();
// }

