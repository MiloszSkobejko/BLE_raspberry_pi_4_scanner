#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ble.py
#  
#  Copyright 2024  <dron5g@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.


#  Enabling Bluetooth low energy on Raspberry Pi 4 device.
#  Dron 5G

import sys
import json
import time
import os.path
import argparse
import requests
#sys.path.append("/home/dron5g/.local/lib/python3.9/site-packages")
from bluepy.btle import Scanner, DefaultDelegate
from datetime import datetime

# Environmental variables
Measured_power = -69
env_n = 2
server_ip = "http://127.0.0.1:8000/data/"
filename = "devices.json"

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"[RPi BLE] Device Discovered: {dev.addr}")
            save_to_file(dev)
        elif isNewData:
            print(f"[RPi BLE] Recieved new data from device: {dev.addr}")


def set_global_variables(config_path='ble.cfg'):
    try:
        if os.path.exists(config_path):
            with open('ble.cfg', 'r') as file:
                config = file.readlines()
            
            for line in config:
                parts = line.strip().split('=')
                if len(parts) == 2:
                    if parts[0].strip() == 'env_n':
                        n = int(parts[1].strip())
                    elif parts[0].strip() == 'Measured_power':
                        force = float(parts[1].strip())
                    elif parts[0].strip() == 'server_ip':
                        ip = parts[1].strip()
                    elif parts[0].strip() == 'filename':
                        filename = parts[1].strip()
            
            globals()['env_n'] = n
            globals()['Measured_power'] = force
            globals()['server_ip'] = ip
            globals()['filename'] = filename

    except Exception as e:
        print(f"[RPi BLE] Error while setting config from file {e}")

def save_to_file(device):
    name = ""
    power = ""
    
    # Raw data reserialise
    for (adtype, desc, value) in device.getScanData():
        if (desc == "Nazwa urządzenia"):
            name = str(value)
        elif (desc == "Tx Power"):
            power = str(value)
    
    # Raw data reserialise for JSON
    rdata = str(device.rawData)
    
    # Calculating distance between scanning device and discovered device in meters,
    # distance depends only on rssi and may not be accurate. It's correctness vary
    # in different enviroments: that's why env_n and measured power variables are handy; 
    # changing their values can make calculating distance more (or less) accurate 
    distance = 10**((Measured_power-device.rssi) / (10 * env_n))
    distance = round(distance, 2)
    
    # Date of discovering device
    disc_date = str(datetime.now())
    
    # Check if file exists
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        
        # Check if device has been already added to devices.json
        if not any(entry['addr'] == device.addr for entry in data):
            
            data.append({'Discovery date': disc_date, 
                         'addr': device.addr,
                         'addType': device.addrType,
                         'rssi': device.rssi,
                         'desc': desc,
                         'raw data': rdata,
                         'power': power,
                         'value': value,
                         'adType': adtype,
                         'distance': distance,
                         'connectable': device.connectable,
                         'on server': 0})
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
    else:
        # If file doesn't exist that create it and save data
        with open(filename, 'w') as file:
            json.dump([{'Discovery date': disc_date, 
                         'addr': device.addr,
                         'addType': device.addrType,
                         'rssi': device.rssi,
                         'desc': desc,
                         'raw data': rdata,
                         'power': power,
                         'value': value,
                         'adType': adtype,
                         'distance': distance,
                         'connectable': device.connectable,
                         'on server': 0}], file, indent=4)

def clear_file():
    if os.path.exists(filename):
        os.remove(filename)
        print("[RPi BLE] devices.json has been removed")
    else:
        print("[RPi BLE] devices.json doesn't exist in current directory")



def search_in_dev(search_term):
    # Check if file exist in curr directory
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        
        devices = [dev for dev in data if any (search_term.lower() in str(value).lower() for value in dev.values())]
        
        if devices:
            print(f"[RPi BLE] Found devices containg searched phrase: '{search_term}' :")
            for dev in devices:
                formatted = json.dumps(dev, indent=4)
                print(formatted)
        else:
            print(f"[RPi BLE] Devices containg searched phrase not found'{search_term}'")
    else:
        print("[RPi BLE] devices.json doesn't exist in current directory")


def send_to_server():
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                devices = json.load(file)
                
            for dev in devices:
                if dev.get("on server") == 0:
                    formatted = json.dumps(dev, indent=4)
                    json_data = {
                        "device": "Bluetooth Low Energy",
                        "data": formatted
                    }
                    response = requests.post(server_ip, json=json_data)
                
                    if response.status_code == 201:
                        print("[RPi BLE] data sent succesfully")
                        
                        # If device data has been sent to server, on server field is changed to 1
                        # in order to avoid duplicates
                        dev["on server"] = 1
                    else:
                        print(f"[RPi BLE] Error while sending data. Error code: {response.status_code}")
                        
            with open(filename, 'w') as file:
                json.dump(devices, file, indent=4)
                    
    except Exception as e:
        print(f"[RPi BLE] Error found: {str(e)}")


def main(args):
    parser = argparse.ArgumentParser(description="Bluetooth low energy scanner")
    parser.add_argument("--time", type=float, help="scan time in seconds, use 'inf' for infinite scanning")
    parser.add_argument("--clear", action="store_true", help="WARNING! deletes devices.json")
    parser.add_argument("--search", type=str, help="search given string in devices.json and prints all device data, which contain serached phrase")
    parser.add_argument("--env", type=int, help="changes N variable, set it from 1 to 4")
    parser.add_argument("--send", action="store_true", help="sends devices.json data to server")
    
    args = parser.parse_args(args[1:])
    
    # Deleting devices.json
    if args.clear:
        clear_file()
        return 0
    
    # Searching for phrase 
    if args.search:
        search_in_dev(args.search)
        return 0
        
    # Sending data to servers
    if args.send:
        send_to_server()
        return 0
        
    # Changes env_n variable value
    if args.env:
        if args.env < 1 or args.env > 4:
            print("[RPi BLE] Error! set it from 1 to 4")
            return 0
        else:
            env_n = args.env
            print(f"[RPi BLE] N value (env_n) changed to {env_n}")
            return 0
    
    
    scanner = Scanner().withDelegate(ScanDelegate())
    
    if  args.time == float('inf'):
        print("[RPi BLE] Starting scanning, time: infinite")
        
        try:
            while True:
                devices = scanner.scan(10)
        except KeyboardInterrupt:
            pass
        finally:
            print("[RPi BLE] Scanning completed")
    elif args.time:
        print(f"[RPi BLE] Starting scanning, time: {args.time} seconds")
        start_time = time.time()
        
        while time.time() - start_time < args.time:
            devices = scanner.scan(10)
        print("[RPi BLE] Scanning completed")
    else:
        print("Scan time wasn't scecified, set scan time using --time <time in seconds> or --time inf")
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))