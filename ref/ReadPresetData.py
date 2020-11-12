import csv
import requests

class ReadPresetData():
    def __init__(self):
        self.latlng_fn = './src/lat_lng.txt'
        self.constellation_fn = './src/constellation.txt'

    def ReadTxt(self, file_type):
        if file_type == 'lat_lng':
            filename = self.latlng_fn
        elif file_type == 'constellation':
            filename = self.constellation_fn

        s = []
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            # next(reader)
            for row in reader:
                s.extend([row])
        return s