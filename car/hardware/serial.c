#include <stdio.h>
#include <stdint.h>

#include "serial.h"

#include <avr/io.h>
#include <avr/interrupt.h>

#define SERIAL_BUFFER_SIZE 255

typedef struct {
    char data[SERIAL_BUFFER_SIZE];
    uint8_t in;
    uint8_t out;
} serial_buffer_t;

static volatile serial_buffer_t in_buff;
static volatile serial_buffer_t out_buff;

static int serial_put_char(char c, FILE* stream);

static inline void buffer_init(volatile serial_buffer_t *buff);
static inline uint8_t buffer_push(volatile serial_buffer_t *buff, char data);
static inline char buffer_pop(volatile serial_buffer_t *buff);
static inline void buffer_clear(volatile serial_buffer_t *buff);
static inline uint8_t buffer_bytes_left(volatile serial_buffer_t *buff);
static inline uint8_t buffer_full(volatile serial_buffer_t *buff);

static FILE serial_stream = FDEV_SETUP_STREAM(serial_put_char, serial_get_char,
                                             _FDEV_SETUP_RW);

void serial_init(long baud) {
    uint16_t ubrr;

    // init input and output buffers
    buffer_init(&in_buff);
    buffer_init(&out_buff);

    // write setup registers
    ubrr = ((F_CPU / (8 * baud)) + 1)/2 - 1;
    UBRR0 = ubrr;

    // enable rx and tx on the line, and intterupts
    UCSR0B = (1<<RXEN0)|(1<<TXEN0);
    UCSR0B |= (1 <<RXCIE0);

    // attach stream to stdio streams
    stdout = &serial_stream;
    stdin = &serial_stream;

    sei();
}

bool serial_available(void) {
    return buffer_bytes_left(&in_buff) > 0;
}

void serial_clear_input(void) {
    buffer_clear(&in_buff);
}


static int serial_put_char(char c, FILE* stream) {
    if (c == '\n') {
        serial_put_char('\r', NULL);
    }

    // wait for buffer to empty
    while (buffer_full(&out_buff));

    cli();
    buffer_push(&out_buff, c);
    UCSR0B |= _BV(UDRIE0);
    sei();

    return 0;
}

int serial_get_char(FILE* stream) {
    if (buffer_bytes_left(&in_buff) == 0) {
        // nothing available
        return 1;
    }

    char c;
    cli();
    c = buffer_pop(&in_buff);
    sei();
    return c;
}

static inline void buffer_init(volatile serial_buffer_t *buff) {
    buff->in = 0;
    buff->out = 0;
}

static inline uint8_t buffer_push(volatile serial_buffer_t *buff, char data) {
    // put data on the stack
    buff->data[buff->in++] = data;
    
    // check for wraparound
    if (buff->in >= SERIAL_BUFFER_SIZE) {
        buff->in = 0;
    }

    return 0;
}

static inline char buffer_pop(volatile serial_buffer_t *buff) {
    char data = buff->data[buff->out++];

    // check for wraparound
    if (buff->out >= SERIAL_BUFFER_SIZE) {
        buff->out = 0;
    }

    return data;
}

static inline void buffer_clear(volatile serial_buffer_t *buff) {
    buff->out = buff->in;
}

static inline uint8_t buffer_bytes_left(volatile serial_buffer_t *buff) {
    if (buff->out > buff->in) {
        return (UINT8_MAX - buff->out) + buff->in;
    } else {
        return buff->in - buff->out;
    }
}

static inline uint8_t buffer_full(volatile serial_buffer_t *buff) {
    // check if we have reached the end of the buffer
    return buff->in != buff->out;
}

ISR(USART_UDRE_vect) 
{
    if (buffer_bytes_left(&out_buff)) {
        UDR0 = buffer_pop(&out_buff);
    } else {
        UCSR0B &= ~_BV(UDRIE0);
    }
}

ISR(USART_RX_vect) 
{
    if (!buffer_full(&in_buff)) {
        buffer_push(&in_buff, UDR0);
        serial_put_char(UDR0, NULL);
    }
}