import os
from datetime import date, datetime
import csv
import json
import requests

latlng_fn = './src/lat_lng.txt'
constellation_fn = './src/constellation.txt'

class Featch2API():
    def __init__(self, choose_api):
        self.today = date.today()
        self.now = datetime.now()
        if choose_api == 'gurunavi':
            self.urls = 'https://api.gnavi.co.jp/RestSearchAPI/v3/'
            self.api_key = os.environ['GURUNAVI_API_KEY']
        elif choose_api == 'hoshimiru':
            self.urls = 'https://livlog.xyz/hoshimiru/constellation'
        else:
            self.urls = None
    
    def HoshimiruAPI(self, prefectures, constellation, spec_date = date.today().strftime("%Y-%m-%d"), spec_hour=datetime.now().strftime("%H")):

        lat_lng = self.LatLngByPrefectures(prefectures)
        id = self.Constellation2ID(constellation)
        r = requests.get(self.urls, params = {'lat': lat_lng['lat'], 'lng': lat_lng['lng'], 'date': spec_date, 'hour': spec_hour, 'min': 0, 'id': id, 'disp': "on"})

        return r

    def GuruNaviRestrantAPI(self):
        r = requests.get(self.urls, params = {'keyid': self.api_key, 'freeword': 'ラーメン', 'pref': 'PREF01'})
        total_hit_count = r.json()['total_hit_count']
        rest_info = {}
        for i in range(len(r.json()['rest'])):
            rest_info[f"rest{i}"] = {}
            rest_info[f"rest{i}"]['name'] = r.json()['rest'][i]['name']
            rest_info[f"rest{i}"]['latitude'] = r.json()['rest'][i]['latitude']
            rest_info[f"rest{i}"]['longitude'] = r.json()['rest'][i]['longitude']
            rest_info[f"rest{i}"]['url'] = r.json()['rest'][i]['url']
            rest_info[f"rest{i}"]['url_mobile'] = r.json()['rest'][i]['url_mobile']
            rest_info[f"rest{i}"]['address'] = r.json()['rest'][i]['address']
            rest_info[f"rest{i}"]['tel'] = r.json()['rest'][i]['tel']
            rest_info[f"rest{i}"]['opentime'] = r.json()['rest'][i]['opentime']
            rest_info[f"rest{i}"]['holiday'] = r.json()['rest'][i]['holiday']
        
        rest_data = {}
        rest_data['total_hit_count'] = total_hit_count
        rest_data['rest_info'] = rest_info
        return rest_data
    
    def GuruNaviPrefAPI(self):
        r = requests.get('https://api.gnavi.co.jp/master/PrefSearchAPI/v3/', params={'keyid':os.environ['GURUNAVI_API_KEY'], 'lang':'ja'})

        pref_code = {}
        pref_code['data'] = []
        for i in range(len(r.json()['pref'])):
            pref_code['data'].append({
                'pref': r.json()['pref'][i]['pref_code'],
                'name': r.json()['pref'][i]['pref_name']
            })
        return pref_code['data']

    def ReadTxt(self, filename):
        s = []
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            # next(reader)
            for row in reader:
                s.extend([row])
        return s
    
    def LatLngByPrefectures(self, prefectures):
        pref_lat_lng = self.ReadTxt(latlng_fn)
        for item in pref_lat_lng:
            if prefectures in item[0]:
                return {'lat': float(item[1]), 'lng': float(item[2])}

        return {'lat': None, 'lng': None}

    def Constellation2ID(self, constellation):
        constellations = self.ReadTxt(constellation_fn)
        for item in constellations:
            if constellation in item[1]:
                return {'id': item[0]}
        
        return {'id': None}

    def gpsRequests(self):
        geo_request_url = 'https://get.geojs.io/v1/ip/geo.json'
        geo_data = requests.get(geo_request_url).json()
        print(geo_data['latitude'])
        print(geo_data['longitude'])

if __name__ == '__main__':
    # featch2api = Featch2API('hoshimiru')
    # print(featch2api.HoshimiruAPI('東京', 'アンドロメダ'))
    featch2api = Featch2API('gurunavi')
    print(featch2api.GuruNaviPrefAPI()[0])
    print(featch2api.GuruNaviRestrantAPI())
    # with open('./src/pref_code.json', 'w') as f:
    #     json.dump(featch2api.GuruNaviPrefAPI(), f)
