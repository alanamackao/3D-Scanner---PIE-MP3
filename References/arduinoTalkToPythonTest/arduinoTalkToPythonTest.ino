// Following code taken from Tabletop Robotics on YouTube: https://youtu.be/Lm_xfm1d5h0?si=q_clN18kiD-mJb9w

String incomingByte ;    

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {

  if (Serial.available() > 0) {
  incomingByte = Serial.readStringUntil('\n');

    if (incomingByte == "on") {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.write("Led on");
    }

    else if (incomingByte == "off") {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.write("Led off");
    }

    else{
     Serial.write("invald input");
    }
  }
}