'''Helper scripts for loading in different data'''
import pandas as pd
import geopandas
from flask import current_app, url_for, abort, request
from digitalTwin import db, routes
import sqlalchemy as sa
import sqlalchemy.orm as so
from digitalTwin.models import models
import numpy as np
from typing import List, Optional
from. import populations, dataConv

def getID(table, column, value, amount = 'one'):
    # amount can be 'one' or 'all'

    query = sa.Select(table.id).where(column == value)
    result = db.session.scalars(query)

    if amount == 'all':
        return result.all()
    
    else:
        # Try to get the first result
        found_id = result.first()
        
        # If nothing is found, handle the error
        if found_id is None:
            print(f"!! 404 ERROR: No record found in table '{table.__tablename__}' where {column} == '{value}'")
            abort(404)
            
        return found_id
          
def findDBData(DBmodel, identifier=''):

    if DBmodel == 'Scenario':
        data = db.first_or_404(sa.select(models.Scenario).where(models.Scenario.scenario_name == identifier))

    elif DBmodel == 'Population':
        data = db.first_or_404(sa.select(models.Population).where(models.Population.id == identifier))

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
    
    elif DBmodel == 'ClimateModel':
        query  = sa.select(models.ClimateModel)
        if identifier:
            query= query.where(models.ClimateModel.id == identifier)
            data = db.session.scalars(query).first()
        else:
            data = db.session.scalars(query).all()

    elif DBmodel == 'PolicyChoices':
        query  = sa.select(models.PolicyChoices)
        if identifier:
            query= query.where(models.PolicyChoices.id == identifier)
            data = db.session.scalars(query).first()
        else:
            data = db.session.scalars(query).all()

    # if data:
    #     # TODO: fix behaviour with too many results

    return data

def loadGeoJSONDB(city: str, popID, subset, columns: Optional[List[str]]=None, includeGeometry=True):

    # number of rows for context
    # total_count = db.session.scalar(sa.select(sa.func.count(models.EPCABMdata)))

    if includeGeometry ==True: 
        geometry = ['geometry_type',
                    'geometry_coordinates_lon',
                    'geometry_coordinates_lat']
    else: geometry = []

    #Handle columns
    if columns is None:
        # User didn't pass anything -> Select All
        query = sa.select(models.EPCABMdata)
    else:
        # User passed a list -> Select Specific
        # Add non-optional geometry columns
        if isinstance(columns, str):
            columns = [columns]
        target_columns = columns + geometry
        
        cols_to_select = [getattr(models.EPCABMdata, col) for col in target_columns]
        query = sa.select(*cols_to_select)

    # # row numbers for subset
    # row_num_col = sa.func.row_number().over(order_by=models.EPCABMdata.UPRN).label("rn")
    # inner_query = sa.select(*cols_to_select, row_num_col)
    
    # filter by uprn
    subquery_mask = uprnMask(popID)
    mask_query = query.where(models.EPCABMdata.UPRN.in_(subquery_mask))
    print('Matching back to uprn data')
    countMatches(mask_query)

    # stmt = inner_query.mask_query()

    # # filter by subset
    # query = sa.select(stmt).where(stmt.c.rn % int(subset) == 1) #  5
    # print(f"Filtering by subset: {subset}%")
    # countMatches(query)

    # print(f"Selecting {filtered_count} out of {total_count}")

    with db.engine.connect() as conn:
        df = pd.read_sql(query, conn) # load from db to data frame
    
    gdf = geopandas.GeoDataFrame(df, 
                                 geometry=geopandas.points_from_xy( df.geometry_coordinates_lat, df.geometry_coordinates_lon),
                                  crs="EPSG:4326") # convert to geodataframe
    gdf = gdf.drop(columns=geometry)
    return gdf

def uprnMask(popID):
    pop = findDBData('Population', popID)
    uprn = models.UPRNdata
    
    # Filter by wards and property types using EPC data
    ward_codes = dataConv.WardNamesToCodes(pop.wards)
    subquery = sa.select(models.EPCABMdata.UPRN).where(models.EPCABMdata.ward_code.in_(ward_codes))
    print(f'Filtering by wards: {pop.wards}')
    countMatches(subquery)
    if pop.property_types:
        # include null if all wards selected
        if len(pop.property_types) == 7:
            subquery = subquery.where(sa.or_(
                models.EPCABMdata.property_type.in_(pop.property_types),
                models.EPCABMdata.property_type==0)
            )
        else:
            subquery = subquery.where(models.EPCABMdata.property_type.in_(pop.property_types))
        print(f'Filtering by properties {pop.property_types}')
        countMatches(subquery)

    # now other parameters using UPRNdata
    query = sa.select(uprn.UPRN).where(uprn.UPRN.in_(subquery))
    print('Matching to uprn data')
    countMatches(subquery)

    if pop.income_types:
        incomes = dataConv.incomeBands(pop.income_types, 'hidp')
        if len(incomes) == 5:
            print('5*5*5*')
            query = query.where(
                sa.or_(uprn.hh_income_band.in_(incomes),
                uprn.hh_income_band == None)
            )
        else:
            query = query.where(uprn.hh_income_band.in_(incomes))

        print(f'Filtering by incomes: {incomes}')
        countMatches(query)
    
    if pop.schedule_types:
        schedules = dataConv.schedules(pop.schedule_types, 'hidp')
        if len(schedules) == 7:
            query = query.where(
                sa.or_(uprn.schedule_type.in_(schedules),
                uprn.schedule_type == None)
            )
        else:
            query = query.where(uprn.schedule_type.in_(schedules))


        print(f'Filtering by schedules: {schedules}')
        countMatches(query)
    
    return query

