#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>

/* Assign a unique ID to these sensors */
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(54321);
Adafruit_LSM303_Mag_Unified mag = Adafruit_LSM303_Mag_Unified(12345);

double accelX, accelY, accelZ; //Stores accelerometer readings
double xAngle, yAngle, zAngle; //Stores calculated angles

void setup(void) 
{
  Serial.begin(9600);
  accel.begin();  //Starts communications with the accelerometer
}

void loop(void) 
{
  /* Get a new sensor event */ 
  sensors_event_t accelEvent; 
  accel.getEvent(&accelEvent);

  /* Sets the acceleration values to the acceleration values */
  accelX = accelEvent.acceleration.x;
  accelY = accelEvent.acceleration.y;
  accelZ= accelEvent.acceleration.z;

  /* Converts these values to angles */
  xAngle = atan2(accelX,(sqrt(accelY*accelY+accelZ*accelZ)))*180/3.14;
  yAngle = atan2(accelY,(sqrt(accelX*accelX+accelZ*accelZ)))*180/3.14;
  zAngle = atan2(accelZ,(sqrt(accelX*accelX+accelY*accelY)))*180/3.14;

  /* These are then printed to the serial */
  Serial.print(xAngle);
  Serial.print(" ");    //Spaces here are what python uses to cut the data.
  Serial.print(yAngle);
  Serial.print(" ");
  Serial.println(zAngle);

  delay(100);
  
}
