// import libraries
#include <Servo.h>

// initialize variables

Servo tiltServo;   // creates servo object to control servo
int tiltServoPos;  // variable to store servo position
Servo panServo;
int panServoPos;  
int IRpin=A0;

String received;  // string to store incoming info from python

void setup() {
  Serial.begin(115200);
  tiltServo.attach(9);     // servo attatched to pin 9
  panServo.attach(8);
}

void loop() {

  if (Serial.available() > 0) {
    received = Serial.readString();
    //Serial.println(received);

    int commaIndex = received.indexOf(',');     // takes index of comma in received message
    tiltServoPos = received.substring(0, commaIndex).toInt();   
        // creates a new string from the beginning of the message to the comma
    panServoPos = received.substring(commaIndex + 1).toInt();
        // creates a new string from the comma to the end of the message

    tiltServo.write(tiltServoPos);
        // moves the tilt servo
    panServo.write(panServoPos);
        // moves the pan servo
    int IRreading = analogRead(IRpin);
        // takes the analog input from the IR sensor and returns it as a voltage

    // prints '{tiltServoPos},{panServoPos},{IRreading}\n' to serial buffer for python to read
    Serial.print(tiltServoPos);
    Serial.print(',');
    Serial.print(panServoPos);
    Serial.print(',');
    Serial.println(IRreading);
  }

}