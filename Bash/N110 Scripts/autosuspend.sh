#!/bin/bash

echo 2 > /sys/bus/usb/devices/1-8/power/autosuspend;
echo auto > /sys/bus/usb/devices/1-8/power/level;

echo 2 > /sys/bus/usb/devices/3-2/power/autosuspend;
echo auto > /sys/bus/usb/devices/3-2/power/level;
