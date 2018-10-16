/*
* This project creates a small thermal camera using the MELEXIS MLX90621
*
* Adapted by Josh Long (https://github.com/longjos) Oct 2015
* Based on a https://github.com/robinvanemden/MLX90621_Arduino_Processing
*
* Original work by:
* 2013 by Felix Bonowski
* Based on a forum post by maxbot: http://forum.arduino.cc/index.php/topic,126244.msg949212.html#msg949212
* This code is in the public domain.
*/
#include <SPI.h>
#include <Arduino.h>
#include <Wire.h>
#include "wireMLX90621.h"

MLX90621 sensor; // create an instance of the Sensor class

void setup(){
  Serial.begin(19200);
  sensor.initialise (4);
 }
void loop(){
  sensor.measure(true); //get new readings from the sensor

  for(int y=0;y<4;y++){ //go through all the rows

    for(int x=0;x<16;x++){ //go through all the columns
      int16_t valueAtXY= sensor.irData[y+x*4]; // extract the temperature at position x/y
      Serial.print(sensor.getTemperature(y+x*4));
      Serial.print("  ");
    }
    Serial.println(y);
  }
  Serial.print ("ambient ");
  Serial.println(sensor.getAmbient());
  // Serial.print ("ptat ");
  // Serial.println(sensor.ptat);
  // Serial.print ("cpix ");
  // Serial.println(sensor.cpix);
  //  tft.setCursor(10, 20);
  // Serial.print ("a.common");
  // Serial.println(sensor.a_common);
delay(50);
};
