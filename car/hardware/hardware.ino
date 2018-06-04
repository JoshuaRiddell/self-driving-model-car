#include <NewPing.h>
#include <Servo.h>

#include "config.h"
#include "ranging.h"
#include "state_lights.h"
#include "receiver.h"
#include "buzzer.h"

// TODO
// add proper tones
// add status LEDs
// arg checking on serial input

// define pin arrays
Servo output_pins[NUM_CHANNELS];

// define incoming bytes buffer
byte incomingBuffer[BUFFER_SIZE];

void wait_for_arm(void);
void wait_for_start(void);
void reset_outputs(void);
void manual_control(void);

// setup peripherals
void setup() {
  // status light pins
  setup_lights();

  // rc receiver pwm input
  setup_receiver();

#ifdef ENABLE_BUZZER
  // status buzzer
  setup_buzzer();
#endif

  // start serial
#ifdef ENABLE_DEBUG
  Serial.begin(SERIAL_BAUD);
#endif

#ifdef SONAR
  // sonar pin modes
  pinMode(SONAR_TRIG, OUTPUT);
  pinMode(SONAR_ECHO, INPUT);
#endif

  // output pin pwm settings
  output_pins[SERVO_ID].attach(SERVO_TX);
  output_pins[THROT_ID].attach(THROT_TX);

  output_pins[SERVO_ID].write(SERVO_IDLE);
  output_pins[THROT_ID].write(THROT_IDLE);
}

void loop() {
  // disarmed state - brake applied and 1 layer of protection before automatic
  // driving starts. To move to next stage pull trigger for 2 seconds then
  // release.
  Serial.write(SERIAL_DISARMED);
  wait_for_arm();

  // armed state - a single pull of the trigger will start the car
  Serial.write(SERIAL_ARMED);
  wait_for_start();

  // in automatic mode - send serial to the pc to trigger serial commands
  Serial.write(SERIAL_AUTO);

#ifdef SONAR
  unsigned long last_sonar = 0;  // the time that the sonar was last read
#endif

  // main automatic control loop
  while (true) {
    if (get_pwm(THROT_ID) < SHUTDOWN_THRESH) {
      // return manual control if sitck pushed forward
      Serial.write(SERIAL_MANUAL);
      manual_control();
      break;
    }

#ifdef SONAR
    if (millis() - last_sonar > SONAR_DELAY) {
      // TODO read the sonar here
      last_sonar = millis();
    }
#endif

    // take pwm value serial input from the computer
    if (Serial.available()) {
      // read two bytes of input
      Serial.readBytes(incomingBuffer, BUFFER_SIZE);
      // write computer command to pwm peripheral
      output_pins[incomingBuffer[0]].write(incomingBuffer[1]);
    }
  }
}

// sequence for initial arming. Waits for the trigger to be pulled
// for 2 seconds then to be released before it progresses
void wait_for_arm() {
  // set white light
  clear_all_lights();
  set_light(WHITE);

  // wait for the trigger to be pressed for more than 2 seconds
  uint8_t timer_counter = 0;
  while (true) {
    if (get_pwm(THROT_ID) > STARTUP_THRESH) {
      // if trigger is pulled then increment timer
      timer_counter += 1;
      if (timer_counter == 1) {
        // if trigger was only just pulled then set a light and play sound
        set_light(BLUE);
        play_sound(SOUND_LOW);
      } else if (timer_counter > ARM_CUTOFF / 50) {
        // if we exceeded time about then continue
        break;
      }
    } else {
      // if trigger was released then reset counter and clear blue light
      clear_light(BLUE);
      timer_counter = 0;
    }
    delay(50);
  }

  // set red armed light and play a sound
  set_light(RED);
  play_sound(SOUND_HIGH);
  delay(100);
  play_sound(SOUND_HIGH);

  // wait for trigger to be released
  while (get_pwm(THROT_ID) > STARTUP_THRESH) {
    ;
  }

  // play a and set leds to armed mode state
  play_sound(SOUND_LOW);
  set_light(GREEN);
  clear_light(BLUE);
  clear_light(RED);
  // currently lit: white + green
  delay(100);
}

// sequence for starting. Waits for the remote trigger to be pressed.
void wait_for_start() {
  // set lights to armed state
  clear_all_lights();
  set_light(WHITE);
  set_light(GREEN);

  // wait for trigger to be pressed
  while (get_pwm(THROT_ID) < STARTUP_THRESH) {
    ;
  }

  // play a sound and set to auto mode lights
  play_sound(SOUND_HIGH);
  clear_light(WHITE);
  // currently lit: green
}

// move to manual control loop feeding input from remote to output pins
void manual_control() {
  // set throttle to neutral and steering to neutral
  reset_outputs();

  // set lights to manual control
  clear_all_lights();
  set_light(BLUE);
  set_light(GREEN);
  play_sound(SOUND_HIGH);

  // delay to allow user to remove finger from brake to prevent a reverse
  delay(1000);

  // main manual control loop
  uint8_t timer_counter = 0;
  while (true) {
    // set outputs to the remote inputs
    output_pins[SERVO_ID].writeMicroseconds(get_pwm(SERVO_ID));
    output_pins[THROT_ID].writeMicroseconds(get_pwm(THROT_ID));

    // check if the throttle is at idle and steering servo at full right to
    // exit full auto mode.
    if (get_pwm(THROT_ID) < THROTTLE_IDLE &&
        get_pwm(SERVO_ID) > STEERING_THRESH) {
      timer_counter += 1;
      if (timer_counter > MANUAL_CUTOFF / MANUAL_DELAY) {
        // if we were in the above conditions for enough time then
        // exit manual mode
        play_sound(SOUND_HIGH);
        break;
      }
    } else {
      // reset counter if not in above conditions
      timer_counter = 0;
    }

    delay(MANUAL_DELAY);
  }

  // idle throttle and centre steering again
  reset_outputs();
}

// idle throttle and centre steering
void reset_outputs() {
  output_pins[SERVO_ID].writeMicroseconds(SERVO_IDLE);
  output_pins[THROT_ID].writeMicroseconds(THROT_IDLE);
}



































