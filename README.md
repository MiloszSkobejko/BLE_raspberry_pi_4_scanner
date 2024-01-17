# Bluetooth Low Energy Scanner on Raspberry Pi 4 (Model B)
This repo contains configuration and source files for bluetooth low energy scanner for raspberry pi.
Raspberry will be used as scanner for advertising data nearby. Gathered data is saved to JSON file 
in the same directory where python script is executed.


## Getting started
Please check if your device has bluez as well as bluepy installed. if not, you can install bluez using:
```
sudo apt-get install bluez
sudo apt-get install libglib2.0-dev
```

I also created script for installing it manually, but it's much safer to do it with apt install.
Do not use this script, unless you are sure what you are doing.

```
sudo pip install bluepy
```
These are all packages you'll need in order to get started with ble.


## How to use it

#### [--time] 
Runs script with scan time parameters (in seconds). 

```
./ble.py --time 60
```

If you want to scan inifinitly long, run:
```
./ble.py --time inf
```


#### [--clear]
Deletes the JSON file with scanned data.
```
./ble.py --clear
```

#### [--search]
Use it for seraching in devices.json. It will print out in console all device data that will contain searched string
```
./ble.py --search 80:bb:34
./ble.py --search miband
```
