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
import glob

### variables ###
print()

### functions ###

# functionalities to implement:
# extract the following
# serial number of HC
def serial_number(data):
    key_value = "serialNumber"
    if key_value in data:
        serialNumber = data[key_value]
        return serialNumber
    else:
        return 0

# name of HC, rooms, sections
# name of HC
def name_hc(data):
    key_value = "hcName"
    if key_value in data:
        hcName = data[key_value]
        return hcName
    else:
        return 0

# this one hard
# is not finished
# if there is sectionID, id in file
# TODO: names of rooms
def name_rooms(data):
    key_value = "name"
    rooms = []
    if "sectionID" & "id" in data:
        for j in data["id"]:
            ID = data["id"]
            if "defaultSensors" in data:
                for i in data[key_value]:
                    rooms.append(data[key_value])
                return rooms
    else:
        return 0

# TODO: names of sections (optional)

# IP and MAC address of HC
# IP address
def ip_hc(data):
    key_value = "ip"
    if "dhcp" in data:
        if "gateway" in data:
            if key_value in data:
                ip_address = data[key_value]
                return ip_address
    else:
        return 0

# MAC address
def mac_hc(data):
    key_value = "mac"
    if "serialNumber" in data:
        if "hcName" in data:
            if key_value in data:
                mac_address = data[key_value]
                return mac_address
    else:
        return 0

# TODO: software version of HC
def software_hc(data):
    key_value = "softVersion"
    if key_value in data:
        #if "hcName" in data:
        #    if key_value in data:
        software_version = data[key_value]
        return software_version
    else:
        return 0


# TODO: HC users and connected devices/sensors
# TODO: HC users
def users(data):
    key_value = "name"
    users = []
    if "email" in data:
        if "id" in data:
            if "type" in data:
                for i in data["id"]:
                    users.append(data[key_value])
                return users
    else:
        return 0

# TODO: HC devices/sensors
# not working
def devices(data):
    key_value_1 = "type"
    key_value_2 = "name"
    devices = {}
    if "remoteGatewayId" in data:
        print("no")
        if "id" in data:
            if "roomID" in data:
                print("fu")
                for i in data["id"]:
                    key = data[key_value_1]
                    value = data[key_value_2]
                    devices[key] = value
                return devices
    else:
        return 0

# TODO: single out events file, convert to csv, convert timestamps
# TODO: identify
def events(data):
    if "id" & "type" & "timestamp" & "deviceID" & "oldValue" & "newValue" in data:
        return 1
    else:
        return 0

# TODO: convert timestamps to humanly readable
def timestamps(file):
    with open(file) as json_file:
        jsondata = json.load(json_file)

    for i in jsondata:
        if "timestamp" in jsondata:
            time = jsondata["timestamp"]
            datetime_time = str(datetime.date.fromtimestamp(time))
            jsondata["timestamp"] = datetime_time    


# TODO: convert to csv
def json_to_csv(file_path):
    with open(file_path) as json_file:
        jsondata = json.load(json_file)
    
    data_file = open("events.csv", 'w', newline='')
    csv_writer = csv.writer(data_file)
    
    count = 0
    for data in jsondata:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    
    data_file.close()
    return

# TODO: open JSON files recursively
path = input("input absolute base path of folder: ")
# ext = (".json", ".csv")
for file in glob.glob(os.path.join(path, '*.json')):
#for file in os.listdir(path):
    #if file.endswith(ext):
    #if file.endswith(".json"):
    try:
        with open(file) as f:
        #f = open(file)
            data = json.load(f)
        #print(data)
            print(software_hc(data))
            if serial_number(data) != 0:
                serialNumber = serial_number(data)
            if name_hc(data) != 0:
                HCname = name_hc(data)
            if ip_hc(data) != 0:
                IP_hc = ip_hc(data)
            if mac_hc(data) != 0:
                MAC_hc = mac_hc(data)
            if name_rooms(data) != 0:
                rooms = name_rooms(data)
            # this one seems like it should work, but doesn't
            if software_hc(data) != 0:
                software = software_hc(data)
            if users(data) != 0:
                user = users(data)
            if devices(data) != 0:
                device = devices(data)
    except:
        pass
        
        #for i in data['some_shit']:
        #    print(i)
    #else:
     #   continue

#with open("fibaro/general_settings.json") as f:
 #   data = json.load(f)

#print(serial_number(data))

print(serialNumber)
print(HCname)
# rooms don't work yet
#print(rooms)
print(IP_hc)
print(MAC_hc)
#print(software)
#print(user)
#print(device)
