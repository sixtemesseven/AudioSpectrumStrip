#include <FastLED.h>

#define NUM_LEDS 300
#define DATA_PIN 5

CRGB leds[NUM_LEDS];

void setup() {
   FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS);
   Serial.setTimeout(100);
   leds[1].setRGB(255, 0, 0);
   FastLED.show();
   delay(1000);
   leds[1].setRGB(0, 255, 0);
   FastLED.show();
   delay(1000);
   leds[1].setRGB(0, 0, 255);
   FastLED.show();
   delay(1000);
}

void loop() {
}
