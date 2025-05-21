# 🩺 PIRMedic

## 📁 Repository Overview

This repository contains the code, data, and notebooks used to analyze and diagnose faults in PIR sensors.

---

## 📦 Directory Structure

<details>
<summary><strong>📊 <code>dataset/</code></strong> — Raw & Processed Data</summary>

| Path | Description |
|------|-------------|
| `FaultDetection/faulty_vs_working.csv` | Mixed dataset of `Aout` signals from working and faulty sensors |
| `FaultDetectionFeatures/` | Extracted FFT and FFT-based features for classifying sensor health |
| `FineGrainedFaultAnalysis/` | `Aout` signals from Class III faulty sensors: paper, tape, and dust |
| `FineGrainedFaultAnalysisFeatures/` | FFT-based features for diagnosing specific Class III fault types |
| `deployments/` | Data (raw and processed) from real-world deployments:<br>📍 *Elevator*, *Lobby*, *Starbucks* |
</details>

<details>
<summary><strong>📓 <code>notebooks/</code></strong> — Jupyter Notebooks</summary>

| Folder | Purpose |
|--------|---------|
| `FaultDetection/` | Notebooks for detecting faulty vs. working sensors |
| `FineGrainedFaultAnalysis/` | Notebooks for diagnosing Class III faults (paper, tape, dust) |
</details>

---

## 📌 Highlights

- ✅ Real-world PIR sensor fault data
- ⚙️ FFT and machine learning-based feature extraction
- 🔍 Fine-grained fault classification for Class III anomalies
- 📈 Includes deployment data from varied environments

---

## 📚 Citation

If you use this repository, please cite the corresponding paper from **ACM BuildSys 2021**.  
*(Add BibTeX entry here if needed.)*

---

## 🛠️ Getting Started

To explore the data and run the notebooks:

```bash
git clone https://github.com/your-org/PIRMedic.git
cd PIRMedic/notebooks/FaultDetection
jupyter notebook
```
