#include <FlexCAN.h>
#include <can_adapter.h>
#include <RMS_can_gen.h>
#include <kinetis_flexcan.h>

// Code for FSAE 2019, written by Austin Stevens and Aaron Morgan.

const int brakePotPin = A16;
const int potPin = A15; // 4-951
const int potPin2 = A14; // 3-720
const int led = 13;
boolean carOn = false;
int G_CAN_BAUD = 250000;
boolean G_SERIAL_LOG = false;

int percentA15;
int percentA14;

struct CAN_message_t torqueMessage;
struct CAN_message_t brakeMessage;
struct CAN_message_t rxMsg;
struct CAN_message_t dashMessage;

// Method to clear the values of any given CAN message, depending on its length.
void zeroize_message(CAN_message_t& torqueMessage, int length){
  for(int i = 0; i < length; i++){
    torqueMessage.buf[i] = 0x00;
  }
}

void setup() {
  if (G_SERIAL_LOG)
  {
    Serial.begin(9600);
  }
  Can0.begin(G_CAN_BAUD);
  pinMode(potPin, INPUT);
  pinMode(potPin2, INPUT);
  pinMode(brakePotPin, INPUT);
  pinMode(led, OUTPUT);
}

void loop() {

  //Brakes:

  int brakeRead = analogRead(brakePotPin); // Fully depressed is 400
  int minValue = 3; // Read from brake at starting position
  int percent = (brakeRead - minValue)/3.97; // 3.97 is used for conversion to 0-100 percentage (400-3/100-0);
  int16_t brakeValue = (int16_t) percent;
  
  digitalWrite(led, HIGH);

  // Writing brake CAN message.
  brakeMessage.id = 0x145; // This is 325 in decimal. This will need to be changed when we can use the Jettson
  brakeMessage.len = 2;
  zeroize_message(brakeMessage, 2);
  brakeMessage.buf[0] = brakeValue;
  brakeMessage.buf[1] = brakeValue >> 8;
  Can0.write(brakeMessage); 
  
  Can0.read(rxMsg);
  delay(125);

  // Send the message to the controller to release the lock when the message from the dash is received.
  if(rxMsg.id == 326 && carOn == false){ // 326 is 0x146 in Hex.
    torqueMessage.id = 0xC0; // This is 192 in decimal.
    torqueMessage.len = 8;
    zeroize_message(torqueMessage, 8);
    Can0.write(torqueMessage);
    dashMessage.id = 0x15E; // This is sent to the dash to tell it to stop sending the start ID. Note: Does this need to be sent continually for the dash to receive it?
    Can0.write(dashMessage);
    carOn = true;
  }
  // Send the message to the controller to close the lock when the dash signals that the car is turned off.
  if(rxMsg.id == 327 && carOn == true){ // 0x147 in Hex.
    torqueMessage.id = 0xC0;
    zeroize_message(torqueMessage, 8);
    Can0.write(torqueMessage);
    dashMessage.id = 0x15F; // Same as above, but to tell the dash to stop sending the stop ID.
    Can0.write(dashMessage);
    carOn = false;
  }

  if(carOn == true){
    //Pedal:
    int potValueA15 = analogRead(potPin);
    int potValueA14 = analogRead(potPin2);

    int16_t torqueValue = (int16_t) 0;
    int16_t speed = 0;
    bool direction = true;
    bool enable = true;
    bool discharge = false;
    int16_t torque_limit = 0;
    
    gen_cmd(&torqueMessage, torqueValue, speed, direction, enable, discharge, torque_limit);
    Can0.write(torqueMessage);
      
    digitalWrite(led, HIGH);
    delay(125);

    //The potentiometer with the smaller range of reads has a deadzone for a certain amount of pedal travel, which needs to be accounted for.      
    if(potValueA15 >= 315){ 
      // THE FOLLOWING IS THE CODE AUSTIN WROTE AS A QUICK FIX
      potValueA14 = potValueA14 + 250;
      percentA15 = 100*(((double)potValueA15-5)/850);
      percentA14 = 100*(((double)potValueA14-3)/723);
         
      if(abs(percentA15 - percentA14) > 5){ // If the difference of the two percentages is greater than 5, then tell the controller to turn off.
        torqueMessage.id = 0xC0;
        zeroize_message(torqueMessage, 8);
        Can0.write(torqueMessage);
        carOn = false;
      }  
      else{
       torqueValue = (int16_t) (percentA15 + percentA14)/2;
       gen_cmd(&torqueMessage, torqueValue, speed, direction, enable, discharge, torque_limit);
       Can0.write(torqueMessage);
      }
        
//        else{ // This else statement does not make sense, so I'm not sure why it's here. Why assign percentA14 if it's not used?
//          percentA15 = 100*((double)(potValueA15-5)/850);
//          percentA14 = percentA15;
//          torqueValue = (int16_t) (percentA15);   
//        }
        
      if(torqueValue > 25 && brakeValue > 0){ // Generate a stop message to the controller if there is more than 25% pedal travel and the brakes are being used at the same time.
          torqueMessage.id = 0xC0;
          zeroize_message(torqueMessage, 8);
          Can0.write(torqueMessage);
          carOn = false;
      }
    }  
  digitalWrite(led, LOW);
  delay(125);
  }
}
