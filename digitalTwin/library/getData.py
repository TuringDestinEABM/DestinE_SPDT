'''Helper scripts for loading in different data'''
import json
from pathlib import Path

def loadJSONdata(filepath):
    with open(filepath) as file:
        data = json.load(file)
    return data
            
def findGEOData(ID, filename):
    filepath = Path(__file__).parents[1] /"data/geo_data/metadata.json"
    metadata = loadJSONdata(filepath)
    for item in metadata["files"]:
        if item["id"] == ID:
           data_loc = item["data_loc"]
           filepath = Path(__file__).parents[1] /"data/geo_data" / data_loc / filename
           data = loadJSONdata(filepath)
           break
    return data
    # TODO: make this do a 404            

def findMetadata(ID):
    path = Path(__file__).parents[1] /"data/geo_data/results" / ID / "metadata.json"
    metadata = loadJSONdata(path)
    
    return metadata

def listSummaryFigures(ID):
    path = Path(__file__).parents[1] /"data/geo_data/results" / ID
    figures = dict(plot_day_hour = str(path /"plot_day_hour.png"),
                   plot_hexbin = str(path /"plot_day_hour.png"),
                   plot_prop_type = str(path /"plot_prop_type.png"),
                   plot_wealth = str(path /"plot_wealth.png")
                   )
    return figures

def listAvailableReports(path):
    folders = [x for x in path.iterdir() if x.is_dir()]
    data = list()

    for folder in folders:
       mdPath = path / folder / "metadata.json"
       metadata =  loadJSONdata(mdPath)
       data.append(metadata) 

    data = dict(files = data)
    # print(data)
    return data