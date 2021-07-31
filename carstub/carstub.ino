#include <Arduino.h>

const byte highbeam = 12;
const byte lowbeam = 13;
const byte frontfog = 14;
const byte leftsignal = 27;
const byte rightsignal = 26;
const byte parklight = 25;

void setup()
{
  Serial.begin(115200);

  pinMode(highbeam, OUTPUT);
  pinMode(lowbeam, OUTPUT);
  pinMode(frontfog, OUTPUT);

  pinMode(leftsignal, OUTPUT);
  pinMode(rightsignal, OUTPUT);

  pinMode(parklight, OUTPUT);
}

void loop()
{
  if (Serial.available() >= 3)
  {
    char *buf = new char[4];
    buf[3] = '\0';
    Serial.readBytes(buf, 3);
    String command = String(buf);
    if (command == "hbh") // set high beam high
    {
      digitalWrite(highbeam, HIGH);
    }
    else if (command == "hbl")
    {
      digitalWrite(highbeam, LOW);
    }
    else if (command == "lbh")
    {
      digitalWrite(lowbeam, HIGH); // green
    }
    else if (command == "lbl") // low beam
    {
      digitalWrite(lowbeam, LOW);
    }
    else if (command == "ffh") // front fog
    {
      digitalWrite(frontfog, HIGH); // blue
    }
    else if (command == "ffl")
    {
      digitalWrite(frontfog, LOW);
    }
    else if (command == "lsh") // left signal
    {
      digitalWrite(leftsignal, HIGH);
    }
    else if (command == "lsl")
    {
      digitalWrite(leftsignal, LOW);
    }
    else if (command == "rsh") // right signal
    {
      digitalWrite(rightsignal, HIGH);
    }
    else if (command == "rsl")
    {
      digitalWrite(rightsignal, LOW);
    }
    else if (command == "plh") // parking light
    {
      digitalWrite(parklight, HIGH);
    }
    else if (command == "pll")
    {
      digitalWrite(parklight, LOW);
    }
  }
}