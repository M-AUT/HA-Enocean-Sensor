# HA-Enocean-Sensor
EnOcean STM 550B / EMSWB (BLE) 

Home Assistant Integration for energy harvesting EnOcean STM 550B and EMSWB BLE sensors.  

Features 
-  Temperature
-  Humidity
-  Illuminance
-  Motion Acceleration X/Y/Z
-  Magnet Contact sensor
-  Energy storage level

Requirements
-  Home Assistant with Bluetooth support
-  EnOcean STM 550B or EMSWB sensor
-  BLE device address
-  Security key (AES key) - can be set at the sensor via NFC in the Enocean App. Format must be e.g. 00112233445566778899AABBCCDDEEFF   


Installation
Copy the enocean_stm550 folder to:
config/custom_components/
Resulting directory structure:

config/custom_components/

    └── custom_components/
        └── enocean_stm550/
            ├── __init__.py
            ├── binary_sensor.py
            ├── config_flow.py
            ├── const.py
            ├── decoder.py
            ├── entity.py
            ├── manifest.json
            ├── sensor.py
            ├── strings.json
            └── translations/
Restart Home Assistant.

Go to:

Settings → Devices & Services → Add Integration
Search for:
EnOcean STM 550B / EMSWB (BLE)
Enter:

Name
BLE Address
Security Key
Finish setup.


----------------------------------

Status: Early release

Tested with:
- EnOcean STM 550B
- Home Assistant 2026.x



Notes
This integration uses passive Bluetooth advertisements and does not require an active Bluetooth connection.

Disclaimer
This is a community project and is not affiliated with EnOcean or Home Assistant.

Screenshots

<img width="713" height="545" alt="image" src="https://github.com/user-attachments/assets/24fb267c-edc3-42b8-bc33-3e4c5d36c37c" />
<img width="497" height="607" alt="image" src="https://github.com/user-attachments/assets/2278d6c5-1708-465c-b069-7006a9de8f83" />




