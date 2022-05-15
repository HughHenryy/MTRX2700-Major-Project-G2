#include <hidef.h>      /* common defines and macros */
#include "derivative.h"      /* derivative-specific definitions */

#include <stdio.h>
#include <stdlib.h>

#include "simple_serial.h"


struct MSG_HEADER{
  int sentinel;
  char msg_type[8];
  unsigned int msg_size;
  unsigned int header_time;
  int end_sentinel;
};

struct MSG_DATA{
  int sentinel;
  int angle;
  int lidar;
  int none;
  unsigned int last_sample_time;
};



void Send_MIX_DATA_Msg(int angle_in, int lidar_in, int nonein) {
  struct MSG_HEADER data_header = {0xABCD, "DATA", 0, 0, 0xDCBA};
  struct MSG_DATA data_message = {0x9876, 0, 0, 0, 0};
                             
  data_header.msg_size = sizeof(struct MSG_DATA);
  data_header.header_time = TCNT;
  
  data_message.last_sample_time = TCNT;
  data_message.angle = angle_in;
  data_message.lidar = lidar_in;
  data_message.none = nonein;
  
  SerialOutputBytes((char*)&data_header, sizeof(struct MSG_HEADER), &SCI1);  
  SerialOutputBytes((char*)&data_message, sizeof(struct MSG_DATA), &SCI1);  
}









void main(void) {
  /* put your own code here */

  int lidar_data = 50;    //distance from sensor 
  int angle = 38;//angle degree from sensor
  int None = 0;//Nothing

  _DISABLE_COP();

  
  // initialise the serial
  SerialInitialise(BAUD_9600, &SCI1);
  
  // initialise the timer
  TSCR1_TEN = 1;  
  TSCR2_PR = 0b111;
  
  //sprintf(text_buffer, "first 12345");
  //SendTextMsg(text_buffer);
  //SendTextMsg(text_buffer);
  //SendTextMsg(text_buffer);
  
  //sprintf(text_buffer, "second 123456");
  //SendTextMsg(text_buffer);
  //SendTextMsg(text_buffer);
  //SendTextMsg(text_buffer);
  
	EnableInterrupts;

  //SendButtonsMsg();
  //SendButtonsMsg();
  //SendButtonsMsg();
  
  _DISABLE_COP();

  for(;;) {

      Send_MIX_DATA_Msg(lidar_data,angle, None);
    //_FEED_COP(); /* feeds the dog */
  } /* loop forever */
  /* please make sure that you never leave main */
}