def calculateSubset(city, subset):
    first = db.first_or_404(sa.select(models.EPCABMdata.id).order_by(models.EPCABMdata.id.asc()).where(models.EPCABMdata.city == city))
    last = db.first_or_404(sa.select(models.EPCABMdata.id).order_by(models.EPCABMdata.id.desc()).where(models.EPCABMdata.city == city))
    num = int(subset * (last-first) /100)
    selection = np.linspace(first,last, num, dtype=int)
    return(selection)

def getTableData(model, page, url_str, active_tab=None, current_tab_id=None, 
                 order='asc', per_page=50, check_results=False):
    
    query = None

    # extra logic for scenarios
    if check_results and model == models.Scenario:
        # Check if related data exists (returns True/False)
        has_agent_ts = db.session.query(models.AgentTimeSeries.id)\
            .filter(models.AgentTimeSeries.scenario_id == models.Scenario.id).exists()
        has_energy_ts = db.session.query(models.EnergyTimeSeries.id)\
            .filter(models.EnergyTimeSeries.scenario_id == models.Scenario.id).exists()
        has_model_ts = db.session.query(models.ModelTimeSeries.id)\
            .filter(models.ModelTimeSeries.scenario_id == models.Scenario.id).exists()

        query = db.session.query(models.Scenario, has_agent_ts, has_energy_ts, has_model_ts)

        if order == 'desc':
            query = query.order_by(models.Scenario.timestamp.desc())

    # standard logic
    else:
        query = db.session.query(model)

        if order == 'desc':
            query = query.order_by(model.timestamp.desc())

    data = query.paginate(page=page, per_page=per_page, error_out=False)

    
    # Preserves tabs when using next-url or prev_url
    def get_args(next_page_num):
        args = request.args.copy()
        if current_tab_id:
            args['tab'] = current_tab_id 
            args[f'page_{current_tab_id}'] = next_page_num
            
        #Clean up URL by removing old params
        args.pop('active_tab', None)
            
        return args

    next_url = url_for(url_str, **get_args(data.next_num)) if data.has_next else None
    prev_url = url_for(url_str, **get_args(data.prev_num)) if data.has_prev else None
        
    return data, next_url, prev_url
    

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
    
    scenario_data = []
    for item in data.items:
        reports = findCorrespondingResults(item)
        data_obj = {'scenario': item,
                    'reports': reports}
        scenario_data.append(data_obj )

    return scenario_data, next_url, prev_url

def viewSourceData(page):
    query = sa.select(models.EPCABMdata)
    data = db.paginate(query, page=page, per_page=50, error_out=False)
    next_url = url_for('digitaltwin.manageData', page2=data.next_num, active_tab='sources') \
            if data.has_next else None
    prev_url = url_for('digitaltwin.manageData', page2=data.prev_num, active_tab='sources') \
            if data.has_prev else None
     

    return data, next_url, prev_url

def findCorrespondingResults(item):
    
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
    
    return response

def getClimateData(page, flag):
    query = sa.select(models.TemperatureTimeSeries).where(models.TemperatureTimeSeries.flag==flag)
    data = db.paginate(query, page=page, per_page=50, error_out=False)
    next_url = url_for('digitaltwin.climate', page2=data.next_num, active_tab='sources') \
            if data.has_next else None
    prev_url = url_for('digitaltwin.climate', page2=data.prev_num, active_tab='sources') \
            if data.has_prev else None
    return data, next_url, prev_url

def clearResults(id):
    tables = [models.AgentTimeSeries, models.EnergyTimeSeries, models.ModelTimeSeries]
    for table in tables:
        print('clearing ' + str(table))
        stmt = sa.delete(table).where(table.scenario_id == id)
        db.session.execute(stmt)
    db.session.commit()


def deleteEntry(table_id, id):
    table_registry = {
    'scenarios': models.Scenario,
    'climate_models': models.ClimateModel,
    'policy_choices': models.PolicyChoices,
    'population': models.Population
    }

    model = table_registry.get(table_id)
    # handle exceptions
    if model == None:
        print(str(table_id) + ' does not match to a valid table')
    else: 
        entry = db.session.get(model, id)
        
        if entry:
            # Deletes the entry
            # Also deletes the children if entry is a scenario
            db.session.delete(entry)
            db.session.commit()

'''Get the user's login'''
def getUserName():
    # TODO: revisit when login functionality sorted
    username = "<username>"
    return username

def countMatches(query):
    count_stmt = sa.select(sa.func.count()).select_from(query)
    filtered_rows = db.session.scalar(count_stmt)

    print(f"Returning {filtered_rows} rows.")
    print('------')