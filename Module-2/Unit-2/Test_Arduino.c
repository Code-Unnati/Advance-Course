void setup() {​

  // Start the serial communication with a baud rate of 9600​

  Serial.begin(9600);​


  // Give some time for the Serial Monitor to start​

  delay(1000);​

  // Print a message to the Serial Monitor​

  Serial.println("Arduino is connected and working properly.");​

}​

void loop() {​

  // Print a message every second​

  Serial.println("Arduino is still connected.");​

  delay(1000);​

}​