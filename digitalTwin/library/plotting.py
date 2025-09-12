from ..modelling import analyze
from pathlib import Path
import geopandas as gpd
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import plotly
import matplotlib.pyplot as plt
import json
import contextily as cx  


def prepare_data(sourceData, outdir, jitterRadius=25):
    dataPath = Path(__file__).parents[1] /"data/ncc_data" / sourceData
    outdir = Path(outdir)

    hourly   = pd.read_csv(outdir / "energy_timeseries.csv")
    model_ts = pd.read_parquet(outdir / "model_timeseries.parquet")
    agent_ts = analyze.reset_agent_index(pd.read_parquet(outdir / "agent_timeseries.parquet"))
   
    hi = analyze.highUsage(dataPath, agent_ts, 25)
    model_ts, prop_cols, wealth_cols = analyze.prepTimeSeries(model_ts)
    return hi, model_ts, prop_cols, wealth_cols

def spatialHexBin(df):    
    fig, ax = plt.subplots(figsize=(6, 6))

    hb = ax.hexbin(
        df.geometry.x, # x cordianates
        df.geometry.y, # y cordianates
        C=df["total_energy"], # total enercy, z cord
        reduce_C_function=sum, 
        gridsize=40,
        mincnt=1,
    )

    # ▼  add an OSM/CartoDB background  ▼
    cx.add_basemap(
        ax,
        crs="EPSG:3857",
        source=cx.providers.CartoDB.Positron,   # light-grey background
        attribution=False,                      # omit tiny © text
    )

    ax.set_axis_off()
    fig.colorbar(hb, label="aggregated kWh")
    ax.set_title("High-usage homes (jittered)")
    fig.tight_layout()
    return fig
    

def dailyByPropTypePX(timeseries, prop_cols):
    daily_type = timeseries.groupby("day")[prop_cols].sum()
    mean_daily_type = daily_type.mean().sort_values(ascending=False)
    fig = px.bar(mean_daily_type, 
                 labels = {"index":"Property Type",
                        "value":"avg kWh / day"},
                 title="Daily Average by Property Type",
                 width=800, height=600)
    fig.update_layout(showlegend=False)
    figJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return figJSON

def dailyByWealth(timeseries, wealth_cols):
    daily_w = timeseries.groupby("day")[wealth_cols].sum()
    avg_w   = daily_w.mean().loc[wealth_cols]    # preserve ordering
    fig = px.bar(avg_w, 
                 labels = {"index":"Property Type",
                        "value":"avg kWh / day"},
                 title="Daily Average by Wealth Group",
                color_discrete_map={"high":"red",
                                    "medium": "orange",
                                    "low":"blue"},
                 width=800, height=600)
    fig.update_layout(showlegend=False)

    figJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return figJSON


