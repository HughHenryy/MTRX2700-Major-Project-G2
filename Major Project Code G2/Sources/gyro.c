#include "gyro.h"



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