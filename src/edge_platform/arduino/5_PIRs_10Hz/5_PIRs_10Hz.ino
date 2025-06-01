
/*
//Normal PIR
int Cout_normal = A0;     
int Aout_normal = A1; 

//Window Covered PIR
int Cout_window_covered = A2;     
int Aout_window_covered = A3; 

//Lens Covered PIR
int Cout_lens_covered = A4;     
int Aout_lens_covered = A5; 

//Cap off PIR
int Cout_lens_covered = A6;     
int Aout_lens_covered = A7; 

//Window broken PIR
int Cout_lens_covered = A8;     
int Aout_lens_covered = A9; 
*/

#define NUM_PIR_PINS 10
int pir_pins[NUM_PIR_PINS]={A0, A1, A2, A3, A4, A5, A6, A7, A8, A9};
short int i;
char ts[100];
char val[100];

void setup() {
  Serial.begin(9600);
  delay(30000);
}

void loop() {
  sprintf(ts, "\n%lu,",millis());
  Serial.print(ts);
  for (i=0; i< NUM_PIR_PINS-1; i=i+2){
    sprintf(val,"%d,%d,", analogRead(i), analogRead(i+1));  
    Serial.print(val);
  }
}
