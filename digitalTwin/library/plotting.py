'''Scripts for creating figures and visual elements, including plotly and maplibre GIS

Figures are returned aas json dumps of plotly fig objects. GIS information returned in geoJSON format, with helper information as dicts.

'''

from ..modelling import analyze
from . import dataManager
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly
import json

from digitalTwin import db, routes
import sqlalchemy as sa
import sqlalchemy.orm as so
from digitalTwin.models import models

def prepare_data(scenario, jitterRadius=25):
    hourly = dataManager.findDBData('EnergyTimeSeries', scenario.id)
    model_ts = dataManager.findDBData('ModelTimeSeries', scenario.id)
    a_ts = dataManager.findDBData('AgentTimeSeries', scenario.id)
    agent_ts = analyze.reset_agent_index(a_ts)
    hi = analyze.highUsage(scenario, agent_ts, 25) 

    model_ts, prop_cols, wealth_cols= analyze.prepTimeSeries(model_ts)
    return hi, model_ts, prop_cols, wealth_cols, hourly
    # return model_ts, prop_cols, wealth_cols, hourly


# script for bar chart showing mean energy usage by different property types.
def dailyByPropTypePX(timeseries, prop_cols):
    prop_cols.remove('id')
    prop_cols.remove('scenario_id')
    timeseries.drop(['id', 'scenario_id'], axis=1)
    daily_type = timeseries.groupby("day")[prop_cols].sum()
    mean_daily_type = daily_type.mean().sort_values(ascending=False)

    ## TODO: remove zero values
    fig = px.bar(mean_daily_type, 
                 labels = {"index":"Property Type",
                        "value":"avg kWh / day"},
                 title="Daily Average by Property Type",
                 width=800, height=600)
    fig.update_layout(showlegend=False, plot_bgcolor='#ffffff') 
    figJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return figJSON


# script for bar chart showing mean energy usage by different wealth groups.
def dailyByWealth(timeseries, wealth_cols):
    daily_w = timeseries.groupby("day")[wealth_cols].sum()
    avg_w   = daily_w.mean().loc[wealth_cols]    # preserve ordering
    print(avg_w.index)
    fig = px.bar(avg_w, 
                 labels = {"index":"Property Type",
                        "value":"avg kWh / day"},
                 title="Daily Average by Wealth Group",
                 color = avg_w.index,
                 color_discrete_map={'high':'darkred', 'medium':'coral', 'low':'lightblue'},
                 width=800, height=500)
    fig.update_layout(showlegend=False, plot_bgcolor='#ffffff')
    fig.update_traces(width=0.35)

    figJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return figJSON

# Heatmap showing total energy usage by day and hour.
def temporalHeatMap(timeseries):

    pivot = timeseries.pivot_table(
        index="day", columns="hour", values="total_energy", aggfunc="sum"
    )

    fig = px.imshow(pivot, width=800, height=400, 
                           labels={"day":"Day","hour":"Hour"},
                           aspect='auto',
                           title="Total demand • day × hour"
                           )

    fig.update_layout(showlegend=True, plot_bgcolor='#ffffff')
    figJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return figJSON

# Produces the data for the maplibre GIS. Returns steps (an array of each time step), timeseries_js (geo_json containing the data), and energy_range (dict of min and max energy usage)
def timeline(scenario):

    # get static data
    # uprns = dataManager.getUPRNs(scenario)
    epc_columns = ["UPRN",
                    "property_type",
                    "property_age",
                    "sap_band_ord"]
    # hidp_columns = ["UPRN",
    #                 "tenure",
    #                 "hh_n_people",
    #                 "hh_income_band",
    #                 "schedule_type"]
    # gdf_static = dataManager.loadGeoJSONSubset(uprns,
    #                                             epc_columns,
    #                                             hidp_columns)
    # print(gdf_static.head())

    gdf_static = dataManager.loadGeoJSONDB('newcastle', scenario.population_id, epc_columns)
    gdf_static_js = gdf_static.to_json()

    # Get min and max data usage to help define colors in the maplibre GIS
    eRange = dataManager.getEnergyRange(scenario.id) 
    energy_range = {"min":round(eRange[0],3), 
                    "max": round(eRange[1],3)
                    }

    # create hour array based on how often recorded
    hourArray=[]
    hour = 0
    while hour < 23:
        hourArray.append(hour)
        hour += scenario.record_every

    return hourArray, gdf_static_js, energy_range

def timeline_daily(scenario, day):
    
    # work out which steps are needed
    stepsToPoll = []
    step = day - 1
    while step < day + 22:
        stepsToPoll.append(step)
        step += scenario.record_every

    # call and flatten dataframe
    target_columns = ['energy_consumption',
                      'step',
                      'Agent_id'
                    ]
    agent_df = dataManager.getEnergyDaily(scenario, stepsToPoll, target_columns)
    agent_df = analyze.reset_agent_index(agent_df)
    # print('---')
    # print(agent_df.head)
    # print('---')

    # reshape into list of dicts
    df_sorted = agent_df.sort_values(by=['agent_id', 'step'])
    energy_data = df_sorted.groupby('agent_id')['energy_consumption'].apply(list).to_dict()
    energy_data = {str(k): v for k, v in energy_data.items()} # force strings to make jsonify happy

    return energy_data