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
#sys.path.append("/home/dron5g/.local/lib/python3.9/site-packages")

from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Nowe urzadzenie: {dev.addr}")
            save_to_file(dev)
        elif isNewData:
            print(f"Orzymano nowe dane od urządzenia: {dev.addr}")



def save_to_file(device):
    filename = "devices.json"
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
    
    #Sprawdz, czy plik juz istnieje
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        
        # Czy dane urządzenie już zostało dodane
        if not any(entry['addr'] == device.addr for entry in data):
            data.append({'addr': device.addr, 'addType': device.addrType, 'rssi': device.rssi, 'desc': desc, 'raw data': rdata, 'power': power, 'value': value, 'adType': adtype, 'connectable': device.connectable})
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
    else:
        # Jesli plik nie istnieje to stwórz go i zapisz ponownie:
        with open(filename, 'w') as file:
            json.dump([{'addr': device.addr, 'addType': device.addrType, 'rssi': device.rssi, 'desc': desc, 'raw data': rdata, 'power': power, 'value': value, 'adType': adtype, 'connectable': device.connectable}], file, indent=4)



def main(args):
    parser = argparse.ArgumentParser(description="Bluetooth low energy scanner")
    parser.add_argument("--time", type=float, help="czas trwania skanowania w sekundach, użyj 'inf' dla skanowania w nieskonczoność")
    args = parser.parse_args(args[1:])
    
    scanner = Scanner().withDelegate(ScanDelegate())
    
    if  args.time == float('inf'):
        print("[BLuetooth Low Energy] Skanowanie rozpoczęte, czas: niesk")
        
        try:
            while True:
                devices = scanner.scan(10)
        except KeyboardInterrupt:
            pass
        finally:
            print("[BLuetooth Low Energy] Skanowanie zakończone")
    elif args.time:
        print(f"[BLuetooth Low Energy] Skanowanie rozpoczęte, czas: {args.time} sekund")
        start_time = time.time()
        
        while time.time() - start_time < args.time:
            devices = scanner.scan(10)
        print("[BLuetooth Low Energy] Skanowanie zakończone")
    else:
        print("Nie podano czasu skanowania, podaj czas skanowania używając --time <czas w sekundach> lub --time inf")
    
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
