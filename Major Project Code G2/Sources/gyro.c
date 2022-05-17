#include "gyro.h"
#include "servo.h"
#include "derivative.h"
#include "simple_serial.h"
#include <string.h>

#define NUM_BIAS_MEASUREMENTS 50
#define TIME_STEP 2.73089 // ms

// stores the current lidar orientation and information on the gyro bias
typedef struct GyroData {
    // current orientation of the lidar in (x, y, z)
  float position[3];

    // bias of each gyro axis, stored in the order (x, y, z)
	float bias[3];
} GyroData;

// allocate memory to store gyroscope information 
GyroData gyroData = {0, 0, 0, 0, 0, 0};

// returns the current orientation of the lidar head 
void get_orientation(float *arr) {
    int i; 
    
    for (i = 0; i < 3; i++) {
        arr[i] = gyroData.position[i];
    }
    
}


void Init_TC5 (void) {
  TSCR1_TEN = 1;
  
  TSCR2 = 0x00;   // prescaler 1, before 32 = 0x04
  TIOS_IOS5 = 1;   // set channel 5 to output compare

  TCTL1_OL5 = 1;    // Output mode for ch5
  TIE_C5I = 1;   // enable interrupt for channel 5
} 



// sets the initial lidar head position to (0, 0, 0) and measures the bias
// in each of the gyro's axes 
void initialise_gyro(void) {
    char buffer[100];
    GyroRaw gyroRawData;
    int i;

	// set servo motors to zero position 
    setServoPose(0, 0);

    // // initialise GyroData struct and set initial position to zero
    // gyroData.position[0] = 0;
    // gyroData.position[1] = 0;
    // gyroData.position[2] = 0;

	// // sum gyroscope measurements to calculate bias 
    // gyroData.bias[0] = 0;
    // gyroData.bias[1] = 0; 
    // gyroData.bias[2] = 0;

    for (i = 0; i < NUM_BIAS_MEASUREMENTS; i++) {
        getRawDataGyro(&gyroRawData);
        
        gyroData.bias[0] += gyroRawData.x;
        gyroData.bias[1] += gyroRawData.y;
        gyroData.bias[2] += gyroRawData.z; 
    }
    
    // average gyro measurements to get bias 
    gyroData.bias[0] /= NUM_BIAS_MEASUREMENTS;
    gyroData.bias[1] /= NUM_BIAS_MEASUREMENTS;
    gyroData.bias[2] /= NUM_BIAS_MEASUREMENTS;

    Init_TC5();

    sprintf(buffer, "Bias: %f %f %f\r\n", gyroData.bias[0], gyroData.bias[1], gyroData.bias[2]);
    SerialOutputString(buffer, &SCI1);

    return;
}



#pragma CODE_SEG __NEAR_SEG NON_BANKED 
__interrupt void TC5_ISR(void) { 
    GyroRaw gyroRawData;
    char str[100];

    // get current gyro angular velocity readings
    getRawDataGyro(&gyroRawData);

    //sprintf(str, "%d %d %d\r\n", gyroRawData.x, gyroRawData.y, gyroRawData.z);
    //SerialOutputString(str, &SCI1);

    // integrate readings to get current gyro position 
    gyroData.position[0] += ((float)gyroRawData.x - gyroData.bias[0]) * TIME_STEP;
    gyroData.position[1] += ((float)gyroRawData.y - gyroData.bias[1]) * TIME_STEP;
    gyroData.position[2] += ((float)gyroRawData.z - gyroData.bias[2]) * TIME_STEP;
    
    //gyroData.position[0] += ((float)gyroRawData.x) * TIME_STEP;
    //gyroData.position[1] += ((float)gyroRawData.y) * TIME_STEP;
    //gyroData.position[2] += ((float)gyroRawData.z) * TIME_STEP;
}                                                








/*
/////////////////// sample code I found online for gyroscope integration ///////////////////
while(1)                                                                                  //
{                                                                                         //
    startInt = mymillis();// this function returns the current time in ms                 //
                                                                                          //
    gyroRaw = readGyro();                                                                 //
                                                                                          //
    //Convert Gyro raw to degrees per second                                              //
    rate_gyro = (float) gyrRaw * GYRO_GAIN;

    //Calculate the angles from the gyro
    gyroAangle += rate_gyro * DT;

    //print the gyro angle ...or anything you find useful

    //Each loop should be at least 20ms.
    while(mymillis() - startInt < 20)
    {
       usleep(100);
    }
}
/////////////////// sample code I found online for gyroscope integration ///////////////////
*/