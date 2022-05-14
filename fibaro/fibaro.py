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

# name of HC, rooms(, sections)
# name of HC
def name_hc(data):
    key_value = "hcName"
    if key_value in data:
        hcName = data[key_value]
        return hcName
    else:
        return 0


# names of rooms
def name_rooms(data):
    key_value = "name"
    rooms = []
    for item in data:
        if "sectionID" in item:
            if "defaultSensors" in item:
                for key, value in item.items():
                    if key == key_value:
                        rooms.append(value)
    if len(rooms) > 0:
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

# software version of HC
def software_hc(data):
    key_value = "softVersion"
    if key_value in data:
        #if "hcName" in data:
        #    if key_value in data:
        software_version = data[key_value]
        return software_version
    else:
        return 0


# HC users and connected devices/sensors
# HC users
def users(data):
    key_value = "name"
    user_list = []
    for item in data:
        if "deviceRights" in item:
            if "email" in item:
                for key, value in item.items():
                    if key == key_value:
                        user_list.append(value)
    if len(user_list) > 0:
        return user_list
    else:
        return 0

# HC devices/sensors
def devices(data):
    key_value_1 = "type"
    key_value_2 = "name"
    devices = {}
    for item in data:
        if "remoteGatewayId" in item:
            if "roomID" in item:
                for key, value in item.items():
                    if key == key_value_2:
                        name = value
                        devices[name] = 0
                    if key == key_value_1:
                        devices[name] = value
    if len(devices) > 0:
        return devices
    else:
        return 0

# single out events file, convert to csv, convert timestamps
# identify
def events(data):
    for item in data:
        #print(item)
        if "oldValue" in item:
            if "newValue" in item:
                if "timestamp" in item:
                    return 1
        else:
            return 0 


# convert timestamps to humanly readable
def timestamps(file, path):
    with open(file, "r") as json_file:
        jsondata = json.load(json_file)

    for item in jsondata:
        for key, value in item.items():
            if key == "timestamp":
                time = value
                date_time = datetime.datetime.fromtimestamp(time)
                serialized_date = date_time.isoformat()
                item[key] = serialized_date

    with open(path + "event_timestamps.json", "w") as f:
        json.dump(jsondata, f, indent=4)


# convert to csv
def json_to_csv(file_path, file):
    with open(file_path + file) as json_file:
        jsondata = json.load(json_file)
    
    data_file = open(file_path + "events.csv", 'w', newline='')
    csv_writer = csv.writer(data_file)
    
    count = 0
    for data in jsondata:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    
    data_file.close()

# open JSON files recursively
# path has to be with trailing /
path = input("input absolute base path of folder (add trailing /): ")
for file in glob.glob(os.path.join(path, '*.json')):
    try:
        with open(file) as f:
            data = json.load(f)
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
            if software_hc(data) != 0:
                software = software_hc(data)
            if users(data) != 0:
                user = users(data)
            if devices(data) != 0:
                device = devices(data)
            if events(data) == 1:
                event_file = file
            
    except:
        pass
        

print("home center serial number: ", serialNumber)
print("home center name: ", HCname)
# TODO: make this output prettier
print("rooms: ", rooms)
print("home center IP: ", IP_hc)
print("home center MAC: ", MAC_hc)
print("home center software version: ", software)
# TODO: make this output prettier
print("home center users: ", user)
# TODO: make this output prettier
print("home center devices: ", device)
print("file containing events: ", event_file)
timestamps(event_file, path)
print("file containing events with human readable timestamps at: ", path + "event_timestamps.json")
json_to_csv(path, "event_timestamps.json")
print("file containing events with human readable timestamps, converted to csv, at: ", path + "events.csv")

# TODO: make report/file with extracted data
