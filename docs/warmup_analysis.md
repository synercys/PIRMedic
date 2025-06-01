<p align="center">
  <a href="" rel="noopener">
    <img src="https://cdn-learn.adafruit.com/assets/assets/000/000/503/medium800/proximity_pirsensor.jpg?1396763621" 
         alt="Insert PIR Sensor Picture here" 
         style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
</p>

<h3 align="center">Internals of PIR Sensor Block</h3>

<div align="center">
  <a href="#"><img src="https://img.shields.io/badge/Sensor-Digital-green.svg" alt="Sensor Type"></a>
  <a href="#"><img src="https://img.shields.io/badge/Cost-%2410-orange.svg" alt="Cost"></a>
  <a href="#"><img src="https://img.shields.io/badge/Environment-Indoors-informational.svg" alt="Environment"></a>
  <a href="#"><img src="https://img.shields.io/badge/Scale-Large%20Scale-yellowgreen.svg" alt="Scale"></a>
  <a href="#"><img src="https://img.shields.io/badge/Applications-Smart%20Buildings-blueviolet.svg" alt="Applications"></a>
</div>

---

<p>
PIR Sensor is a Passive Infrared Sensor that detects the presence of humans or motion in the region of interest. 
They are also called "Pyroelectric" or "IR motion" sensors. The wavelength of IR that is sensed is usually around 10 μm. 
The sensor consists of a pyroelectric material, a Fresnel lens, and a Micro Power PIR Motion Detector IC. 
The board has supporting circuitry to configure the timing and sensitivity of the IC.
</p>

## 📝 Table of Contents
+ [Introduction](#intro)
+ [Physics of the Sensor](#physics)
+ [Block Diagram](#block_diagram)
+ [What can go wrong?](#fault_scenarios)
+ [How do we monitor these blocks?](#monitor)

## Introduction <a name="intro"></a>
PIR sensors are commonly used to detect occupancy in smart buildings to achieve goals such as security and power savings.

## Physics of the Sensor <a name="physics"></a>
PIR sensors work on the principle of pyroelectricity—voltage generation when heat is applied to a material.

## Block Diagram <a name="block_diagram"></a>

<p align="center">
  <a href="" rel="noopener">
    <img src="../figures/warmup_experiments/pir_block_diagram.png" 
         alt="PIR Sensor Block Diagram" 
         style="max-width: 80%; height: auto; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
</p>

<p align="center">
  <a href="" rel="noopener">
    <img src="../figures/warmup_experiments/PIR_sensor_top.jpg" 
         alt="PIR Sensor Top View" 
         style="max-width: 80%; height: auto; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
</p>

<p align="center">
  <a href="" rel="noopener">
    <img src="../figures/warmup_experiments/PIR_sensor_bottom.jpg" 
         alt="PIR Sensor Bottom View" 
         style="max-width: 80%; height: auto; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
</p>

## What can go wrong? <a name="fault_scenarios"></a>
Faults can be due to:
+ Pyroelectric sensing element failure
+ PIR Motion detector IC failure
+ Damage to Fresnel lens

Data correctness can be affected by:
+ False positives due to differential noise

## How can we monitor the block? <a name="monitor"></a>
Current measurements in PIR sensor:

| Status        | Current Measured |
|---------------|-------------------|
| Working Part  | < 24 μA           |

---

## Questions
+ Can I say when an object is present, do we see a current at the output of the pyroelectric?
+ Properties of the pyroelectric element
+ Output for standard input
+ Turning on/off drain, what happens to source?
+ Vary drain, get some source, check Vout — assume constant environment, high sampling
+ Find what types of PIR sensors are on the market
> What are the different ways the sensors fail?

## Common Causes of False Alarms in PIR
**Source:** [ACT Meters - Five Causes of PIR False Alarms](https://www.actmeters.com/advice/five-causes-of-pir-false-alarms/)

+ Low or unstable voltage at the detector.
+ Sudden infrared movement/heat changes.
+ White light momentarily blinding the detector.
+ Direct draught striking the detector.
+ RFI/EMI signals from mobile phones or other devices.

## Initial Experiments
+ **Current-based testing:** Low current (< 25 μA) — unreliable.
+ **Pyroelectric element testing:** Pulse at drain, look at source. Vary PWM duty cycle and voltage at drain, observe source voltage.
+ **Retriggering/non-retriggering modes:** Capture Vout.
+ **Warm-up behavior study:** Vout, Source, and heating/cooling tests.

---

## Warm-up Behavior Observations

<p align="center">
  <a href="" rel="noopener">
    <img src="../figures/warmup_experiments/PIRGreenAnamolous.png" 
         alt="PIR Warm-up Anomalous" 
         style="max-width: 90%; height: auto; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
</p>
<i>Observations:</i> Warm-up behavior without obstruction shows different characteristics from other modules — both Source and Vout observed.

<p align="center">
  <a href="" rel="noopener">
    <img src="../figures/warmup_experiments/PIRGreen1.jpg" 
         alt="PIR Warm-up 1" 
         style="max-width: 90%; height: auto; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
</p>
<i>Observations:</i> Vout spikes each time the sensor is turned on.

<p align="center">
  <a href="" rel="noopener">
    <img src="../figures/warmup_experiments/PIRGreen1_AfterHeating.jpg" 
         alt="PIR Warm-up After Heating" 
         style="max-width: 90%; height: auto; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
</p>
<i>Observations:</i> Heated pyro element at 400°C for ~1 min results in increased response delays.

<p align="center">
  <a href="" rel="noopener">
    <img src="../figures/warmup_experiments/PIRGreen1_AfterCooling.jpg" 
         alt="PIR Warm-up After Cooling" 
         style="max-width: 90%; height: auto; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
</p>
<i>Observations:</i> Behavior reverts to normal after natural cooling.

<p align="center">
  <a href="" rel="noopener">
    <img src="../figures/warmup_experiments/PIRGreen2.jpg" 
         alt="PIR Warm-up Green 2" 
         style="max-width: 90%; height: auto; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
</p>
<i>Observations:</i> Another sensor confirms similar behavior.

<p align="center">
  <a href="" rel="noopener">
    <img src="../figures/warmup_experiments/PIRBlue1.jpg" 
         alt="PIR Warm-up Blue 1" 
         style="max-width: 90%; height: auto; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
</p>
<i>Observations:</i> Different waveform — decaying Vout after switching off.

<p align="center">
  <a href="" rel="noopener">
    <img src="../figures/warmup_experiments/PIRBlue2.jpg" 
         alt="PIR Warm-up Blue 2" 
         style="max-width: 90%; height: auto; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
  </a>
</p>
<i>Observations:</i> Similar to previous—confirmation of behavior.

---

- Compare working & non-working behaviors of PIR sensors.
- Check Vout and output from the BISS0001 IC (pin 2).

| What to Fail            | How to Fail                     | Verify Failure | Quantity to Monitor | Is There a Change? |
|-------------------------|---------------------------------|----------------|----------------------|--------------------|
| Pyroelectric Element    | Heating one leg of the element  | ?              |                      |                    |

---

### List of Experiments Planned After Team Meeting

First, we characterize the working sensors. We look at Vout and later at source voltage:

+ Vout as a function of distance

