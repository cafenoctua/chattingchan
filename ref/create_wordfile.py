import json

def ReadData(filename):
    with open(filename, 'r') as f:
        if '.json' in filename:
            data = json.load(f)
        else:
            data = f.readlines()
    return data
        
if __name__ == "__main__":
    prefs = ReadData('./src/pref_code.json')
    pref = []
    with open('./src/pref.txt', 'w') as f:
        for i in range(len(prefs)):
            f.write(prefs[i]['name']+'\n')