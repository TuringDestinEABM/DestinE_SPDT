import json

def loadJSONdata(filepath):
    with open(filepath) as file:
        data = json.load(file)
    return data
            
