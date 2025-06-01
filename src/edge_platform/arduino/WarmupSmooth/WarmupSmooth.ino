

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
  
}

void loop() {
  digitalWrite(13,LOW);
  timestart=millis();
  timenow=millis();
  while(timenow-timestart<5000)
  {
    
    //sensorValue1 = analogRead(sensorPin1);
    timenow = millis();
    Serial.print(timenow);
    Serial.print(",");
    sensorValue = analogRead(sensorPin);
    sensorValue1 = analogRead(sensorPin1);
    Serial.print(sensorValue);
    Serial.print(",");
    Serial.print(sensorValue1);
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
    sensorValue1 = analogRead(sensorPin1);
    Serial.print(sensorValue);
    Serial.print(",");
    Serial.print(sensorValue1);
    Serial.print(",");
    Serial.println("1"); 
  }
  
}
