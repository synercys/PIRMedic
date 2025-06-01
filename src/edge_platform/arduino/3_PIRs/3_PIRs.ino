
/*
//Normal PIR
int Aout_normal = A0;     
int Cout_normal = A1; 

//Window Covered PIR
int Aout_window_covered = A2;     
int Cout_window_covered = A3; 

//Lens Covered PIR
int Aout_lens_covered = A4;     
int Cout_lens_covered = A5; 
*/

#define NUM_PIR_PINS 6
int pir_pins[NUM_PIR_PINS]={A0, A1, A2, A3, A4, A5};
short int i;


void setup() {
  Serial.begin(9600);
  delay(30000);
}

void loop() {
  Serial.print(millis());
  Serial.print(",");
  for (i=0; i< NUM_PIR_PINS-1; i=i+2){
    Serial.print(analogRead(i)); 
    Serial.print(",");
    Serial.print(analogRead(i+1));
    Serial.print(",");  
  }
  Serial.println();
}
