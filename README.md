# PIRSensorReliability
Repository containing code for reliability in PIR sensors in submission to SIGMETRICS 2021.

dataset/ contains the data collected.
- FaultDetection/faulty_vs_working.csv : contains a mix of Aout from working and faulty sensors
- FaultDetectionFeatures/ : contains the extracted FFT, FFT-based features used to perform the classification between working and faulty sensors
- FineGrainedFaultAnalysis/ : contains Aout from different Class III faulty sensors (some of which are covered with paper, some with tape and some with dust)
- FineGrainedFaultAnalysisFeatures/ : contains the extracted FFT and FFT-based features used to perform the diagnosis for Class III faults
- deployments/ : contains the data (both raw and processed) from elevator, lobby and starbucks

notebooks/ contains the different jupyter notebooks
- FaultDetection/ : are the different fault detection implementations i.e., separate between faulty and working sensors
- FineGrainedFaultAnalysis/ : are the different class III faults i.e., find out whether it is paper, tape or dust that caused the class III fault
