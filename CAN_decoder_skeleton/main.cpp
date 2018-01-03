// One way to compile this file is to run 'gcc main.cpp -o output' in the same directory as main.cpp.
// This should create an executable called 'output'. What the executable does doesn't really matter, as long as it compiles without errors.
// It may also compile using the Arduino IDE, but I'm not sure. I didn't test that.

// Some typedefs for length specific ints
#include <stdint.h>

// Define the CAN_message_t struct. Done by the FlexCAN library, so this would typically be done in the FlexCAN.h header
typedef struct CAN_message_t {
  uint32_t id; // can identifier
  uint8_t ext; // identifier is extended
  uint8_t len; // length of data
  uint16_t timeout; // milliseconds, zero will disable waiting
  uint8_t buf[8];
} CAN_message_t;

// Some general purpose error states. Not complete, but serve as a decent example.
enum ERROR {E_NO_ERR, E_NOT_FOUND, E_INVALID_ARG};

// Forward declaration: Lets the compiler know that, at some point, there is going to be
// a function named decode_message that takes a CAN_message_t message and returns an ERROR enum.
ERROR decode_message(CAN_message_t msg);

// Another, stating that there's going to be a function called build_torque that takes a torque value in the form of an int,
// a reference to a CAN_message_t struct, and returns an ERROR enum.
// The '&' after CAN_message_t here means that the variable is 'passed by reference'. Functionally, this means that,
// rather than copying the CAN_message_t struct and having the function use that copy, any modifications to
// msg inside the function will also change msg outside of the function. 
ERROR build_torque_msg(uint16_t torque, CAN_message_t& msg);

// Main method. Basically just so that this compiles.
// Runs when the program is executed, with arguments argc (number of commandline arguments)
// and argv (character arrays containing the arguments).
//
// Ex: If this file was compiled to an executable named 'foo', and then executed in the command
// line with the following command:
//    foo arg1 arg2
// argc would equal 3, and argv would be an array of character arrays with contents 'foo', 'arg1' and 'arg2'
int main(int argc, char *argv[])
{
  // Create some random CAN_message_t. Doesn't matter what's in it, since this is just to give an example of how the functions
  // are called.
  CAN_message_t msg_in;
  ERROR res;
  // We would grab the error result after calling the decode message.
  res = decode_message(msg_in);
  // If the result isn't E_NO_ERR (or something like that), something's gone wrong.
  if (res != ERROR::E_NO_ERR)
    {
      // In the actual code, we would do something.
    }

  //Create a CAN message to propagate.
  CAN_message_t msg_out;
  //Build a CAN_message_t with a torque value of 160. 
  res = build_torque_msg(160, msg_out);
  if (res != ERROR::E_NO_ERR)
    {
      // If we have an error, then things didn't work right.
    }
  else
    {
      // Otherwise, msg_out would have been set up with the proper data for the torque CAN command, and
      // could be sent with something like FlexCAN's write(CAN_message_t msg) method.

      //Commented out, since we don't actually have that library included.
      //write(msg_out);
    }
  
}

// The actual implementation of the decode_message function
ERROR decode_message(CAN_message_t msg)
{
  // FILL IN: Read some messages, according to the RMS CAN Protocol document.
  return ERROR::E_NO_ERR;
}

ERROR build_torque_msg(uint16_t torque, CAN_message_t& msg)
{
  // FILL IN: Set the parameters of msg according to the RMS CAN Protocol document, and the passed torque.
  return ERROR::E_NO_ERR;
}

