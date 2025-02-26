### Materials used for hardware node
- CubeCell ESP32 Development Board with a 915MHz LoRa Antenna 
- Capacitive Soil Moisture Sensor (3.3 - 5.5 working voltage)
- PH Sensor (PH0 - 14) with a neutral measurement (PH7) at 2.51 V
- Shillehtek GY302 BH1750 Presoldered Light Intensity Module
- CubeCell ASR6502 Development Board with a 915MHz LoRa Antenna


### Construction

Currently in use is a CubeCell ESP32 Dev Board with code to connect to WiFi (testing purposes) and pull satellite temperature and positional data. A Shillehtek Light Intensity Module is also wired in to measure the amount of light captured by the sensor (measured in and at an accurate range of 0-65535 lumens). A Capacitive Soil Moisture Sensor is also connected to measure the amount of water in the soil. This is a rough sensor and will not provide scientifically accurate readings. However it does provide meaningful insight as to the conditions of the soil invisible to the naked eye. 

A 3D printed shell is being designed to protect the circuit while exposing the Soil Moisture Sensor. Caulk will be used to seal the surrounding area to prevent rust and water damage to the other circuits. The shell is designed to be partially buried with the light sensor at the top exposed to measure ambient light. A plastic or glass covering will be installed to protect the sensor from direct contact to the elements.

### Deployment

Deployment testing will be done at the California State University's Northridge campus at its local orange grove to simulate conditions in the Colombian agriculture farm. A LoRaWan gateway is also set up to facilitate communication between the node and user application.