# Real-Time-Monitoring-and-Control-of-Water-Flow-Using-Raspberry-Pi

This project is a real-time water flow monitoring and control system using a Raspberry Pi. The system measures the water flow rate using a water flow sensor and displays the real-time data on an i2c LCD. The control logic is implemented using Python programming.

## Features

- Real-time water flow rate monitoring
- Display of flow rate on an i2c LCD screen
- Python-based implementation for enhanced data processing

## Technologies Used

- **Programming Languages**: Python
- **Hardware**: Raspberry Pi, Water Flow Sensor, i2c LCD Display
- **Software**: Thonny IDE, Node-RED
- **Libraries/Frameworks**: GPIO Zero, smbus2

## Requirements

- Raspberry Pi
- Water Flow Sensor
- i2c LCD Display
- Python 3
- Libraries: `smbus2`, `gpiozero`

You can install the required libraries using pip:

```bash
pip install smbus2 gpiozero
```

## Hardware Setup
  1.Connect the Water Flow Sensor to the GPIO pin 17 on the Raspberry Pi.
  2.Connect the i2c LCD Display to the i2c pins on the Raspberry Pi.

## Installation and Usage.

  1.Clone the Repository:  

    git clone https://github.com/darshith-v/Real-Time-Monitoring-and-Control-of-Water-Flow-Using-Raspberry-Pi.git

    cd Real-Time-Monitoring-and-Control-of-Water-Flow-Using-Raspberry-Pi

  2.Run the Python Script:

    python water_flow_monitor.py
