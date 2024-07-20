void setup() {   ​

  // initialize inbuilt LED pin as an output.​

  pinMode(LED_BUILTIN, OUTPUT);​

}​

// loop function runs over and over  again forever​

void loop() {​

  digitalWrite(LED_BUILTIN, HIGH);   // turn the  LED on by making the pin 13 HIGH​

  delay(500);              // wait for a 0.5  second​

  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the  pin 13 LOW​

  delay(500);              // wait for a 0.5 second​

}