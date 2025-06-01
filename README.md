# 🩺 PIRMedic

## 📁 Repository Overview

This repository contains the code, data, and notebooks used to analyze and diagnose faults in PIR sensors.

---

## 📦 Directory Structure

<details>
<summary><strong>📓 <code>src/</code></strong> — Code used in the edge platform: *Arduino* and *Raspberry Pi*</summary>

| Folder | Purpose |
|--------|---------|
| `edge_platform/arduino` | Data collection sketches used in the Arduino Microcontroller |
| `edge_platform/raspberrypi` | Data Analysis & Feature extraction python code used in the Raspberry Pi |
| `matlab` | MATLAB Visualization scripts for frequency visualization and K-S statistic computation |
</details>

<details>
<summary><strong>📓 <code>scripts/</code></strong> — Helper scripts to plot data from different lens types and converting ADC values into voltages</summary>

| Folder | Purpose |
|--------|---------|
| `plot_single_sensor_ADC_count.py` | Helper script to plot voltages from ADC values |
| `plot_single_sensor_lens_types.py` | Helper script to analyze nature of voltage waveforms from different lens types |
</details>

<details>
<summary><strong>📊 <code>dataset/</code></strong> — Raw & Processed Data</summary>

| Path | Description |
|------|-------------|
| `FaultDetection/faulty_vs_working.csv` | Time-domain of `Aout` signals from working and faulty sensors |
| `FaultDetectionFeatures/` | Extracted FFT and FFT-based features for classifying PIR sensor health |
| `FineGrainedFaultAnalysis/` | Time-domain of `Aout` signals from Class III faulty sensors |
| `FineGrainedFaultAnalysisFeatures/` | FFT-based features for diagnosing specific Class III fault types |
| `deployments/` | Data (raw and processed) from real-world deployments: *Elevator*, *Lobby*, *Starbucks* |
</details>

<details>
<summary><strong>📓 <code>notebooks/</code></strong> — Jupyter Notebooks</summary>

| Folder | Purpose |
|--------|---------|
| `FaultDetection/` | Notebooks for detecting faulty vs. working sensors |
| `FineGrainedFaultAnalysis/` | Notebooks for diagnosing Class III faults (paper, tape, dust) |
</details>

<details>
<summary><strong>📓 <code>docs/</code></strong> — Back of the Envelope Calculations + Warm-up Analysis</summary>

| Folder | Purpose |
|--------|---------|
| `back_of_envelope_analysis/` | Data collected from sensors in the lab that were subjected to thermal stress |
| `warmup_analysis.md` | Notes containing observations from warm-up analysis in PIR sensors |
</details>

## 🛠️ Getting Started

- ``` git clone https://github.com/synercys/PIRMedic.git ```
- Flash the appropriate sketch on Arduino from ```src/edge_platform/arduino``` depending on the number and type of PIR sensors
- Connect the Arduino to the Raspberry Pi using a serial cable and note the serial device 
  - e.g., ```/dev/cu.usbmodem1421```
- Copy ```src/edge_platform/arduino``` onto the Raspberry Pi using ```scp```
- Run ```main.py``` using ```python3 main.py```. 
  - ```main.py``` will read the data collected from the Arduino through the serial device and store the features in ```data/``` directory on the Raspberry Pi
- For fault detection or fault diagnosis, when needed run the corresponding jupyter notebook from ```notebooks/``` on the Raspberry Pi
  - The notebooks can also be run on a separate server, provided ```data/``` from the Raspberry Pi is copied to it

---

## 📌 Highlights

- ✅ Real-world PIR sensor fault data
- ⚙️ FFT and machine learning-based feature extraction
- 🔍 Fine-grained fault classification for Class III anomalies
- 📈 Includes deployment data from varied environments

---

## 📚 Citation

Please read the paper from ACM [TOSN]() and [BuildSys]() for additional information

---