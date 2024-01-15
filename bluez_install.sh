#!/bin/bash

echo "This script configures bluez on your device"
echo "Lastest version is 5.59, downloading bluez"

wget https://www.kernel.org/pub/linux/bluetooth/bluez-5.69.tar.xz
tar xvf bluez-5.69.tar.xz

echo "installing dependencies"
sudo apt-get install libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev

cd bluez-5.69
export LDFLAGS=-lrt
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --enable-library -disable-systemd
make
sudo make install
sudo cp attrib/gatttool /usr/bin/

echo "Bluez 5.69 Installed!"
