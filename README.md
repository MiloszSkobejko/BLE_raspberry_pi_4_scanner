# 5G_Drone BLE Module on Raspberry Pi 4 (Model B)
This repo contains configuration and source files for bluetooth low energy raspberry pi. 

## Getting started
Please check if your device has bluez as well as bluepy installed. if not, you can install bluez using:
```
sudo apt-get install bluez
sudo apt-get install libglib2.0-dev
```
and bluepy:
```
sudo pip install bluepy
```
These are all packages you'll need in order to get started with ble.


## How to use
Run script with scan time parameters (in seconds). Json file with results will be created in the same location as where script is executed.

```
./ble.py --time 60
```

If you want to scan inifinitly long, run:
```
./ble.py --time inf
```
