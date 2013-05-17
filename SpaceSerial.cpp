#include "SpaceSerial.h"
#include <EEPROMAnything.h>
#include <stdarg.h>

#if 1
static void DEBUGF(char* fmt, ...) {
        va_list args;
        va_start(args, fmt);

        char buf[1024];
        vsprintf(buf, fmt, args);
        Serial.print(buf);

        va_end(args);
}
#else
static void DEBUGF(char*, ...) {}
#endif

static char recv_buf[sizeof(message_t)];
size_t recv_idx;

int                     nav_mode;
bool                    nav_ready;
size_t                  nav_point_count;
nav_point_t     nav_points[63];

static eeprom_header_t eeprom_header;


void spaceserial_init(void) {
        DEBUGF("spaceserial_init()\n");
        recv_idx = 0;
        nav_ready = false;
        nav_point_count = 0;
        nav_mode = NAV_MODE_COMPASS;

        EEPROM_readAnything(0, eeprom_header);
        if (eeprom_header.magic == EEPROM_MAGIC) {
                nav_point_count = eeprom_header.points_expected;
                nav_ready = (eeprom_header.points_expected == eeprom_header.points_stored);
                nav_mode = eeprom_header.nav_mode;

                int i;
                for (i = 0; i < eeprom_header.points_stored; i++) {
                        EEPROM_readAnything((i+1)*sizeof(nav_point_t), nav_points[i]);
                }
        }
        else {
                eeprom_header.magic = EEPROM_MAGIC;
                eeprom_header.points_expected = 0;
                eeprom_header.points_stored = 0;
                eeprom_header.nav_mode = nav_mode;
                eeprom_header.null = 0;
                EEPROM_writeAnything(0, eeprom_header);
        }
}

void spaceserial_set_mode(char mode) {
        nav_mode = mode;
        eeprom_header.nav_mode = nav_mode;
        EEPROM_writeAnything(0, eeprom_header);
}

static void mnavbegin(message_t* msg) {
        nav_point_count = msg->nav_begin.num_points;
        if (nav_point_count > 63) {
                DEBUGF("Too many navigation points (%d > 63)!\n", nav_point_count);
        }
        nav_ready = false;

        eeprom_header.points_expected = nav_point_count;
        eeprom_header.points_stored = 0;
        EEPROM_writeAnything(0, eeprom_header);
}
static void mnavdata(message_t* msg) {
        uint8_t idx = msg->nav_data.idx;
        if (idx < nav_point_count) {
                nav_points[idx].latitude = msg->nav_data.latitude / 100000.0f;
                nav_points[idx].longitude = msg->nav_data.longitude / 100000.0f;
                EEPROM_writeAnything((idx+1)*sizeof(nav_point_t), nav_points[idx]);

                eeprom_header.points_stored++;
                EEPROM_writeAnything(0, eeprom_header);
        }
        else {
                DEBUGF("Got a point that doesn't exist (%d of %d)\n",idx+1,nav_point_count);
        }
}

void spaceserial_feed(int c) {
        //if (c == -1) return;
        // Feed buffer
        recv_buf[recv_idx++] = c;
        if (recv_idx != sizeof(message_t)) return;

        // Parse and handle message
        message_t* msg = (message_t*)&recv_buf[0];
        int t = msg->msg_type;
        DEBUGF("Got a message! Yay! IT IS OF TYPE %d.\n", t);
        switch(t) {
                // Beginning of a navigation sequence
                case M_NAV_BEGIN:
                        mnavbegin(msg);
                        break;

                // A single point in a navigation sequence
                case M_NAV_DATA:
                        mnavdata(msg);
                        break;

                // End of a navigation sequence
                case M_NAV_END:
                        nav_ready = true;
                        break;

                case M_NAV_MODE:
                        nav_mode = msg->nav_mode.mode;
                        eeprom_header.nav_mode = nav_mode;
                        EEPROM_writeAnything(0, eeprom_header);
                        break;

                default:
                        DEBUGF("Invalid message type: %d\n", msg->msg_type);
                        break;
        }
        recv_idx = 0;
}