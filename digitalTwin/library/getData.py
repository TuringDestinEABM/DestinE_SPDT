from json import loads as json_loads
from flask import jsonify

def getGEOJSON(file_path):
    with open(file_path) as file:
        try: 
            result = jsonify(file)
        except:
            result = jsonify()
        finally: 
            return result
            
