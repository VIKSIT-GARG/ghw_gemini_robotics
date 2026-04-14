String inputString = "";         
bool stringComplete = false;  

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN , OUTPUT);
  inputString.reserve(200);
  Serial.println("Arduino Ready");
}

void loop() {
  if (stringComplete) {
    inputString.trim();

    // Hardware Logic
    if (inputString == "BEE_DETECTED") {
      digitalWrite(LED_BUILTIN , HIGH);
      Serial.println("Action: Bzz! Target found! 🐝");
    } else if (inputString == "IDLE") {
      digitalWrite(LED_BUILTIN , LOW);
      Serial.println("Action: Nothing cool detected.");
    }

    inputString = "";
    stringComplete = false;
  }
}


// This function runs automatically in the background when data arrives
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
