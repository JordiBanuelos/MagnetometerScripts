Hey everyone this githib account includes pyth

# MagnetometerScripts

This repository contains Python scripts for interfacing a **PNI RM3100 triaxial magnetometer** with a **Raspberry Pi** using the **I2C protocol**. It includes tools for:

- Printing real-time magnetic field readings to the terminal
- Logging X, Y, Z magnetic field data and timestamps to a CSV file
- (Optionally) Visualizing data with real-time matplotlib plots

---

## Hardware Requirements

- Raspberry Pi (tested on Pi 3 B+)
- PNI RM3100 Geomagnetism Sensor (I2C version)
- Pi connected to sensor via Cat5 Ethernet cable or jumper wires
- 3.3V power supply (not 5V!) to avoid damaging the sensor

---

## Contents

| File | Description |
|------|-------------|
| `magPrint.py` | Continuously prints X, Y, Z values to the terminal |
| `magToCsv.py`   | Logs X, Y, Z values + timestamps to a CSV file |
| `magplot.py`  | (Optional) Plots values in real time using `matplotlib` |

---

## 🔧 Setup

### 1. Enable I2C on Raspberry Pi:
```bash
sudo raspi-config
# Go to Interfaces → Enable I2C

