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

# Zmienne środowiskowe dystansu
Measured_power = -69
env_n = 2

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Wykryto urzadzenie: {dev.addr}")
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
    
    # Obliczanie dystansu pomiedzy raspberry, a wykrytym urządzeniem
    distance = 10**((Measured_power-device.rssi) / (10 * env_n))
    distance = round(distance, 2)
    
    # Data wykrycia urządzenia
    disc_date = str(datetime.now())
    
    #Sprawdz, czy plik juz istnieje
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        
        # Czy dane urządzenie już zostało dodane
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
        # Jesli plik nie istnieje to stwórz go i zapisz ponownie:
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
    
    filename = "devices.json"
    
    if os.path.exists(filename):
        os.remove(filename)
        print("devices.json został usuniety")
    else:
        print("devices.json nie istnieje w tym katalogu")



def search_in_dev(search_term):
    
    filename = "devices.json"
    
    #Sprawdz, czy plik juz istnieje
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        
        devices = [dev for dev in data if any (search_term.lower() in str(value).lower() for value in dev.values())]
        
        if devices:
            print(f"Znalezione urządzenia zawierające fragment '{search_term}' :")
            for dev in devices:
                formatted = json.dumps(dev, indent=4)
                print(formatted)
        else:
            print(f"Nie znaleziono urządzeń zawierających fragment '{search_term}'")
    else:
        print("devices.json nie istnieje w tym katalogu")


def send_to_server():
    
    filename = "devices.json"
    
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                devices = json.load(file)
                
            server_addr = "http://127.0.0.1:8000/data/"
            
            for dev in devices:
                if dev.get("on server") == 0:
                    formatted = json.dumps(dev, indent=4)
                    json_data = {
                        "device": "Bluetooth Low Energy",
                        "data": formatted
                    }
                    response = requests.post(server_addr, json=json_data)
                
                    if response.status_code == 201:
                        print("[BLuetooth Low Energy] Pomyślnie przesłano dane")
                        
                        # Zaznaczenie, że dane urządzenia zostały przesłane na serwer
                        dev["on server"] = 1
                    else:
                        print(f"[BLuetooth Low Energy] Bład podczas przesyłania danych. Kod odpowiedzi: {response.status_code}")
                        
            with open(filename, 'w') as file:
                json.dump(devices, file, indent=4)
                    
    except Exception as e:
        print(f"[BLuetooth Low Energy] [ERR] wystąpił błąd: {str(e)}")


def main(args):
    parser = argparse.ArgumentParser(description="Bluetooth low energy scanner")
    parser.add_argument("--time", type=float, help="czas trwania skanowania w sekundach, użyj 'inf' dla skanowania w nieskonczoność")
    parser.add_argument("--clear", action="store_true", help="UWAGA! usuwa plik devices.json")
    parser.add_argument("--search", type=str, help="wyszukuje ")
    parser.add_argument("--env", type=int, help="zmienia ustawienia N do obliczania dystansu, ustaw na od 1 do 4")
    parser.add_argument("--send", action="store_true", help="Wysyła devices.json na server")
    
    args = parser.parse_args(args[1:])
    
    # Czyszczenie pliku devices.json
    if args.clear:
        clear_file()
        return 0
    
    # Szukanie danych urządzenia
    if args.search:
        search_in_dev(args.search)
        return 0
        
    # Przesyłanie danych na serwer
    if args.send:
        send_to_server()
        return 0
        
    # Zmiana ustawienia n:
    if args.env:
        if args.env < 1 or args.env > 4:
            print("błąd! ustaw wartosc od 1 do 4")
            return 0
        else:
            env_n = args.env
            print(f"ustawiono N na {env_n}")
            return 0
    
    # Odpalanie skanera 
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
