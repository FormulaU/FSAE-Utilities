#include <FlexCAN.h>
#include <can_adapter.h>
#include <RMS_can_gen.h>
#include <kinetis_flexcan.h>

const int potPin = A15;
const int potPin2 = A14;
const int brakePotPin = A16;
const int led = 13;
boolean carOn = false;

struct CAN_message_t torqueMessage;
struct CAN_message_t brakeMessage;
struct CAN_message_t rxMsg;
struct CAN_message_t dashMessage;
struct CAN_message_t testMessage;

// Method to clear the values of any given CAN message, depending on its length.
void zeroize_message(CAN_message_t& torqueMessage, int length){
  for(int i = 0; i < length; i++){
    torqueMessage.buf[i] = 0x00;
  }
}

void setup() {
  Can0.begin(250000);
  pinMode(potPin, INPUT);
  pinMode(potPin2, INPUT);
  pinMode(brakePotPin, INPUT);
  //pinMode(testPin, INPUT);
  pinMode(led, OUTPUT);
  Serial.begin(9600);
}

void loop() {

  //Brakes:

  int brakeRead = analogRead(brakePotPin); // Fully depressed is 415.
  int minValue = 1023; // Read from brake at starting position
  int percent = (brakeRead - minValue)/-6.08; // -6.08 is used for conversion to 0-100 percentage (415-1023/100-0);
  int16_t brakeValue = (int16_t) percent;
  
  digitalWrite(led, HIGH);

  // Writing brake CAN message.
  brakeMessage.id = 0x145; // This is 325 in decimal. This will need to be changed when we can use the Jettson
  brakeMessage.len = 2;
  zeroize_message(brakeMessage, 2);
  brakeMessage.buf[0] = brakeValue;
  brakeMessage.buf[1] = brakeValue >> 8;
  Can0.write(brakeMessage); 

  int16_t torqueValue = (int16_t) 0;
  int16_t speed = 0;
  bool direction = true;
  bool enable = true;
  bool discharge = false;
  int16_t torque_limit = 0;

  gen_cmd(&torqueMessage, torqueValue, speed, direction, enable, discharge, torque_limit);
  Can0.write(torqueMessage);
  
  Can0.read(rxMsg);
  delay(500);

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
    // Send the message to the controller to close the lock when the car is turned off.
    if(rxMsg.id == 327 && carOn == true){ // 0x147 in Hex.
      torqueMessage.id = 0xC0;
      zeroize_message(torqueMessage, 8);
      Can0.write(torqueMessage);
      dashMessage.id = 0x15F; // Same as above, but to tell the dash to stop sending the stop ID.
      Can0.write(dashMessage);
      carOn = false;
    }
    
    if(carOn == true){
      //Pedal: One potentiometer reads from 3-967 (long, single wires), the second reads from 4-865 (shorter wires with connector).
  
      int potValueA0 = analogRead(potPin);
      int potValueA1 = analogRead(potPin2);
      int percentA0 = (potValueA0 - 3)/9.64; // Analog read of A0 converted into a percentage of 0-100.
      int percentA1 = (potValueA1 - 4)/8.61; // Analog read of A1 converted into a percentage of 0-100.
      
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
            
      if(percentA1 >= 1){ //The potentiometer with the smaller range of reads has a deadzone for 20% of pedal travel, which needs to be accounted for.
        int fixedA1 = (potValueA1 + 172); // Offsets the range by 20%
        int scaledA1 = (fixedA1 + 41.25)*0.896631823; // Scales the read from that potentiometer to match the other potentiometer.
    
        int newPercentA1 = scaledA1/9.64; // This converts the new value to a percentage of 0-100.
        
        if(abs(percentA0 - newPercentA1) > 5){ // If the difference of the two percentages is greater than 5, then tell the controller to turn off.
          torqueMessage.id = 0xC0;
          zeroize_message(torqueMessage, 8);
          Can0.write(torqueMessage);
          carOn = false;
        }
        else{ // Otherwise take the average of both percentages and use that as the CAN message.
          torqueValue = (int16_t) (percentA0 + percentA1)/2;
          gen_cmd(&torqueMessage, torqueValue, speed, direction, enable, discharge, torque_limit);
          Can0.write(torqueMessage);
        }
        
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
