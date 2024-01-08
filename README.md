# 5G_Drone
This repo contains configuration and source files for land-drone device. Drone is equipped with different types of data transmitters and receivers as 5G, WiFi, LoraWAN and Bluetooth Low Energy.  Main purpose is being a portable range extender for listed technologies. 

## Installing Raspberri Pi 4 image on your device.
In case if you don't have ready to work raspberry pi, you can install my image with bluetooth le configured and (presumably) working.
OS image is in the Image folder, follow official raspberry pi instruction in order to install it:
[link]

## Installing only Bluetooth Low Energy module
If you have your own image already installed and don't want to change it, script below will install all important libraries and modules on your device.


## BLE Remaining Tasks
- [ ] add raspberri pi image
- [ ] add ble config files (bash script that download bluez as well as bluepy)
- [ ] add ble source files
- [ ] create server that checks if collected by ble files has been correctly sent 
