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
from .modelConfig import load_config
from ..library import dataManager, policies
from digitalTwin.config import Config

import tempfile, yaml

# ──────────────────────────── main ────────────────────────────────
def run(scenario, log_callback=print) -> None:

    # load gdf for only the selected agents
    epc_columns = [
    "UPRN","property_type","sap_rating","energy_cal_kwh","energy_demand_kwh",
    "floor_area_m2","property_age","main_fuel_type","main_heating_system",
    "retrofit_envelope_score","is_heatpump_candidate", "heatpump_candidate_class",
    "heating_controls","meter_type",
    "cwi_flag","swi_flag","loft_ins_flag","floor_ins_flag","glazing_flag",
    "is_electric_heating","is_gas","is_oil","is_solid_fuel","is_off_gas"
    ]
   
   # load geodatframe based on 'population' table
    gdf = dataManager.loadAndMerge(scenario.city, scenario.population_id, epc_columns=epc_columns, includeGeometry=True) 
    gdf["heatpump_candidate_class"] = gdf["heatpump_candidate_class"].astype(str).replace({'None': None, 'nan': None, 'True': 'true', 'False': 'false'}) # convert from bool to str for compatability with agent.py

    # geodataframe  

    log_callback('data loaded')
    print('-----------')
    print(gdf.head())
    print('-----------')


    climate_path = Config.CLIMATE_DATA

    # create config file
    log_callback('Creating config file from policy selection')
    # createPolicyConfig(gdf, scenario.policy_id, log_callback=log_callback)

    # # update gdf based on policies
    # gdf_updated = switchToHeatpump(gdf, scenario.policy_id, log_callback=log_callback)

    model = EnergyModel(gdf=gdf,
                        climate_parquet= climate_path,
                        climate_start=scenario.start_day, # to do make changeable
                        local_tz="Europe/London",
                        collect_agent_level=True,   # keep per-household traces
                        agent_collect_every=scenario.record_every#, # once per day
                        #config_path=cfg      # either created from policy choice
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

# def switchToHeatpump(gdf, policy_id, log_callback=print):

#     # policy_choices = dataManager.findDBData('PolicyChoices', policy_id)
#     policy_data = policies.getPolicy(f'policy_choices: {policy_choices}')
#     print(f'policy_choices: {policy_choices}')

#     return gdf



def createPolicyConfig(gdf, policy_id, log_callback=print):
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as tmp:
        policy_cfg = tmp.name

        policy_choices = dataManager.findDBData('PolicyChoices', policy_id)
        print(f'policy_choices: {policy_choices}')
        policy_data = policies.getPolicy(policy_id)
        print(f'policy_data: {policy_data}')
        # log_callback(policy_data)

         # create metadata
        if policy_choices.description:
            meta = {"name": policy_choices.policy_name,
                    "date": str(policy_choices.timestamp),
                    "notes": policy_choices.description
                    }
        else:
            meta = {"name": policy_choices.policy_name,
                    "date": str(policy_choices.timestamp)
                    }
            
        char_map =[{'policy':'Ward', 'cfg':'ward_code', 'policy_list':'wards'},
                   {'policy':'Income', 'cfg':'hh_income_band', 'policy_list':'income_types'},
                   {'policy':'Property', 'cfg':'property_type', 'policy_list':'property_types'},
                   {'policy':'Schedule', 'cfg':'schedule_type', 'policy_list':'schedule_types'}]
        mapping_lookup = {
            item['policy']: {'cfg': item['cfg'], 'list': item['policy_list']} 
                for item in char_map
        } # lookup dictionary

        yaml_data = {}

        char_types = {
            'qualifying_characteristics': {
                'prefix': 'qualifying'
            },
            'disqualifying_characteristics': {
                'prefix': 'disqualifying'
            }
        }

        for rule in policy_data['rules']:
            # Check both qualifying and disqualifying lists
            for attr_key, config in char_types.items():
                
                # Check if the rule has this attribute and it's not empty
                characteristics = getattr(rule, attr_key, None)
                
                if characteristics:
                    # Name: e.g., 'qualifying_2' or 'disqualifying_2'
                    block_name = f"{config['prefix']}_{rule.id}"
                    
                    # Initialize structure
                    yaml_data[block_name] = {
                        "eligibility": {}
                    }
                    
                    # Map each characteristic to its cfg key and data list
                    for char_name in characteristics:
                        map_info = mapping_lookup.get(char_name)
                        
                        if map_info:
                            cfg_key = map_info['cfg']
                            list_attr = map_info['list']
                            
                            # Pull the data (e.g., the list of wards) from the rule
                            data_list = list(getattr(rule, list_attr, []))
                            
                            # Assign to the eligibility section
                            yaml_data[block_name]["eligibility"][cfg_key] = data_list

#         # 2. Print to command line for verification
#         print("--- GENERATED YAML CONFIG ---")
#         print(yaml.dump(yaml_data, sort_keys=False, default_flow_style=None))
#         print("-----------------------------")
                                    
                            

       

       
#         yaml.safe_dump({
#             "meta": meta,
#         })
#     print(f"Policy override config: {elderly_cfg}")