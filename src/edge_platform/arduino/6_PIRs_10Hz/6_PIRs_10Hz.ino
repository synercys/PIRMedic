
/*
//Class I -- Lens Cap Dislodged (Dislocated/Cap Fallen)
int Cout_normal = A0;     
int Aout_normal = A1; 

//Class II -- Lens Cap Deformed (Puncture/Shape Deformation)
int Cout_window_covered = A2;     
int Aout_window_covered = A3; 

//Class III -- Lens Cap Covered (Paper/Tape)
int Cout_lens_covered = A4;     
int Aout_lens_covered = A5; 

//Class IV -- Window Damage (Oil)
int Cout_lens_covered = A6;     
int Aout_lens_covered = A7; 

//Class V -- Electronic Fault
int Cout_lens_covered = A8;     
int Aout_lens_covered = A9; 

//Normal PIR
int Cout_lens_covered = A10;     
int Aout_lens_covered = A11; 
*/

#define NUM_PIR_PINS 12
int pir_pins[NUM_PIR_PINS]={A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11};
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
