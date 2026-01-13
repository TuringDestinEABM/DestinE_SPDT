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


# TODO: Fix this
# # script for spatial hexbin figure
# def spatialHexBin(df):    
#     fig, ax = plt.subplots(figsize=(6, 6))

#     hb = ax.hexbin(
#         df.geometry.x, # x cordianates
#         df.geometry.y, # y cordianates
#         C=df["total_energy"], # total enercy, z cord
#         reduce_C_function=sum, 
#         gridsize=40,
#         mincnt=1,
#     )

#     # ▼  add an OSM/CartoDB background  ▼
#     cx.add_basemap(
#         ax,
#         crs="EPSG:3857",
#         source=cx.providers.CartoDB.Positron,   # light-grey background
#         attribution=False,                      # omit tiny © text
#     )

#     ax.set_axis_off()
#     fig.colorbar(hb, label="aggregated kWh")
#     ax.set_title("High-usage homes (jittered)")
#     fig.tight_layout()
#     return fig
    
# script for bar chart showing mean energy usage by different property types.
def dailyByPropTypePX(timeseries, prop_cols):
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
    # dataPath = Path(__file__).parents[1] /"data/synthetic_data" / scenario.data_source
      
    # combine agent data and energy usage timeseries into a single dataframe
    agent_ts = analyze.reset_agent_index(dataManager.findDBData('AgentTimeSeries', scenario.id))
    timeseries = analyze.allUsage_ts(scenario, agent_ts, 25)
    timeseries.drop('energy', axis = 1)
    timeseries_js = timeseries.to_json()

    # Get min and max data usage to help define colors in the maplibre GIS
    ec = timeseries['energy_consumption'] 
    energy_range = {"min":round(ec.min(),3), 
                    "max": round(ec.max(),3)
                    }

    # create list of number of steps                
    stepArray = []
    for step in pd.unique(timeseries['step']):
        stepArray.append(int(step))

    steps = {
       "min": min(stepArray),
       "max": max(stepArray),
       "steps": stepArray
    }

    
  
    return steps, timeseries_js, energy_range
