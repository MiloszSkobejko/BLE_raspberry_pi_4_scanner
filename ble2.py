#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ble2.py
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
#  
#  


import sys
sys.path.append("/home/dron5g/.local/lib/python3.9/site-packages")

import json
from bluepy.btle import Scanner, DefaultDelegate
from pygments import highlight, lexers, formatters
 
try:
    # based on http://ianharvey.github.io/bluepy-doc/scanner.html#sample-code
 
    scanner = Scanner() 
    devices = scanner.scan(10.0)
 
    devices_m = []
 
    for dev in devices:
        name = ""
        power = ""
        for (adtype, desc, value) in dev.getScanData():
            if (desc == "Complete Local Name"):
                name = str(value)
            elif (desc == "Tx Power"):
                power = str(value)
 
        # add device addr, addType and rssi to devices_m
        devices_m.append({'addr': dev.addr, 'addType': dev.addrType, 'rssi': dev.rssi, 'name': name, 'power': power})
 
    # standard print
    # json_devices = json.dumps(devices_m)
    # print(json_devices)
 
    # colored print
    formatted_json = json.dumps(devices_m, indent=4)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)
 
except Exception as ex:
    print ( "Unexpected error in BLE Scanner BLUEPY: %s" % ex )
