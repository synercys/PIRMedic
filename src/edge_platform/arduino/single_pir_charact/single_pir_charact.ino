/*
 * Murata PIR EVM
 * Cout --> A0;     
 * Aout --> A1; 
*/
char val1[255];//, val2[255], val3[255], val4[255], val5[255], val6[255];
void setup() {
  Serial.begin(9600);
  delay(30000); //30 secs is the warm-up time from experiments
}

void loop() {
  sprintf(val1, "%lu,%d,%d,", millis(), analogRead(A0), analogRead(A1));
  //  sprintf(val2, "%d,%d,", analogRead(A2), analogRead(A3));
  //  sprintf(val3, "%d,%d,", analogRead(A4), analogRead(A5));
  //  sprintf(val4, "%d,%d,", analogRead(A6), analogRead(A7));
  //  sprintf(val5, "%d,%d,", analogRead(A8), analogRead(A9));
  //  sprintf(val6, "%d,%d,", analogRead(A10), analogRead(A11));
  //  Serial.print(val1);
  //  Serial.print(val2);
  //  Serial.print(val3);
  //  Serial.print(val4);
  //  Serial.print(val5);
  Serial.println(val1);
  delay(20);
}
