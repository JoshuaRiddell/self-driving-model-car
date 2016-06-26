#include <Servo.h>

// pwm values
//          min   mid   max
// servo:   1032  1364  1700
// throt:   1020  1556  2056



// buzzer parameters
#define BUZZER_PIN 8
#define BUZZ_DURATION 40000
#define SOUND_HIGH 100
#define SOUND_MIDDLE 110
#define SOUND_LOW 115

// sonar pins
#define SONAR_ECHO 0
#define SONAR_TRIG 7

// reciever pins
#define SERVO_RX 2
#define THROT_RX 3

// output pins
#define SERVO_TX 10
#define THROT_TX 11

// idle values for outputs
#define SERVO_IDLE 1364
#define THROT_IDLE 1556

// specific thresholds
#define SHUTDOWN_THRESH 1100  // less than this for shutdown
#define STARTUP_THRESH 1930  // larger than this for startup
#define ARM_CUTOFF 3000 // ms to wait until arm

// array values for servo and throttle
#define SERVO_ID 0
#define THROT_ID 1
#define NUM_CHANNELS 2

// define pin arrays
static const uint8_t input_pins[] = { SERVO_RX, THROT_RX };
Servo output_pins[NUM_CHANNELS];

// define pwm data caches
volatile unsigned long prev_time[NUM_CHANNELS];
volatile uint16_t pwm_val[NUM_CHANNELS];

void wait_for_arm(void);
void wait_for_start(void);
void play_sound(uint16_t frequency);
void emergency_shutdown(void);

void setup() {
  // start serial
  Serial.begin(115200);

  // sonar pin modes
  pinMode(SONAR_TRIG, OUTPUT);

  // reciever pin modes
  pinMode(SERVO_RX, INPUT);
  pinMode(THROT_RX, INPUT);

  // output pin modes
  output_pins[SERVO_ID].attach(SERVO_TX);
  output_pins[THROT_ID].attach(THROT_TX);
  
  output_pins[SERVO_ID].write(SERVO_IDLE);
  output_pins[THROT_ID].write(THROT_IDLE);

  // attach unique pin interrupts
  attachInterrupt(digitalPinToInterrupt(SERVO_RX), handle_servo_intr, CHANGE);
  attachInterrupt(digitalPinToInterrupt(THROT_RX), handle_throt_intr, CHANGE);
  
  // set piezo output
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  wait_for_arm();
  wait_for_start();

  while (1) {
    if (pwm_val[THROT_ID] < SHUTDOWN_THRESH) {
      emergency_shutdown();
    }
    
    
  }
}

void wait_for_arm() {  
  uint8_t timer_counter = 0;
  while (true) {
    Serial.println(pwm_val[THROT_ID]);
    if (pwm_val[THROT_ID] > STARTUP_THRESH) {
      timer_counter += 1;
      if (timer_counter == 1) {
        play_sound(SOUND_LOW);
      } else if (timer_counter > ARM_CUTOFF / 50) {
        break;
      }
    } else {
      timer_counter = 0;
    }
    delay(50);
  }
  
  play_sound(SOUND_HIGH);
  delay(50);
  play_sound(SOUND_HIGH);
  
  while (pwm_val[THROT_ID] > STARTUP_THRESH) {
    ;
  }
  
  play_sound(SOUND_LOW);
  delay(500);
}

void wait_for_start() {
  while (pwm_val[THROT_ID] < STARTUP_THRESH) {
    ;
  }
  play_sound(SOUND_HIGH);
}

void emergency_shutdown() {
  while (true) {
    output_pins[SERVO_ID].write(SERVO_IDLE);
    output_pins[THROT_ID].write(THROT_IDLE);
    play_sound(SOUND_LOW);
  }
}

void handle_servo_intr() {
  // pass through current pin value
  handle_interrupt(SERVO_ID, digitalRead(SERVO_RX));
}

void handle_throt_intr() {
  // pass through current pin value
  handle_interrupt(THROT_ID, digitalRead(THROT_RX));
}

void handle_interrupt(uint8_t pin_id, bool change) {
  // handle the pwm counters
  if (change) {
    prev_time[pin_id] = micros();
  } else {
    pwm_val[pin_id] = micros() - prev_time[pin_id];
  }
}

void play_sound(uint16_t frequency) {
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
}



























