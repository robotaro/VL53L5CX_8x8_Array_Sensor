#include <Wire.h>
#include <SparkFun_VL53L5CX_Library.h>

SparkFun_VL53L5CX myImager;
VL53L5CX_ResultsData measurementData;

int imageResolution = 0;
int imageWidth = 0;

void setup()
{
  Serial.begin(115200);
  delay(1000);

  Wire.begin();
  Wire.setClock(400000);

  if (myImager.begin() == false)
  {
    while (1);
  }

  myImager.setResolution(8 * 8);
  myImager.setRangingFrequency(15);  // Max refresh rate at 8x8 is 15Hz

  imageResolution = myImager.getResolution();
  imageWidth = sqrt(imageResolution);

  myImager.startRanging();
}

void loop()
{
  if (myImager.isDataReady() == true)
  {
    if (myImager.getRangingData(&measurementData))
    {
      // Start identifier
      Serial.print("[");

      for (int y = 0; y <= imageWidth * (imageWidth - 1); y += imageWidth)
      {
        for (int x = imageWidth - 1; x >= 0; x--)
        {
          Serial.print(measurementData.distance_mm[x + y]);
          if (!(x == 0 && y == imageWidth * (imageWidth - 1))) {
            Serial.print(","); // Separate values with a comma
          }
        }
      }

      // Stop identifier
      Serial.println("]");
    }
  }

  delay(5);
}
