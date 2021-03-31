// Use if you want to force the software SPI subsystem to be used for some reason (generally, you don't)
// #define FASTLED_FORCE_SOFTWARE_SPI
// Use if you want to force non-accelerated pin access (hint: you really don't, it breaks lots of things)
// #define FASTLED_FORCE_SOFTWARE_SPI
// #define FASTLED_FORCE_SOFTWARE_PINS
#include <FastLED.h>

#define NUM_LEDS 300
#define DATA_PIN 5

uint8_t bins[512] = {0};

CRGB leds[NUM_LEDS];

const uint8_t gamma8[] = {
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 };

// This function sets up the ledsand tells the controller about them
void setup() {
    FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS);
    Serial.begin(115200);
    FastLED.show();
    Serial.setTimeout(100);
}


void loop() {
  Serial.flush();
  Serial.printf("G%c", '\n'); //Request data

  for(int z; z < 100; z++)
  {
    if(Serial.available() > 50) 
    {
      Serial.readBytes(bins, 301);
      if(true) //bins[300] == char(0xff))
      {
        for(int j = 0; j < NUM_LEDS; j++)
        {
          if(bins[j] <= 0)
          {
            //Catch negative / default 0
            leds[j].setRGB(0,0,0);
          }
          else if(bins[j] < 90)
          {
            //Green Channel
            uint8_t nr = gamma8[int(bins[j]) * 255 / 90];
            leds[j].setRGB(0, nr, 0);
          }
          else if(bins[j] < 180)
          {
            //yellow Channel
            uint8_t nr = gamma8[(int(bins[j]) - 90) * 255 / 90];
            leds[j].setRGB(nr , nr, 0);
          }
          else
          {
            //Red Channel
            uint8_t nr = gamma8[(int(bins[j]) - 180) * 255 / 90];
            leds[j].setRGB(nr, 0, 0);
          }    
        }
        FastLED.show();
        z = 999;
      }
    }
  }
}
