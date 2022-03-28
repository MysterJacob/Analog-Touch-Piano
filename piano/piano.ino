/*
 Copyright (c) 2015 NicoHood
 See the readme for credit to other people.

 AnalogTouch example
 Lights an Led if pin is touched and prints values to the Serial
*/

// AnalogTouch
#include <AnalogTouch.h>

// Choose your analog and led pin
const int pins[6] = {A0,A1,A2,A3,A4,A5};
#define pinLed LED_BUILTIN
static bool touched[6] = {0};
static uint16_t ref[6] = {0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF};
// Slow down the automatic calibration cooldown
#define offset 1
#if offset > 6
#error "Too big offset value"
#endif

void setup()
{
  // Led setup
  pinMode(pinLed, OUTPUT);
  pinMode(3, OUTPUT);
  // Start Serial for debugging
  Serial.begin(9600);
  tone(3,420,1000);
}
bool GetFromPin(int pin){
      uint16_t value = analogTouchRead(pins[pin]);
      //value = analogTouchRead(pinAnalog, 100);
    
      // Self calibrate
      if (value < ( ref[pin]  >> offset))
        ref[pin] = (value << offset);
      // Cool down
      else if (value > (ref[pin] >> offset))
        ref[pin]++;
    
      // Print touched?
      bool touched = (value - (ref[pin] >> offset)) > 40;
      return touched;
}
void loop()
{
  for(int i =0;i<6;i++){
      touched[i]= GetFromPin(i);
      if(i == 0){
        digitalWrite(pinLed,touched ? HIGH : LOW);
      }
  }
  unsigned int sent = 0;
  for(int i = 0;i<6;i++){
    sent = (sent << 1) | touched[i];
  }
  Serial.println(sent);
  delay(50);
}
