
int toggle1=1;
ISR(TIMER1_COMPA_vect){
  if (toggle1){
    digitalWrite(13,HIGH);
    toggle1 = 0;
  }
  else{
    digitalWrite(13,LOW);
    toggle1 = 1;
  }
}
int sensorPin = A0;    // select the input pin for the potentiometer
int sensorPin1 = A1; 
int sensorValue = 0;  // variable to store the value coming from the sensor
int sensorValue1 = 0;
long int timenow=0,timestart=0;

void setup() {
  Serial.begin(9600);
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
  //digitalWrite(13,HIGH);
  pinMode(12,OUTPUT);
  digitalWrite(12,LOW);
  //digitalWrite(12,HIGH);
  //delay(30000);
  cli(); // stop interrupts
  TCCR1A = 0; // set entire TCCR1A register to 0
  TCCR1B = 0; // same for TCCR1B
  TCNT1  = 0; // initialize counter value to 0
  // set compare match register for 0.25 Hz increments
  OCR1A = 62499; // = 16000000 / (1024 * 0.25) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS12, CS11 and CS10 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (0 << CS11) | (1 << CS10);
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);
  sei(); // allow interrupts
  
  
}

void loop() {
 /* digitalWrite(13,LOW);
  timestart=millis();
  timenow=millis();
  while(timenow-timestart<5000)
  {
    
    //sensorValue1 = analogRead(sensorPin1);
    timenow = millis();
    Serial.print(timenow);
    Serial.print(",");
    sensorValue = analogRead(sensorPin);
    Serial.print(sensorValue);
    Serial.print(",");
    Serial.println(0); 
  }
  timestart=millis();
  timenow=millis();
  digitalWrite(13,HIGH);
  while(timenow-timestart<30000)
  {
    
    //sensorValue1 = analogRead(sensorPin1);
    timenow = millis();
    Serial.print(timenow);
    Serial.print(",");
    sensorValue = analogRead(sensorPin);
    Serial.print(sensorValue);
    Serial.print(",");
    Serial.println("1"); 
  }
  */
 
  timenow = millis();
  Serial.print(timenow);
  Serial.print(",");
  sensorValue = analogRead(sensorPin);
  sensorValue1 = analogRead(sensorPin1);
  Serial.print(sensorValue);
  Serial.print(",");
  Serial.print(sensorValue1);
  Serial.print(",");
  Serial.println(digitalRead(13));
  //delay(500);

  
}
