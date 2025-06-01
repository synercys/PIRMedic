#include "arduinoFFT.h"
arduinoFFT FFT = arduinoFFT();
#define frequency1  66 //Define Sampling Frequency 1
#define frequency2  5000 // If you want to sample at two frequencies, Define Sampling Frequency 2
//int type = 0x0A;
int type = 0x03;
//uint8_t voltage[128]={128,134,140,146,152,158,165,170,176,182,188,193,198,203,208,213,218,222,226,230,234,237,240,243,245,248,250,251,253,254,254,255,255,255,254,254,253,251,250,248,245,243,240,237,234,230,226,222,218,213,208,203,198,193,188,182,176,170,165,158,152,146,140,134,128,121,115,109,103,97,90,85,79,73,67,62,57,52,47,42,37,33,29,25,21,18,15,12,10,7,5,4,2,1,1,0,0,0,1,1,2,4,5,7,10,12,15,18,21,25,29,33,37,42,47,52,57,62,67,73,79,85,90,97,103,109,115,121}; //Voltage Data
uint16_t voltage[256];
uint16_t fft[128]; // FFT Data
int i;
void voltagemes()
{
  int samplingFrequency =1; 
  int currcount = 0;
  if(type==0x0A)
    samplingFrequency =frequency1; 
  if(type==0x03)
    samplingFrequency =frequency2;
  unsigned int sampling_period_us = round(1000000*(1.0/samplingFrequency));
  currcount=0;
  long long int microseconds = micros();
  float volt = 0;
  while(currcount<256)
  {
    volt = analogRead(0); // connect to Aout is connected to A0, Cout is connected to A1
//    voltage[currcount] = uint8_t(((((volt*5)/1023)/50)/1)*1000) ;//1ohm is the value of the shunt resistor, 50 is the gain of the opamp
    //voltage[currcount] = uint8_t((volt*5)/1023);
    voltage[currcount] = volt;
    currcount++;
    while(micros() - microseconds < sampling_period_us){
          //empty loop
        }
     microseconds += sampling_period_us; 
  }      
}
void takefft()
{
//  volatile double vReal[128]={0};
//  volatile double vImag[128]={0};
   double vReal[256]={0};
   double vImag[256]={0};
  for(int i=0;i<256;i++)
    {
      vReal[i] = voltage[i];
      vImag[i] = 0;
    }
  FFT.Windowing(vReal, 256, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(vReal, vImag, 256, FFT_FORWARD);
  FFT.ComplexToMagnitude(vReal, vImag, 256);
  for(int i =0; i<128;i++)
  {
     fft[i] = round(vReal[i]);
//    fftval2 = round(vReal[i]);
//    if(i>1)
//    {
//      voltage[i-2] = round(fftval2/4);
//      bonsaidata[(62*seq)+i-2] = round(fftval2/4)*64;
//    }
  }
}
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  type = 0x0A;
  voltagemes();
  takefft();
//  for(i=0; i<64; i++){
//    Serial.print(fft[i]);
//    Serial.print(",");
//  }
    for(i=0; i<256; i++){
    Serial.println(voltage[i]);
    }
}

void loop() {

  type = 0x0A;
  voltagemes();
  takefft();
    for(i=0; i<256; i++){
    Serial.println(voltage[i]);
  }





  
  // put your main code here, to run repeatedly:
//  type = 0x0A;
//  voltagemes();
//  takefft();
//  for(i=0; i<64; i++){
//    Serial.print(fft[i]);
//    Serial.print(",");
//    Serial.print(",");
//    Serial.print(voltage[2*i]);
//    Serial.print(",");
//    Serial.println(voltage[2*i+1]);
// }
}
