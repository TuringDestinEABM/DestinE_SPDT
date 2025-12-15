'''Helper scripts for loading in different data'''
import json
from pathlib import Path
import pandas as pd
from flask import current_app, url_for
from digitalTwin import db, routes
import sqlalchemy as sa
import sqlalchemy.orm as so
from digitalTwin.models import models

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

def findDBData(DBmodel, identifier):
    if DBmodel == 'Scenario':
        data = db.first_or_404(sa.select(models.Scenario).where(models.Scenario.scenario_name == identifier))

    elif DBmodel == 'EnergyTimeSeries':
        query = sa.Select(models.EnergyTimeSeries).where(models.EnergyTimeSeries.scenario_id == identifier)
        with db.engine.connect() as conn:
            data = pd.read_sql(query, conn)

    elif DBmodel == 'ModelTimeSeries':
        query = sa.Select(models.ModelTimeSeries).where(models.ModelTimeSeries.scenario_id == identifier)
        with db.engine.connect() as conn:
            data = pd.read_sql(query, conn)

    elif DBmodel == 'AgentTimeSeries':
        query = sa.Select(models.AgentTimeSeries).where(models.AgentTimeSeries.scenario_id == identifier)
        with db.engine.connect() as conn:
            data = pd.read_sql(query, conn)
        
    return data

def findMetadata(ID):
    results_dir = Path(current_app.config['RESULTS_DIR'])
    path = results_dir / ID / "metadata.json"
    metadata = loadJSONdata(path)
    return metadata

def listSummaryFigures(ID):
    results_dir = Path(current_app.config['RESULTS_DIR'])
    path = results_dir / ID
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


def listAvailableScenarios(page):
    query = sa.select(models.Scenario).order_by(models.Scenario.timestamp.desc())
    data = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('digitaltwin.reports', page=data.next_num) \
        if data.has_next else None
    prev_url = url_for('digitaltwin.reports', page=data.prev_num) \
        if data.has_prev else None

    return data, next_url, prev_url