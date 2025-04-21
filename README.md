# SRAM Static Noise Margin (SNM) Generation Tool

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-matplotlib%2C%20pandas%2C%20numpy-orange)
## Overview

This Python-based tool provides visualization support for analog simulations by generating Voltage Transfer Characteristic (VTC) graphs and calculating Static Noise Margin (SNM) for SRAM cells.

## 工作流程演示

```mermaid
graph LR
  A[1. 初始化] --> B[2. 扫描]
  B --> C[3. 采集]
  C --> D[4. 计算]
  D --> E[5. 可视化]
```

<div align="center">
  <img src="./images/1.png" width="15%" title="1. 初始化">
  <img src="./images/2.png" width="15%" title="2. 扫描"> 
  <img src="./images/3.png" width="15%" title="3. 采集">
  <img src="./images/4.png" width="15%" title="4. 计算">
  <img src="./images/5.png" width="15%" title="5. 可视化">
</div>

<div style="text-align: center; margin-top: 10px;">
  <small>图：SRAM SNM分析五步工作流程</small>
</div>
---

## Key Features

- **Supports two analysis modes**:
  - Static/read analysis (`SNM_twosquare.py`)
  - Write analysis (`SNM_onesquare.py`)
- **Processes simulation data from Cadence Virtuoso**
- **Automatically identifies SNM through largest square fitting**
- **Generates professional VTC plots with SNM visualization**

---

## System Requirements

- **Programming Language**: Python 3
- **Recommended IDE**: PyCharm
- **Dependencies**:
  - `matplotlib`
  - `pandas`
  - `numpy`

---

## Usage Instructions

### 1. Simulation Data Preparation

- Perform simulations in Cadence Virtuoso ADE L.
- Export sweep results for both left and right voltage nodes as CSV files.

### 2. Tool Configuration

- For static/read analysis, use `SNM_twosquare.py`.
- For write analysis, use `SNM_onesquare.py`.

### 3. File Setup

- Edit the input file paths in the Python script to point to your CSV files.
- Specify your desired output filename.
- **(For `SNM_twosquare.py` only)**: Set an appropriate cutoff voltage for loop separation.

### 4. Execution

- Run the Python script.
- The tool will:
  - Process the simulation data.
  - Generate VTC plots.
  - Calculate and display SNM.
  - Save the graph image in the script's directory.

---

## Performance Notes

- The largest square fitting algorithm provides approximate results.
- Accuracy depends on simulation sampling rate.
- **Recommended**: Use fewer than 1000 sample points for optimal processing time.

---

## Output

The tool generates an image containing:

- Complete VTC characteristics.
- Identified SNM square regions.
- Calculated noise margin values.

---
