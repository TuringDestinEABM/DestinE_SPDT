#!/usr/bin/env python
"""
run.py – batch executor for the Household-Energy ABM
===================================================

This script:

1. reads a GeoJSON of building polygons,
2. instantiates `EnergyModel`,
3. runs it for `days × 24` hourly steps,
4. writes three data artefacts to `outdir`:

   ┌───────────────────────────────┐
   │ energy_timeseries.csv         │  – per-hour total & average kWh
   │ model_timeseries.parquet      │  – DataCollector (model-level vars)
   │ agent_timeseries.parquet      │  – DataCollector (agent-level vars)
   └───────────────────────────────┘

"""

from __future__ import annotations

from pathlib import Path

# import cloudpickle as pickle #Not currently used
import geopandas as gpd
import pandas as pd

from .model import EnergyModel

# ──────────────────────────── main ────────────────────────────────
def run(sourceData, days, outdir) -> None:

    # 1 ─ load geometry + build model ---------------------------------
    # dataPath = Path(__file__).parents[1] /"data/ncc_data" / sourceData
    dataPath = Path(__file__).parents[1] /"data/synthetic_data" / sourceData
    gdf   = gpd.read_file(dataPath)
    # return(gdf)
    model = EnergyModel(gdf)

    # 2 ─ run simulation ----------------------------------------------
    steps   = days * 24 #TODO: make this user input
    records = []                                    # per-hour summary rows

    for step in range(steps):
        model.step()

        tot = sum(h.energy_consumption for h in model.household_agents)
        records.append(
            dict(
                step=step,
                hour=step % 24,
                day=step // 24,
                total_energy=tot,
                avg_energy=tot / len(model.household_agents),
            )
        )

    # 3 ─ write outputs ----------------------------------------------
    # 3-a CSV with hourly totals
    df = pd.DataFrame(records)
    csv_path = outdir / "energy_timeseries.csv"
    df.to_csv(csv_path, index=False)

    # 3-b Parquet tables from Mesa’s DataCollector
    model_parquet  = outdir / "model_timeseries.parquet"
    agent_parquet  = outdir / "agent_timeseries.parquet"
    model.datacollector.get_model_vars_dataframe().to_parquet(model_parquet)
    model.datacollector.get_agent_vars_dataframe().to_parquet(agent_parquet)

    # # 3-c Optional: pickle entire model for replay
    # pickle_path = outdir / "energy_model.pkl"
    # with open(pickle_path, "wb") as fh:
    #     pickle.dump(model, fh)



#Defining the place to save data, will change when I sort databasing
