import main_framework
import glob
import json
import os
import csv



class Fibaro_Application(main_framework.File_Processing):

    def __init__(self): 
        self.path = input("input absolute base path of relevant folder (add trailing /): ")
        for file in glob.glob(os.path.join(self.path, '*.json')):
                    try:
                        with open(file) as f:
                            data = json.load(f)
                            #print(self.nested_data(data, "oldValue", "newValue"))
                            if self.extract_data(data, "serialNumber") != 0:
                                self.serialNumber = self.extract_data(data, "serialNumber")
                            if self.extract_data(data, "hcName") != 0:
                                self.HCname = self.extract_data(data, "hcName")
                            if self.extract_data(data, "ip") != 0:
                                self.IP_hc = self.extract_data(data, "ip")
                            if self.extract_data(data, "mac") != 0:
                                self.MAC_hc = self.extract_data(data, "mac")
                            if self.nested_data(data, "defaultSensors", "name") != 0:
                                self.rooms = self.nested_data(data, "defaultSensors", "name")
                            if self.extract_data(data, "softVersion") != 0:
                                self.software = self.extract_data(data, "softVersion")
                            if self.nested_data(data, "deviceRights", "name") != 0:
                                self.user = self.nested_data(data, "deviceRights", "name")
                            if self.devices(data) != 0:
                                self.device = self.devices(data)
                            if self.nested_data(data, "oldValue", "newValue") != 0:
                                self.event_file = file
                            
                    except:
                        pass

    # special case in which a dict is created 
    def devices(self, data):
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

test = Fibaro_Application()     


# output can be on standard output
print("home center serial number: ", test.serialNumber)
print("home center name: ", test.HCname)
print("rooms: ", test.rooms)
print("home center IP: ", test.IP_hc)
print("home center MAC: ", test.MAC_hc)
print("home center software version: ", test.software)
print("home center users: ", test.user)
print("home center devices: ", test.device)
print("file containing events: ", test.event_file)
test.convert_timestamp(test.event_file, test.path)
print("file containing events with human readable timestamps at: ", test.path + "event_timestamps.json")
test.convert_format(test.path,  "event_timestamps.json", test.path+"events.csv")
print("file containing events with human readable timestamps, converted to csv, at: ", test.path + "events.csv")

# or output can be fed into report format, as preferred
# in this case csv file created which
# possible extension of base classes
with open('report.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['home center serial number', test.serialNumber])
    writer.writerow(['home center name', test.HCname])
    writer.writerow(['rooms', test.rooms])
    writer.writerow(['home center IP', test.IP_hc])
    writer.writerow(['home center MAC', test.MAC_hc])
    writer.writerow(['home center software version', test.software])
    writer.writerow(['home center users', test.user])
    writer.writerow(['home center devices', test.device])
    writer.writerow(['events file', test.event_file])
    writer.writerow(['events file human readable timestamps', test.path + "event_timestamps.json"])
    writer.writerow(['events file csv', test.path + "events.csv"])
