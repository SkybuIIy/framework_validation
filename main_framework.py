import json
import csv
import datetime
import requests

### TECHNICAL FRAMEWORK IN FORM OF BASE CLASSES ###\

# even if inheriting from the base class does not help, functions defined can be taken as 
# a baseline and reference point and modified accordingly

# base class for any actions related to file processing
class File_Processing:
    # conversion of file format
    # takes file paths for input and output file
    # only includes conversion from json to csv
    # possibility to extend
    def convert_format(self, input_path, file, output_path):
        
        with open(input_path + file) as json_file:
            jsondata = json.load(json_file)
        
        data_file = open(output_path, 'w', newline='')
        csv_writer = csv.writer(data_file)
        
        count = 0
        for data in jsondata:
            if count == 0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(data.values())
        
        data_file.close()        
    

    # converts Unix Epoch timestamps into human readable
    # only for json files 
    # possibility to extend to other timestamp and file formats
    def convert_timestamp(self, file, path):
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




    # this will most likely need the most adjustments, depending on what information is to be extracted
    # only for json files as of now
    # possibility to extend
    # in this case, it may be more valuable to use this function as a reference rather than inheriting it
    def extract_data(self, data, key_value):
        # for one-dimensional json data
        if key_value in data:
            result = data[key_value]
            return result
        else:
            return 0

    # for nested json data
    # creates a list
    def nested_data(self, data, key_value_1, key_value_2):
        listing = []
        for item in data:
            if key_value_1 in item:
                for key, value in item.items():
                    if key == key_value_2:
                        listing.append(value)
        if len(listing) > 0:
            return listing
        else:
            return 0


# class for interactions with the api
# possible extension to include authentication methods
class API_Actions:
    # need for authentication
    def request_api(self, url, authentication):
        response = requests.get(url, authentication)
        return response.json()



    
    
