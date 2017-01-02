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

void setup() {
  setup_lights();
  setup_receiver();
  
#ifdef BUZZER
  setup_buzzer();
#endif
  
  // start serial
#ifdef DEBUG
  Serial.begin(SERIAL_BAUD);
#endif

#ifdef SONAR
  // sonar pin modes
  pinMode(SONAR_TRIG, OUTPUT);
  pinMode(SONAR_ECHO, INPUT);
#endif

  // output pin modes
  output_pins[SERVO_ID].attach(SERVO_TX);
  output_pins[THROT_ID].attach(THROT_TX);
  
  output_pins[SERVO_ID].write(SERVO_IDLE);
  output_pins[THROT_ID].write(THROT_IDLE);
}

void loop() {
  wait_for_arm();
  wait_for_start();

#ifdef SONAR
  unsigned long last_sonar = 0;  // the time that the sonar was last read
#endif

  while (true) {
    if (get_pwm(THROT_ID) < SHUTDOWN_THRESH) {
      // return manual control if sitck pushed forward
      manual_control();
      break;
    }

#ifdef SONAR
    if (millis() - last_sonar > SONAR_DELAY) {
      // READ THE SONAR
      last_sonar = millis();
    }
#endif

    if (Serial.available()) {
      Serial.readBytes(incomingBuffer, BUFFER_SIZE);
      output_pins[incomingBuffer[0]].write(incomingBuffer[1]);
    }
  }
}

void wait_for_arm() {
  clear_all_lights();
  set_light(WHITE);
  
  uint8_t timer_counter = 0;
  while (true) {
    if (get_pwm(THROT_ID) > STARTUP_THRESH) {
      timer_counter += 1;
      if (timer_counter == 1) {
        set_light(BLUE);
        play_sound(SOUND_LOW);
      } else if (timer_counter > ARM_CUTOFF / 50) {
        break;
      }
    } else {
      clear_light(BLUE);
      timer_counter = 0;
    }
    delay(50);
  }

  set_light(RED);
  play_sound(SOUND_HIGH);
  delay(100);
  play_sound(SOUND_HIGH);
   
  while (get_pwm(THROT_ID) > STARTUP_THRESH) {
    ;
  }
  
  play_sound(SOUND_LOW);
  set_light(GREEN);
  clear_light(BLUE);
  clear_light(RED);
  // currently lit: white + green
  delay(100);
}

void wait_for_start() {
  clear_all_lights();
  set_light(WHITE);
  set_light(GREEN);
  
  while (get_pwm(THROT_ID) < STARTUP_THRESH) {
    ;
  }
  
  play_sound(SOUND_HIGH);
  clear_light(WHITE);
  // currently lit: green
}

void manual_control() {
  reset_outputs();

  clear_all_lights();
  set_light(BLUE);
  set_light(GREEN);
  play_sound(SOUND_HIGH);

  uint8_t timer_counter = 0;
  while (true) {
    output_pins[SERVO_ID].writeMicroseconds(get_pwm(SERVO_ID));
    output_pins[THROT_ID].writeMicroseconds(get_pwm(THROT_ID));

    if (get_pwm(THROT_ID) < SHUTDOWN_THRESH && get_pwm(SERVO_ID) > STEERING_THRESH) {
      timer_counter += 1;
      if (timer_counter > MANUAL_CUTOFF / MANUAL_DELAY) {
        play_sound(SOUND_HIGH);
        break;
      }
    }
    delay(MANUAL_DELAY);
  }
  
  reset_outputs();
}

void reset_outputs() {
  output_pins[SERVO_ID].writeMicroseconds(SERVO_IDLE);
  output_pins[THROT_ID].writeMicroseconds(THROT_IDLE);
}



































