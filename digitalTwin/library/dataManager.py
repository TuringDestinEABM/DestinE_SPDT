'''Helper scripts for loading in different data'''
import json
from pathlib import Path
import pandas as pd
import geopandas
from flask import current_app, url_for
from digitalTwin import db, routes
import sqlalchemy as sa
import sqlalchemy.orm as so
from digitalTwin.models import models
import numpy as np
from typing import List, Optional

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

# def loadSourceData(table, subset=100):
# def loadGeoJSONDB(city):
#     # print(city)
#     query = sa.Select(models.EPCABMdata).where(models.EPCABMdata.city == city)
    
#     with db.engine.connect() as conn:
#         df = pd.read_sql(query, conn) # load from db to data frame
#     gdf = geopandas.GeoDataFrame(df, 
#                                  geometry=geopandas.points_from_xy(df.geometry_coordinates_lon, df.geometry_coordinates_lat),
#                                   crs="EPSG:4326") # convert to geodataframe
#     gdf = gdf.drop(columns=['id','geometry_type','geometry_coordinates_lon','geometry_coordinates_lat'])
#     return gdf

def loadGeoJSONDB(city: str, subset: int, columns: Optional[List[str]]=None):
    
    geometry = ['geometry_type',
                'geometry_coordinates_lon',
                'geometry_coordinates_lat']

    #Handle Columns
    if columns is None:
        # User didn't pass anything -> Select All
        query = sa.select(models.EPCABMdata)
        # query = query.where(models.EPCABMdata.city == city)
    else:
        # User passed a list -> Select Specific
        # Add non-optional geometry columns
        target_columns = columns + geometry
    
        cols_to_select = [getattr(models.EPCABMdata, col) for col in target_columns]
        query = sa.select(*cols_to_select)
    
    query = query.where(models.EPCABMdata.city == city)

    # Handle Subset (Optional)
    if subset != 100:
        selection = calculateSubset(city, subset)
        # --- FIX: Convert numpy types to standard Python ints ---
        selection = [int(x) for x in selection]
        query = query.where(models.EPCABMdata.id.in_(selection))

    with db.engine.connect() as conn:
        df = pd.read_sql(query, conn) # load from db to data frame
    
    gdf = geopandas.GeoDataFrame(df, 
                                 geometry=geopandas.points_from_xy( df.geometry_coordinates_lat, df.geometry_coordinates_lon),
                                  crs="EPSG:4326") # convert to geodataframe
    gdf = gdf.drop(columns=geometry)
    return gdf

def calculateSubset(city, subset):
    first = db.first_or_404(sa.select(models.EPCABMdata.id).order_by(models.EPCABMdata.id.asc()).where(models.EPCABMdata.city == city))
    last = db.first_or_404(sa.select(models.EPCABMdata.id).order_by(models.EPCABMdata.id.desc()).where(models.EPCABMdata.city == city))
    num = int(subset * (last-first) /100)
    selection = np.linspace(first,last, num, dtype=int)
    return(selection)
    
# def findMetadata(ID):
#     results_dir = Path(current_app.config['RESULTS_DIR'])
#     path = results_dir / ID / "metadata.json"
#     metadata = loadJSONdata(path)
#     return metadata

# def listSummaryFigures(ID):
#     results_dir = Path(current_app.config['RESULTS_DIR'])
#     path = results_dir / ID
#     figures = dict(plot_day_hour = str(path /"plot_day_hour.png"),
#                    plot_hexbin = str(path /"plot_day_hour.png"),
#                    plot_prop_type = str(path /"plot_prop_type.png"),
#                    plot_wealth = str(path /"plot_wealth.png")
#                    )
#     return figures

# def listAvailableReports(path):
#     folders = [x for x in path.iterdir() if x.is_dir()]
#     data = list()

#     for folder in folders:
#        mdPath = path / folder / "metadata.json"
#        metadata =  loadJSONdata(mdPath)
#        data.append(metadata) 

#     data = dict(files = data)
#     # print(data)
#     return data


def listAvailableScenarios(page, order='asc'):
    query = sa.select(models.Scenario)
    
    if order == 'desc':
        query = query.order_by(models.Scenario.timestamp.desc())

    data = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('digitaltwin.reports', page=data.next_num) \
            if data.has_next else None
    prev_url = url_for('digitaltwin.reports', page=data.prev_num) \
            if data.has_prev else None
     

    return data, next_url, prev_url

def manageScenarios(page, order='asc'):
    query = sa.select(models.Scenario)
    
    if order == 'desc':
        query = query.order_by(models.Scenario.timestamp.desc())

    data = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('digitaltwin.manageData', page1=data.next_num) \
            if data.has_next else None
    prev_url = url_for('digitaltwin.manageData', page1=data.prev_num) \
            if data.has_prev else None
    reports = findCorrespondingResults(data)

    return data, next_url, prev_url, reports

def viewSourceData(page):
    query = sa.select(models.EPCABMdata)
    data = db.paginate(query, page=page, per_page=50, error_out=False)
    next_url = url_for('digitaltwin.manageData', page2=data.next_num, active_tab='sources') \
            if data.has_next else None
    prev_url = url_for('digitaltwin.manageData', page2=data.prev_num, active_tab='sources') \
            if data.has_prev else None
     

    return data, next_url, prev_url

def findCorrespondingResults(data):
    responses = {}
    for item in data.items:
        id = item.id
                
        # look for corresponding results in the three tables
        tables = [models.AgentTimeSeries, models.EnergyTimeSeries, models.ModelTimeSeries]
        results = []
        for table in tables:
            result = bool(db.session.query(table.id).where(table.scenario_id == id).first()) # returns true if at least on, false if not
            results.append(result)

        # see if no results, three results or partial results
        if sum(results ) == 0:
            response = 'No results'
        elif sum(results) == len(tables):
            response = 'Full results'
        else:
            response = 'Partial results'
        responses[int(id)] = response
    
    return responses

def clearResults(id):
    tables = [models.AgentTimeSeries, models.EnergyTimeSeries, models.ModelTimeSeries]
    for table in tables:
        print('clearing ' + str(table))
        stmt = sa.delete(table).where(table.scenario_id == id)
        db.session.execute(stmt)
    db.session.commit()

def deleteScenario(id):
    scenario = db.session.get(models.Scenario, id)
    
    if scenario:
        # This single line deletes the scenario AND all 3 time series tables automatically
        db.session.delete(scenario)
        db.session.commit()

