#include <NewPing.h>
#include <Servo.h>

#include "config.h"
#include "ranging.h"
#include "state_lights.h"
#include "receiver.h"

// TODO
// add proper tones
// add status LEDs
// arg checking on serial input

// debug switch
#define DEBUG  // enables debug messages
#define SERIAL  // enables serial communications (in deployment this will be enabled)
// #define SONAR  // enables sonar ranging
// #define PIEZO_OFF  // turns the piezo off for quiet debugging mode

// define pin arrays
Servo output_pins[NUM_CHANNELS];

// define incoming bytes buffer
byte incomingBuffer[BUFFER_SIZE];

void wait_for_arm(void);
void wait_for_start(void);
void play_sound(uint16_t frequency);
void reset_outputs(void);
void manual_control(void);

void setup() {
  setup_lights();

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
  
  // set piezo output
  pinMode(BUZZER_PIN, OUTPUT);
  
  setup_receiver();
}

void loop() {
  wait_for_arm();
  
  while (true) {
    wait_for_start();

#ifdef SONAR
    unsigned long last_sonar = 0;  // the time that the sonar was last read
#endif

    while (true) {
      if (get_pwm(THROT_ID) < SHUTDOWN_THRESH) {
        manual_control();
        break;
      }

#ifdef SONAR
      if (millis() - last_sonar > SONAR_DELAY) {
        last_sonar = millis();
        
      }
#endif

      if (Serial.available()) {
        Serial.readBytes(incomingBuffer, BUFFER_SIZE);
        output_pins[incomingBuffer[0]].write(incomingBuffer[1]);
      }
    }
  }
}

void wait_for_arm() {  
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
  delay(100);
}

void wait_for_start() {
  while (get_pwm(THROT_ID) < STARTUP_THRESH) {
    ;
  }
  play_sound(SOUND_HIGH);
  clear_light(WHITE);
}

void manual_control() {
  reset_outputs();
  while (get_pwm(THROT_ID) > STARTUP_THRESH || get_pwm(SERVO_ID) > STEERING_THRESH) {
    ;
  }
  delay(500);
  play_sound(SOUND_HIGH);
  uint8_t timer_counter = 0;
  while (true) {
    output_pins[SERVO_ID].writeMicroseconds(get_pwm(SERVO_ID));
    output_pins[THROT_ID].writeMicroseconds(get_pwm(THROT_ID));
    
    if (get_pwm(SERVO_ID) > STEERING_THRESH) {
      timer_counter += 1;
      if (timer_counter > MANUAL_CUTOFF / MANUAL_DELAY) {
        play_sound(SOUND_HIGH);
        break;
      }
    } else {
      timer_counter = 0;
    }
    delay(MANUAL_DELAY);
  }
  reset_outputs();
}

void play_sound(uint16_t frequency) {
#ifndef PIEZO_OFF
  for (uint16_t i = 0; i < BUZZ_DURATION/frequency; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delayMicroseconds(frequency);
    digitalWrite(BUZZER_PIN, LOW);
    delayMicroseconds(frequency);
    digitalWrite(BUZZER_PIN, HIGH);
    delayMicroseconds(frequency);
    digitalWrite(BUZZER_PIN, LOW);
    delayMicroseconds(frequency);
  }
#endif
}

void reset_outputs() {
  output_pins[SERVO_ID].writeMicroseconds(SERVO_IDLE);
  output_pins[THROT_ID].writeMicroseconds(THROT_IDLE);
}



































