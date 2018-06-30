#ifndef ENCODER_
#define ENCODER_

typedef struct {
    uint16_t x;
    uint16_t y;
    uint16_t theta;
} pos_t;

void encoder_init(void);
void encoder_reset_pos(void);
void encoder_update(void);
void encoder_get_pos(pos_t *pos);

#endif  // ENCODER_
