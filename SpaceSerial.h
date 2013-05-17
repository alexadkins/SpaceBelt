#ifndef _SPACE_SERIAL_H_
#define _SPACE_SERIAL_H_

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#define M_NAV_BEGIN     0
#define M_NAV_DATA              1
#define M_NAV_END               2
#define M_NAV_MODE              3

#define PACK __attribute__((__packed__))

#ifndef bool
#define bool int
#define true 1
#define false 0
#endif

typedef struct {
        uint8_t msg_type;
        union {
                struct {
                        uint8_t idx;
                        int32_t latitude, longitude;
                } PACK nav_data;
                struct {
                        uint8_t num_points;
                        uint8_t null[8];
                } PACK nav_begin;
                struct {
                        uint8_t mode;
                        uint8_t null[8];
                } PACK nav_mode;
        };
} PACK message_t;

#define NAV_MODE_COMPASS '1'
#define NAV_MODE_TARGET '2'
#define NAV_MODE_DIRECTIONS '3'


extern void spaceserial_init(void);
extern void spaceserial_feed(int c);
extern void spaceserial_set_mode(char mode);


typedef struct {
        float latitude, longitude;
} PACK nav_point_t;

extern bool                     nav_ready;
extern size_t           nav_point_count;
extern int                      nav_mode;
extern nav_point_t      nav_points[63];

#define EEPROM_MAGIC 0x3A9F
typedef struct {
        uint16_t magic;
        uint8_t points_expected;
        uint8_t points_stored;
        uint8_t nav_mode;

        uint32_t null : 24; // Padding
} PACK eeprom_header_t;

#endif//_SPACE_SERIAL_H_