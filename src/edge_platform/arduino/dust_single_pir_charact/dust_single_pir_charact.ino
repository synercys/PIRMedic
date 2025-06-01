/*
 * Murata PIR EVM
 * Cout --> A0;     
 * Aout --> A1; 
*/
char val[255];
void setup() {
  Serial.begin(9600);
  delay(30000); //30 secs is the warm-up time from experiments
}

void loop() {
  // Serial.println(analogRead(A0));
  sprintf(val, "%lu,%d,%d,", millis(), analogRead(A6), analogRead(A7));
  Serial.println(val);
  delay(20);
}
