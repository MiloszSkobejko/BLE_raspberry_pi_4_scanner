#!/bin/bash

sudo ./ble.py --clear

while true
do
	sudo ./ble.py --time 60
	sudo ./ble.py --send
	sleep 5
done
