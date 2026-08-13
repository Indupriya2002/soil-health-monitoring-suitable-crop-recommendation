#include <SoftwareSerial.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define RE_PIN 7
#define DE_PIN 6

SoftwareSerial rs485(3, 4); // RO -> D2, DI -> D3
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Modbus commands
byte nitro[] = {0x01, 0x03, 0x00, 0x1E, 0x00, 0x01, 0xE4, 0x0C};
byte phos[]  = {0x01, 0x03, 0x00, 0x1F, 0x00, 0x01, 0xB5, 0xCC};
byte pota[]  = {0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xC0};

byte values[7];

void setup() {
  Serial.begin(9600);     // Must match FastAPI baud rate
  rs485.begin(9600);

  pinMode(RE_PIN, OUTPUT);
  pinMode(DE_PIN, OUTPUT);

  digitalWrite(RE_PIN, LOW);
  digitalWrite(DE_PIN, LOW);

  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("NPK Sensor");
  lcd.setCursor(0, 1);
  lcd.print("Initializing...");
  delay(2000);

  lcd.clear();
}

void loop() {
  int N = readSensor(nitro);
  delay(300);

  int P = readSensor(phos);
  delay(300);

  int K = readSensor(pota);
  delay(300);

  // ✅ SEND CLEAN FORMAT TO PYTHON BACKEND
  // Format: N,P,K
  Serial.print(N);
  Serial.print(",");
  Serial.print(P);
  Serial.print(",");
  Serial.println(K);

  // LCD Display
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("N:");
  lcd.print(N);
  lcd.print(" P:");
  lcd.print(P);

  lcd.setCursor(0, 1);
  lcd.print("K:");
  lcd.print(K);
  lcd.print(" mg/kg");

  delay(3000);
}

int readSensor(byte *request) {

  // Enable transmission
  digitalWrite(DE_PIN, HIGH);
  digitalWrite(RE_PIN, HIGH);
  delay(10);

  rs485.write(request, 8);
  rs485.flush();

  // Switch to receive mode
  digitalWrite(DE_PIN, LOW);
  digitalWrite(RE_PIN, LOW);

  delay(200);

  int index = 0;
  unsigned long startTime = millis();

  while (millis() - startTime < 1000) {
    if (rs485.available()) {
      values[index++] = rs485.read();
      if (index >= 7) break;
    }
  }

  if (index >= 5) {
    int val = values[3] * 256 + values[4];
    return val;
  }

  return 0; // return 0 if failed
}

