#include <Adafruit_ATParser.h>
#include <Adafruit_BLE.h>
#include <Adafruit_BLEBattery.h>
#include <Adafruit_BLEEddystone.h>
#include <Adafruit_BLEGatt.h>
#include <Adafruit_BLEMIDI.h>
#include <Adafruit_BluefruitLE_SPI.h>
#include <Adafruit_BluefruitLE_UART.h>

// first make "pairing" with HC-06 devise
// view devises list by running 'ls /dev/tty.* in terminal, you can see /dev/tty.HC-06-DevB on the list
// then go to arduino editor, and choose your devise bluetooth under the 'Tools > Serial port' menu
// Now open the serial monitor (Tools > Serial monitor). 
// You should notice that the red led of the bluetooth module has stopped blinking. That means we are connected!
// Now when you send a “1” the led on the pin 13 should turn ON, and if you send a “0” it should turn off. 

void setup() {
  // initialize serial:
  Serial.begin(9600);
  // initialize the led pin
  pinMode(13, OUTPUT);
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    switch(inChar) {
      case '1':
        digitalWrite(13, HIGH);
        Serial.print("pin 13 was turn on");
      break;
      case '0':
        digitalWrite(13, LOW);
        Serial.print("pin 13 was turn off");
      break;
    }
  }
}
