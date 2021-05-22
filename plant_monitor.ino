// DHT11 humidity and temperature sensor, SE012 photoresistor, FC-28 soil moisture sensor
// 128x64 OLED, 1 channel relay module (5V), 5050 plant grow led strip lights (12V), piezo buzzer


#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <avr/pgmspace.h>

#include "DHT.h"

#include <ezBuzzer.h>

// dht
#define DHT_PIN 2
#define DHT_TYPE DHT11

// oled
#define RESET_BUTTON 2
#define OLED_RESET 4
#define SCREEN_WIDTH 128  // in pixels
#define SCREEN_HEIGHT 64


DHT dht(DHT_PIN, DHT_TYPE);

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


int pin_relay = 13;
const int relay_on = 0;
const int relay_off = 1;

unsigned long last_time = 0;
int sample_count = 0;
int sample_max_quantity = 5;  // how many measurements are required to calculate a mean
int sample_wait = 2000;  // time to wait for the next measurement
// those values allow the data to be measured and sent in 10 seconds intervals

float val_temp_c;  // temperature in Celsius, 0 C - 50 C, +/- 2 C accuracy
float sum_temp_c;

float val_air;  // relative humidity, range 20 % - 80 %
float sum_air;

int pin_photores = A0;  // photoresistor
float val_photores;
float sum_photores;
int limit_photores = 40;  // below this value turn on the led lights

int pin_soil = A1;  // soil moisture sensor
float val_soil; 
float sum_soil;
int limit_soil = 45;  // below this value alert about low moisture with the buzzer

float mean_temp_c;
float mean_air;
float mean_photores;
float mean_soil;


int pin_buzzer = 11;
ezBuzzer buzzer(pin_buzzer);

// frequency of the melody: 494, 392, 587, 440, 494, 698, 659, 880, 1047, 988
int melody[] = {NOTE_B4, NOTE_G4, NOTE_D5, NOTE_A4, NOTE_B4, NOTE_F5, NOTE_E5, NOTE_A5, NOTE_C6, NOTE_B5};
int note_duration[] = {4, 4, 4, 4, 4, 4, 4, 4, 4, 2};  // 2 = half note, 4 = quarter note
int note_length;


// coordinates for oled_display function
// [] = {value_x, value_y, unit_x, unit_y}
int oled_temp_c[] = {22, 15, 54, 15};  
int oled_air[] = {22, 45, 54, 45};
int oled_photores[] = {90, 15, 122, 15};
int oled_soil[] = {90, 45, 122, 45}; 


static const unsigned char PROGMEM temp[] = {0x0f,0x00,0x10,0x80,0x26,0x40,0x29,0x40,0x29,0x40,0x29,0x40,
0x2d,0x40,0x29,0x40,0x29,0x40,0x2d,0x40,0x29,0x40,0x29,0x40,0x2d,0x40,0x29,0x40,0x29,0x40,0x2d,0x40,0x29,
0x40,0x2f,0x40,0x6d,0x60,0x4d,0x20,0x9c,0x90,0xbe,0x50,0xbf,0x50,0x9e,0x90,0x4d,0x20,0x66,0x60,0x30,0xc0,
0x1f,0x80};
// 12 x 28

static const unsigned char PROGMEM air[] = {0x30,0xc3,0x00,0x49,0x24,0x80,0x86,0x18,0x40,0x30,0xc3,0x00,
0x49,0x24,0x80,0x86,0x18,0x40,0x30,0xc3,0x00,0x49,0x24,0x80,0x86,0x18,0x40,0x30,0xc3,0x00,0x49,0x24,0x80,
0x86,0x18,0x40,0x30,0xc3,0x00,0x49,0x24,0x80,0x86,0x18,0x40,0x30,0xc3,0x00,0x49,0x24,0x80,0x86,0x18,0x40,
0x30,0xc3,0x00,0x49,0x24,0x80,0x86,0x18,0x40};
//18x21

static const unsigned char PROGMEM sun[] = {0x00,0x20,0x00,0x00,0x20,0x00,0x00,0x20,0x00,0x30,0x20,0x60,
0x18,0x00,0xc0,0x0c,0x01,0x80,0x00,0xf8,0x00,0x01,0x04,0x00,0x02,0x72,0x00,0x02,0xfa,0x00,0xf5,0xfd,0x78,
0x05,0xfd,0x00,0x02,0xfa,0x00,0x02,0x72,0x00,0x01,0x04,0x00,0x00,0xf8,0x00,0x0c,0x01,0x80,0x18,0x00,0xc0,
0x30,0x20,0x60,0x00,0x20,0x00,0x00,0x20,0x00,0x00,0x20,0x00};
// 21x22

