### imports ###
import datetime
import time
import io
import sys
import requests
import json
import configparser
import csv
import os

### variables ###


### functions ###





# functionalities to implement:
# extract the following
# TODO: serial number of HC
def serial_number(data):
    key_value = "serialNumber"
    if key_value in data:
        serialNumber = data[key_value]
        return serialNumber
    else:
        return 0

# TODO: name of HC, rooms, sections
# TODO: IP and MAC address of HC
# TODO: software version of HC
# TODO: HC users and connected devices/sensors
# TODO: single out events file, convert to csv, convert timestamps


# open JSON files recursively
path = input("input absolute base path of folder: ")
# ext = (".json", ".csv")
for file in os.listdir(path):
    #if file.endswith(ext):
    if file.endswith(".json"):
        f = open(file)
        data = json.load(f)
        for i in data['some_shit']:
            print(i)
    else:
        continue