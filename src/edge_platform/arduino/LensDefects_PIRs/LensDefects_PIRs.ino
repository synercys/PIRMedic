
/*
//Normal PIR
int Cout_normal = A0;     
int Aout_normal = A1; 

//Plastic Covered PIR
int Cout_window_covered = A2;     
int Aout_window_covered = A3; 

//Paper Covered PIR
int Cout_lens_covered = A4;     
int Aout_lens_covered = A5; 

//Dust covered PIR
int Cout_lens_covered = A6;     
int Aout_lens_covered = A7; 

*/

//#define NUM_PIR_PINS 10
//int pir_pins[NUM_PIR_PINS]={A0, A1, A2, A3, A4, A5, A6, A7};
//short int i;
char val[255];

void setup() {
  Serial.begin(9600);
  delay(30000);
}

void loop() {
  sprintf(val, "%lu,%d,%d,%d,%d,%d,%d,%d,%d,\n", millis(), 
  analogRead(A0), analogRead(A1), 
  analogRead(A2), analogRead(A3), 
  analogRead(A4), analogRead(A5),
  analogRead(A6), analogRead(A7));
  Serial.print(val);
}
