#include <FlexCAN.h>
#include <can_adapter.h>
#include <RMS_can_gen.h>
#include <kinetis_flexcan.h>

// Code for FSAE 2019, written by Austin Stevens and Aaron Morgan.

const int brakePin = A16;
const int brakeMin = 3;
const int brakeMax = 400;
const int apps1Pin = A15; // 4-951
const int apps1Min = 315;
const int apps1Max = 855;
const int apps2Pin = A14; // 3-720
const int apps2Min = 253;
const int apps2Max = 726;
const int led = 13;
boolean carOn = false;
long G_CAN_BAUD = 250000;
boolean G_SERIAL_LOG = false;
long loop_start_ms = 0;

// Action delays
const int G_BRK_MSG_DELAY_MS = 125;
int g_brk_msg_timeout = G_BRK_MSG_DELAY_MS;
const int G_TRQ_MSG_DELAY_MS = 125;
int g_trq_msg_timeout = G_TRQ_MSG_DELAY_MS;
const int G_BLNK_MS = 125;
int g_blnk_ms = G_BLNK_MS;

struct CAN_message_t torqueMessage;
struct CAN_message_t rxMsg;
struct CAN_message_t dashMessage;

// Method to clear the values of any given CAN message, depending on its length.
void zeroize_message(CAN_message_t& torqueMessage, int length){
  for(int i = 0; i < length; i++){
    torqueMessage.buf[i] = 0x00;
  }
}

// Returns a value from 0 to 100, based upon the min value and max value.
// Returns no less than 0, and no more than 100.
double percentalize_pot(int adc_read, int min_val, int max_val)
{
  if (adc_read < min_val)
  {
    return 0;
  }
  else if (adc_read > max_val)
  {
    return 100;
  }
  else
  {
    int range = max_val - min_val;
    return 100*(static_cast<double>(adc_read - min_val) / range);
  }
}

// Writes a CAN message to the bus that indicates the position of the brake pedal.
void writeBrakeMsg(int16_t brakeValue)
{
  // Brake message.
  struct CAN_message_t brakeMessage;

  // Writing brake CAN message.
  brakeMessage.id = 0x145; // This is 325 in decimal. This will need to be changed when we can use the Jettson
  brakeMessage.len = 2;
  zeroize_message(brakeMessage, 2);
  brakeMessage.buf[0] = brakeValue;
  brakeMessage.buf[1] = brakeValue >> 8;
  Can0.write(brakeMessage);
}

// Handles sending torque messages to the controller. Shuts down the controller in case of a variety of failures.
// Returns false if the car is turned off after handling the torque command.
bool handleTorqueCmd(double apps1Percent, double apps2Percent, double brakePercent)
{
  int16_t torqueValue = (int16_t) (apps1Percent + apps2Percent) / 2;
  int16_t speed = 0;
  bool direction = true;
  bool enable = true;
  bool discharge = false;
  int16_t torque_limit = 0;

  // If the difference of the two percentages is greater than 5, then tell the controller to turn off. 
  // Also Generate a stop message to the controller if there is more than 25% pedal travel and the 
  // brakes are being used at the same time.
  if(abs(apps1Percent - apps2Percent) > 5 || (torqueValue > 25 && brakePercent > 10))
  {
    torqueMessage.id = 0xC0;
    zeroize_message(torqueMessage, 8);
    Can0.write(torqueMessage);
    return false;
  }
  else
  {
   gen_cmd(&torqueMessage, torqueValue, speed, direction, enable, discharge, torque_limit);
   Can0.write(torqueMessage);
   return true;
  }
}

void setup() {
  if (G_SERIAL_LOG)
  {
    Serial.begin(9600);
  }
  Can0.begin(G_CAN_BAUD);
  pinMode(apps1Pin, INPUT);
  pinMode(apps2Pin, INPUT);
  pinMode(brakePin, INPUT);
  pinMode(led, OUTPUT);
  loop_start_ms = millis();
}

void loop()
{
  long new_ms = millis();
  int delta = loop_start_ms - new_ms;
  loop_start_ms = new_ms;

  // Grab and percentalize the ADC values.
  // Brakes:
  float brakePercent = percentalize_pot(analogRead(brakePin), brakeMin, brakeMax);
  // Accelerator:
  float apps1Percent = percentalize_pot(analogRead(apps1Pin), apps1Min, apps1Max);
  float apps2Percent = percentalize_pot(analogRead(apps2Pin), apps2Min, apps2Max);

  // iterate timers
  g_brk_msg_timeout -= delta;
  g_trq_msg_timeout -= delta;
  g_blnk_ms -= delta;

  // Handle received CAN messages.
  Can0.read(rxMsg);
  // Send the message to the controller to release the lock when the message from the dash is received.
  if(rxMsg.id == 0x145 && carOn == false){ // 326 is 0x146 in Hex.
    torqueMessage.id = 0xC0; // This is 192 in decimal.
    torqueMessage.len = 8;
    zeroize_message(torqueMessage, 8);
    Can0.write(torqueMessage);
    dashMessage.id = 0x15E; // This is sent to the dash to tell it to stop sending the start ID. Note: Does this need to be sent continually for the dash to receive it?
    Can0.write(dashMessage);
    carOn = true;
  }
  // Send the message to the controller to close the lock when the dash signals that the car is turned off.
  else if(rxMsg.id == 0x146 && carOn == true){ // 327 is 0x147 in Hex.
    torqueMessage.id = 0xC0;
    zeroize_message(torqueMessage, 8);
    Can0.write(torqueMessage);
    dashMessage.id = 0x15F; // Same as above, but to tell the dash to stop sending the stop ID.
    Can0.write(dashMessage);
    carOn = false;
  }

  // Handle timer'd actions
  // Blink LED
  if (g_blnk_ms <= 0)
  {
    digitalWrite(led, HIGH);
    g_blnk_ms = G_BLNK_MS;
  }

  // Send Brake Messages
  if (g_brk_msg_timeout <= 0)
  {
    writeBrakeMsg(static_cast<int16_t>(brakePercent));
    g_brk_msg_timeout = G_BRK_MSG_DELAY_MS;
  }

  // Send Torque messages.
  if (g_trq_msg_timeout <= 0)
  {
    if (carOn == true)
    {
      carOn = handleTorqueCmd(apps1Percent, apps2Percent, brakePercent);
    }
    g_trq_msg_timeout = G_TRQ_MSG_DELAY_MS;
  }
}