static const unsigned char PROGMEM moon[] = {0x01,0xf0,0x00,0x07,0xe0,0x00,0x0e,0xc0,0x00,0x19,0x80,0x00,
0x33,0x00,0x00,0x37,0x00,0x00,0x66,0x00,0x00,0x66,0x00,0x00,0xc6,0x00,0x00,0xc6,0x00,0x00,0xc3,0x00,0x00,
0xc3,0x00,0x00,0x61,0x80,0x00,0x61,0x80,0x00,0x70,0xc0,0x00,0x30,0x70,0x00,0x18,0x1f,0xe0,0x0c,0x01,0xc0,
0x07,0x03,0x80,0x03,0xff,0x00,0x00,0xfc,0x00};
// 19x21

static const unsigned char PROGMEM water[] = {0x02,0x00,0x02,0x00,0x02,0x00,0x07,0x00,0x07,0x00,0x0f,0x80,
0x1f,0xc0,0x3f,0xe0,0x3f,0xe0,0x7f,0xf0,0x7f,0xf0,0x7f,0xf0,0xff,0x98,0xff,0x08,0xfe,0x08,0xfe,0x08,0x7c,
0x10,0x7c,0x10,0x3e,0x20,0x1f,0xc0,0x07,0x00};
// 13x21


bool dht11_error(float val_sensor1, float val_sensor2) {
  if (isnan(val_sensor1) or isnan(val_sensor2)) {
    Serial.println(F("Connection error DHT11"));

    display.clearDisplay();
    display.drawRoundRect(10, 10, 118, 54, 10, WHITE);
    
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(22, 25);
    display.print(F("Connection error"));
    display.setCursor(53, 40);
    display.print(F("DHT11"));
    display.display();
    return true;
    }
  else {
    return false;
  }
}


void oled_display(float val_sensor, int arr[]) {
  display.setCursor(arr[0], arr[1]);
  display.print(val_sensor);
  display.setCursor(arr[2], arr[3]);

  if (val_sensor == mean_temp_c) {
    display.print(String("C"));
  }
  else {
    display.print(String("%"));
  }
}


void buzzer_alert() {
  buzzer.loop();

  if (buzzer.getState() == BUZZER_IDLE) {
    buzzer.playMelody(melody, note_duration, note_length);
  }
}


void setup() {
  digitalWrite(pin_relay, relay_off);  // initialise the relay to off
  pinMode(pin_relay, OUTPUT);   

  pinMode(RESET_BUTTON, INPUT_PULLUP);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);

  dht.begin();
  
  note_length = sizeof(note_duration) / sizeof(int);
  
  Serial.begin(9600);
}


void loop() {
  unsigned long current_time = millis();

  // MEASUREMENTS
  val_temp_c = dht.readTemperature();
  val_air = dht.readHumidity();

  if (dht11_error(val_temp_c, val_air) == true) {
    return;
  }
  
  val_photores = map(analogRead(pin_photores), 0, 1023, 100, 0); 
  val_soil = map(analogRead(pin_soil), 0, 1023, 100, 0);

  // CALCULATING THE MEAN VALUES
  if (current_time - last_time > sample_wait) {
    last_time = current_time;
    sample_count += 1;
    
    sum_temp_c += val_temp_c;
    sum_air += val_air;
    sum_photores += val_photores;
    sum_soil += val_soil;
    
    if (sample_count == sample_max_quantity) {
      mean_temp_c = sum_temp_c / sample_count;
      mean_air = sum_air / sample_count;
      mean_photores = sum_photores / sample_count;
      mean_soil = sum_soil / sample_count;

    // SERIAL -> PYTHON
      if (mean_temp_c == 0 or mean_air == 0 or mean_photores == 0 or mean_soil == 0) {
        return;
      }
      else {
        Serial.print(mean_temp_c);
        Serial.print(F(" "));
        Serial.print(mean_air);
        Serial.print(F(" "));
        Serial.print(mean_photores);
        Serial.print(F(" "));
        Serial.print(mean_soil);
      
        sample_count = sum_temp_c = sum_air = sum_photores = sum_soil = 0;    
      }

        // OLED
        display.clearDisplay();

        display.drawBitmap(3, 5, temp, 12, 28, 1);
        display.drawBitmap(0, 40, air, 18, 21, 1);
        display.drawBitmap(69, 39, water, 13, 21, 1);
  
        if (mean_photores < limit_photores) {
          display.drawBitmap(67, 7, moon, 19, 21, 1); 
        }
        else {
          display.drawBitmap(65, 7, sun, 21, 22, 1);
        }

        display.setTextSize(1);
        display.setTextColor(WHITE);

        oled_display(mean_temp_c, oled_temp_c);
        oled_display(mean_air, oled_air);
        oled_display(mean_photores, oled_photores);
        oled_display(mean_soil, oled_soil);

        display.display();
    }
  }
   
 // LIGHT ON/OFF
 if (mean_photores < limit_photores) {  // too dark, turn on the lights
    digitalWrite(pin_relay, relay_on);
  }
  else {
    digitalWrite(pin_relay, relay_off);
  }
        
  // BUZZER ON/OFF
  if (mean_soil < limit_soil) {  // too dry, start the alert
    buzzer_alert();
  }
  
}
