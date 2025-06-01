
int sensorPin = A0;    // select the input pin for the potentiometer
int sensorPin1 = A1; 
int sensorValue = 0;  // variable to store the value coming from the sensor
int sensorValue1 = 0;
long int timenow=0,timestart=0;

 

void setup() {
  Serial.begin(9600);
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
  pinMode(12,OUTPUT);
  digitalWrite(12,LOW);
  delay(30000);
}

 

void loop() {
  
  timenow = millis();
  Serial.print(timenow);
  sensorValue = analogRead(sensorPin);
  Serial.print(",");
  Serial.println(sensorValue); 
}
