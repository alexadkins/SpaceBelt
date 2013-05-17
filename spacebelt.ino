#include <TinyGPS.h>
#include <SoftwareSerial.h>
#include <Keypad.h>
#include <Wire.h>
#include <stdlib.h>
#include <EEPROM.h>
#include <EEPROMAnything.h>
#include <SpaceSerial.h>
// Baud rate for communication with Python
#define TERMBAUD 9600
// GPS baud rate
#define GPSBAUD 57600
#define GPS_RX 3
#define GPS_TX 4
#define GPS_EXPIRATION (60*10*1000)
#define HMC6352_SLAVE (0x42 >> 1)
#define HMC6352_READ 0x41
struct State {
        float latitude;
        float longitude;
        float heading;
        unsigned long gps_timestamp;
        boolean gps_fix;
        int current_motor;
        int current_nav_point;
} g_State;
TinyGPS g_GPS;
SoftwareSerial g_GPSSerial(GPS_RX, GPS_TX);
const static int g_MotorCount         = 8;
const static int g_MotorPins[]         = {6, 7, 8, 9, 10, 11, 12, 13};
void setup();
void loop();
void update_gps();
void update_compass();
void set_motor(int motor_num);
int anglemath(float long1, float lat1, float long2, float lat2);
void setup()
{
        Serial.begin(TERMBAUD);
        g_GPSSerial.begin(GPSBAUD);
        // Initialize spaceserial
        spaceserial_init();
        // Initialize all motor pins
        int i;
        for (i = 0; i < g_MotorCount; i++)
        {
                pinMode(g_MotorPins[i], OUTPUT);
                digitalWrite(g_MotorPins[i], LOW);
        }
        // Set default state values
        g_State.latitude = 0.0f;
        g_State.longitude = 0.0f;
        g_State.gps_timestamp = 0;
        g_State.gps_fix = false;
        g_State.current_motor = -1;
        g_State.current_nav_point = 0;
}
void loop()
{
        if (Serial.available())
        {
                spaceserial_feed(Serial.read());
        }
        update_compass();
        update_gps();
        switch(nav_mode)
        {
        case NAV_MODE_COMPASS:
                set_motor(round((0 - g_State.heading) * g_MotorCount / 360.0f));
                break;
        case NAV_MODE_TARGET:
                if (!nav_ready)
                {
                        set_motor(-1);
                        break;
                }
                int target_heading = anglemath(g_State.longitude, g_State.latitude,
                        nav_points[0].longitude, nav_points[0].latitude);
                set_motor(round((target_heading - g_State.heading) * g_MotorCount / 360.0f));
                break;
        case NAV_MODE_DIRECTIONS:
                if (!nav_ready || current_nav_point == nav_point_count)
                {
                        set_motor(-1);
                        break;
                }
                // Point towards the current navigation point.
                float lat1 = g_State.latitude, long1 = g_State.longitude;
                float lat2 = nav_points[current_nav_point].latitude, long2 = nav_points[current_nav_point].longitude;
                int target_heading = anglemath(long1, lat1, long2, lat2);
                set_motor(round((target_heading - g_State.heading) * g_MotorCount / 360.0f));
                // If we're close enough, switch to the next point.
                if (pow(lat2-lat1,2)+pow(long2-long1,2) < 0.0001f)
                {
                        current_nav_point++;
                }
                break;
        }
}
// set_motor(int motor_num)
//        Set which motor is currently vibrating.
void set_motor(int motor_num)
{
        if (motor_num >= 0)
        {
                motor_num = motor_num % g_MotorCount;
        }
        if (motor_num == g_State.current_motor) return;
        if (g_State.current_motor >= 0)
                digitalWrite(g_MotorPins[g_State.current_motor], LOW);
        if (motor_num >= 0)
                digitalWrite(g_MotorPins[motor_num], HIGH);
        g_State.current_motor = motor_num;
}
// update_gps()
//         Read any available data from the GPS chip, and if it's there, grab
//         the latest latitude/longitude pair.
void update_gps()
{
        while (g_GPSSerial.available())
        {
                // TinyGPS.encode() returns 'true' if a new sentence has been parsed.
                if (g_GPS.encode(g_GPSSerial.read()))
                {
                        g_GPS.f_get_position(&(g_State.latitude), &(g_State.longitude));
                        g_State.gps_timestamp = millis();
                        g_State.gps_fix = true;
                }
        }
        // Check for gps data expiration.
        if (g_State.gps_fix &&
                millis() - g_State.gps_timestamp >= GPS_EXPIRATION)
        {
                g_State.gps_fix = false;
        }
}
// update_compass()
//        Read the current heading from the compass chip.
void update_compass()
{
        Wire.beginTransmission(HMC6352_SLAVE);
        Wire.write(HMC6352_READ);              // The "Get Data" command
        Wire.endTransmission();
        //time delays required by HMC6352 upon receipt of the command
        //Get Data. Compensate and Calculate New Heading : 6ms
        delay(6);
        Wire.requestFrom(HMC6352_SLAVE, 2); //get the two data bytes, MSB and LSB
        //"The heading output data will be the value in tenths of degrees
        //from zero to 3599 and provided in binary format over the two bytes."
        byte MSB = Wire.read();
        byte LSB = Wire.read();
        float headingSum = (MSB << 8) + LSB; //(MSB / LSB sum)
        g_State.heading = headingSum / 10;
}
int anglemath(float long1, float lat1, float long2, float lat2)
{
    //lat1 & long1 refer to current location
        //lat2 & long2 refer to destination
        int height = abs(lat1 - lat2);
        int width = abs(long1 - long2);
 
        //Angle in radians
        int radangle = atan(width/height);
        //Angle in degrees
        int degangle = radangle*M_PI/180;
        //Finding the quadrant
        if (lat1 > lat2){
                y = 0;
        }
        else{
                y = 1;
        }
        if (long1 > long2){
                x = 0;
        }
        else{
                x = 1;
        }
        //Adjusting angle for proper quadrant
        if (y == 0){
                if (x == 0){
                        angle = degangle + 180;
                }
                else if (x == 1){
                        angle = degangle + 90;
                }
        }
        else if (y == 1){
                if (x == 0){
                        angle = degangle + 270;
                }
                else if (x == 1){
                        angle = degangle;
                }
        }
    return angle;  
}