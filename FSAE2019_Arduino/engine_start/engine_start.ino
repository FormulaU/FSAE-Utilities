#include <FlexCAN.h>
#include <kinetis_flexcan.h>

// Code for FSAE 2019, written by Austin Stevens and Aaron Morgan.

int buttonPin = 1;     
int lightPin = 2;
int teensyLightPin = 13;       
int buttonState;           
int lastButtonState = LOW; 
boolean carOn = false;
boolean sendingStart = false;
boolean sendingStop = false;

unsigned long debounceDelay = 200; 
unsigned long lastDebounceTime = 0;       

struct CAN_message_t msg;
struct CAN_message_t startMessage;
struct CAN_message_t stopMessage;

void setup()
{
  Can0.begin(250000);
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
  pinMode(lightPin, OUTPUT);
  pinMode(teensyLightPin, OUTPUT);
}

void loop()
{
  digitalWrite(lightPin, HIGH);
  // LED if the car is OFF
  if (!carOn)
  {
    digitalWrite(teensyLightPin, HIGH);
  }
  else
  {
    digitalWrite(teensyLightPin, HIGH);
  }
  
  // read a message
  Can0.read(msg);
    
  // check ID to see if brake message and if brake is pressed more than 50% of the way
  boolean brakePressed = msg.id == 0x145 && msg.buf[0] > 50;

  buttonState = digitalRead(buttonPin);
  int reading = digitalRead(buttonPin);

  if(sendingStart == true){
    Can0.write(startMessage);
  }
  if(sendingStop == true){
    Can0.write(stopMessage);
  }

  if(msg.id == 0x15E){
    sendingStart = false;
  }
  if(msg.id == 0x15F){
    sendingStop = false;
  }

  if(brakePressed && carOn == false && reading == HIGH){  
    
    // turn on the car
    startMessage.id = 0x146;// 0x146 is the agreed upon ID for the start message
    startMessage.len = 8;
    for(int i = 0; i < 8; i++){
      startMessage.buf[i] = 0x00;
    }
    sendingStart = true;    
    carOn = true;
  
    digitalWrite(lightPin, HIGH);
    delay(500); 
    digitalWrite(teensyLightPin, LOW);
  }
  else if(reading == HIGH && carOn == true){

    //turn off car
    stopMessage.id = 0x147; // 0x147 is the agreed upon ID for the stop message
    stopMessage.len = 8;
    for(int i = 0; i < 8; i++){
      stopMessage.buf[i] = 0x00;
    }
    sendingStop = true;
    carOn = false;
    
    digitalWrite(lightPin, LOW);
    delay(3000);
  }

// This commented section is to get the LED from the start button to flash, depending on the battery level.

//  if(carOn == true && msg.id == 0x148 && msg.buf[0] <= 50 && msg.buf[0] > 25){ // Will need to update the ID with something else to match Josh's CAN message for the battery. Doublecheck that he's going to fill buf[0].
//    digitalWrite(lightPin, LOW);
//    delay(1000);
//    digitalWrite(lightPin, HIGH);
//    delay(4000);
//  }
//
//  if(carOn == true && msg.id = 0x149 && msg.buf[0] <= 25){ // Same as above.
//    digitalWrite(lightPin, LOW);
//    delay(500);
//    digitalWrite(lightPin, HIGH);
//    delay(1000);
//  }
 
}
