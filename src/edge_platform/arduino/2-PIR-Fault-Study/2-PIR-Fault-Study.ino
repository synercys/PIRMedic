/*
 * Working
 * Cout --> A0;     
 * Aout --> A1; 
 * 
 * Faulty
 * Cout --> A2;     
 * Aout --> A3; 
*/
char val1[255];
void setup() {
  Serial.begin(9600);
  delay(30000); //30 secs is the warm-up time from experiments
}

void loop() {
  sprintf(val1, "%lu,%d,%d,%d,%d", millis(), analogRead(A0), analogRead(A1), analogRead(A2), analogRead(A3));
  Serial.println(val1);
  delay(20);
}
