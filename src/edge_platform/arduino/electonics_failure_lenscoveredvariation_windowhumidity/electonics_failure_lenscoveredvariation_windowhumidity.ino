
/*
//Electronics Failure
int Aout_normal = A0;     
int Cout_normal = A1; 

//Lens Covered (Tape, Partial)
int Aout_window_covered = A2;     
int Cout_window_covered = A3; 

//Window Covered (Humidity - Oil + Water)
int Aout_window_covered = A4;     
int Cout_window_covered = A5; 

*/

#define NUM_PIR_PINS 2
int pir_pins[NUM_PIR_PINS]={A0, A1};
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
  delay(40);
}
