# Real-Time-Monitoring-and-Control-of-Water-Flow-Using-Raspberry-Pi

## 📘 Project Overview
This project is a real-time water flow monitoring system built using a Raspberry Pi, a YF-S201 water flow sensor, and a 16x2 I2C LCD display. It measures the flow rate of water in liters per minute (L/min) and displays it on the LCD and console.

## ✨ Features
- Real-time water flow measurement
- LCD display output
- Console logging for debugging
- Interrupt-driven pulse counting
- I2C communication with LCD

## 🛠️ Hardware Requirements
- Raspberry Pi (any model with GPIO and I2C support)
- YF-S201 Water Flow Sensor
- 16x2 I2C LCD Display (PCF8574 backpack)
- Jumper wires
- Breadboard (optional)

## 💻 Software Requirements
- Raspberry Pi OS
- C++ Compiler (e.g., g++)
- wiringPi Library
- I2C enabled (`raspi-config` → Interfaces → I2C)

## ⚙️ Setup Instructions
1. Connect the YF-S201 sensor to GPIO pin 17.
2. Connect the I2C LCD to the Raspberry Pi's SDA and SCL pins.
3. Enable I2C using `raspi-config`.
4. Install the wiringPi library.
5. Compile the C++ code using:
   ```bash
   g++ flow_monitor.cpp -o flow_monitor -lwiringPi
   ```
6. Run the program using:
   ```bash
   ./flow_monitor
   ```

## 🔍 How It Works
- The YF-S201 sensor generates digital pulses as water flows through it.
- Each pulse is counted using GPIO interrupts.
- Every second, the pulse count is converted to flow rate using a known conversion factor (e.g., 450 pulses = 1 liter).
- The calculated flow rate is displayed on the LCD and printed to the console.

## 🧭 Flowchart Reference
Refer to the flowchart image for a visual representation of the system's operation:
1. System Initialization
2. LCD Initialization
3. Attach Interrupt to Flow Sensor
4. Start Loop
5. Wait 1 Second
6. Calculate Flow Rate
7. Display on LCD
8. Print to Console
9. Repeat

## 📄 License
This project is open-source and available under the MIT License.
