
int sensorPin = A0;    // select the input pin for the potentiometer
int sensorPin1 = A1; 
int sensorValue = 0;  // variable to store the value coming from the sensor
int sensorValue1 = 0;
long int timenow=0;
 

void setup() {
  Serial.begin(9600);
  //Serial.print("Hello");
  //delay(30000);
  
}

 

void loop() {
  
  timenow = millis();
  Serial.print(timenow);
  Serial.print(",");
  sensorValue = analogRead(sensorPin);  
  sensorValue1 = analogRead(sensorPin1);
  Serial.print(sensorValue); 
  Serial.print(",");
  Serial.println(sensorValue1); 
}
