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
from ..library import dataManager
from digitalTwin.config import Config

# ──────────────────────────── main ────────────────────────────────
def run(scenario, log_callback=print) -> None:

    fields = [
    "UPRN","property_type","sap_rating","energy_cal_kwh","energy_demand_kwh",
    "floor_area_m2","property_age","main_fuel_type","main_heating_system",
    "retrofit_envelope_score",
    "heating_controls","meter_type",
    "cwi_flag","swi_flag","loft_ins_flag","floor_ins_flag","glazing_flag",
    "is_electric_heating","is_gas","is_oil","is_solid_fuel","is_off_gas"
    ]
   
    gdf   = dataManager.loadGeoJSONDB(scenario.city, scenario.population_id, scenario.subset, fields) # geodataframe  
    log_callback('data loaded')
    climate_path = Config.CLIMATE_DATA

    model = EnergyModel(gdf=gdf,
                        climate_parquet= climate_path,
                        climate_start="2022-07-15", # to do make changeable
                        local_tz="Europe/London",
                        collect_agent_level=True,   # keep per-household traces
                        agent_collect_every=24      # once per day
                    )
    log_callback('model created')

    # 2 ─ run simulation ----------------------------------------------
    steps   = scenario.days * 24 #TODO: make this user input
    records = []                                    # per-hour summary rows
    log_callback(f'Running model. {steps} steps to go...')
    for step in range(steps):

        # call back every 10 steps
        if step % 10 ==0:
            log_callback(f'Running model. {step} out of {steps}.')

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
    
    return model, records

