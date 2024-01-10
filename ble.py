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
sys.path.append("/home/dron5g/.local/lib/python3.9/site-packages")

from bluepy.btle import Scanner, DefaultDelegate
from pygments import highlight, lexers, formatters

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Nowe urzadzenie: {dev.addr}")
        elif isNewData:
            print(f"Orzymano nowe dane od urządzenia: {dev.addr}")

def main(args):
    
    scanner = Scanner().withDelegate(ScanDelegate())
    devices_m = []
    
    # całkowity czas skonaowania
    scan_time = 60;
    start_time = time.time()
    
    print("[BLuetooth Low Energy] Skanowanie rozpoczęte")
    
    while time.time() - start_time < scan_time:
        #interwały skanowania (co 10 sekund)
        devices = scanner.scan(10)
        
        for dev in devices:
            name = ""
            power = ""
            for (adtype, desc, value) in dev.getScanData():
                if (desc == "Nazwa urządzenia"):
                    name = str(value)
                elif (desc == "Tx Power"):
                    power = str(value)
 
            # Jesli urzadzenia 
            devices_m.append({'addr': dev.addr, 'addType': dev.addrType, 'rssi': dev.rssi, 'name': name, 'power': power})
 
        # standard print
        # json_devices = json.dumps(devices_m)
        # print(json_devices)
 
        # colored print
        formatted_json = json.dumps(devices_m, indent=4)
        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        print(colorful_json)
    
    
    # Zakończenie skanowania
    print("[BLuetooth Low Energy] Skanowanie zakończone")
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
