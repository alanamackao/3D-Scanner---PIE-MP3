// import libraries
#include <Servo.h>

// initialize variables
String inYpos;   // string to store incoming Y position
int yServoInstruct; // int to use for servo instruction
int xServoInstruct; 
Servo yServo;   // creates servo object to control servo
int yServoPos;  // variable to store servo position
Servo xServo;
int xServoPos;  
int IRpin=A0;

void setup() {
  Serial.begin(9600);
  yServo.attach(9);     // servo attatched to pin 9
}

void loop() {

  if (Serial.available() > 0) {
    inYpos = Serial.readStringUntil('\n');
    // Serial.println(inYpos);
    Serial.println(inYpos.indexOf('y'));
      // always gives 0, should sometimes be giving -1
      // doesn't enter if statement even if it's equal to 0

    if (inYpos.indexOf('y') == 0) {
      inYpos.substring(1);
      yServoPos = inYpos.toInt();
      yServo.write(yServoPos);

      Serial.println(yServoPos); // converts yServoPos to a string again
    }
    
    
    int IRreading = analogRead(IRpin);

    // if (incomingByte == "on") {
    //   digitalWrite(LED_BUILTIN, HIGH);
    //   Serial.write("Led on");
    // }

    // else if (incomingByte == "off") {
    //   digitalWrite(LED_BUILTIN, LOW);
    //   Serial.write("Led off");
    // }

    // else{
    //  Serial.write("invald input");
    // }
  }
}