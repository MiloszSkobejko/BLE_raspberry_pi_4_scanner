# Bluetooth Low Energy Scanner on Raspberry Pi 4 (Model B)
This repo contains configuration and source files for bluetooth low energy scanner for raspberry pi.
Raspberry will be used as scanner for advertising data nearby. Gathered data is saved to JSON file 
in the same directory where python script is executed.


## Getting started
Raspbian should have bluez already installed, check it on your device. Updating is recommended. 
```
sudo apt-get update
```

If bluez is not installed, you can install it using:
```
sudo apt-get install bluez 
```

Now you need only bluepy and libglib2.0-dev

```
sudo apt-get install libglib2.0-dev
sudo pip install bluepy
```

I also created script for installing it manually, but it's much safer to do it with apt install.
Do not use this script, unless you are sure what you are doing.


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
