import json

file_path = "./src/pref_code.json"
with open(file_path, "r") as json_file:
    json_data = json.load(json_file)
    print(json_data[-1]['pref'])