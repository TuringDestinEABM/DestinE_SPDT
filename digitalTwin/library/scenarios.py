'''Scripts which deal with running the simulations, as well as storing the data and metadata. Takes results from CreateScenarioForm, creates a folder and metadata dict and runs the ABM model.

This functionality to be replaced with databasing in the deployment version'''

from digitalTwin.modelling import energyABM
import datetime, json
from pathlib import Path
import random
from digitalTwin import db
from digitalTwin.models import models
import sqlalchemy as sa
import sqlalchemy.orm as so

'''main script'''
def createNewScenario(form):
    days = form.Days.data
    scenario_name = form.ScenarioName.data

    scenario = models.Scenario(scenario_name = scenario_name,
                days = days,
                city = form.City.data,
                subset = form.Subset.data,
                user_name = getUserName(),
                timestamp = datetime.datetime.now(datetime.timezone.utc),
                init_lat = setInitLatLon(form.City.data)[0],
                init_lon = setInitLatLon(form.City.data)[1])
                
    
    db.session.add(scenario)
    db.session.commit()
    
    return scenario_name

def run(scenario_name):
    scenario = db.first_or_404(sa.select(models.Scenario).where(models.Scenario.scenario_name == scenario_name))
    model, records = energyABM.run(scenario) # run the model
    print('model run')
    # pass the energy time series to the database
    for entry in records:
        energy_ts = models.EnergyTimeSeries(scenario_id = scenario.id,
                                            step = entry["step"],
                                            hour = entry["hour"],
                                            day = entry["day"],
                                            total_energy = entry["total_energy"],
                                            average_energy = entry["avg_energy"]
                                            )
        db.session.add(energy_ts)
    db.session.commit()
    print('energy_ts saved')
    # pass the model time series to the database
    model_df = model.datacollector.get_model_vars_dataframe() # method for mesa model (dataframe seems to be only option)
    model_dict = model_df.to_dict('records') # convert to list for quicker iteration
    for row in model_dict:
        model_ts = models.ModelTimeSeries(scenario_id = scenario.id,
                                        mid_terraced_house = row["mid-terraced house"],
                                        semi_detached_house = row["semi-detached house"],
                                        flats_small = row["small block of flats/dwelling converted in to flats"],
                                        flats_large = row["large block of flats"],
                                        flats_block = row["block of flats"],
                                        end_terrace_house = row["end-terraced house"],
                                        detached_house = row["detached house"],
                                        flat_mixed_use = row["flat in mixed use building"],
                                        high = row["high"],
                                        medium = row["medium"],
                                        low = row["low"],
                                        total_energy = row["total_energy"],
                                        cumulative_energy = row["cumulative_energy"])
        db.session.add(model_ts)
    db.session.commit()
    print('model_ts saved')

   # pass the agent time series to the database
    agent_df = model.datacollector.get_agent_vars_dataframe() # method for mesa model (dataframe seems to be only option)
    agent_dict = [agent_df.columns.tolist()] + agent_df.reset_index().values.tolist() # convert to list for quicker iteration
    for row in agent_dict:
        if row[0] != 'energy': # first row is column headings, skip this
            agent_ts = models.AgentTimeSeries(scenario_id = scenario.id,
                                            energy = row[2],
                                            energy_consumption = row[3],
                                            step = row[0],
                                            Agent_id = row[1]
                                            )
            db.session.add(agent_ts)
    db.session.commit()
    print('agent_ts saved')

    # return gdf


'''Get the user's login'''
def getUserName():
    # TODO: revisit when login functionality sorted
    username = "<username>"
    return username

def setInitLatLon(city):
    print(city)
    if city == 'newcastle':
        lon = -1.65260
        lat = 55.01802

    elif city == 'sunderland':
        lon = -1.401567
        lat = 54.901682
    
    else:
        lon = 0.0
        lat = 0.0

    return [lon, lat]



# def dummyRunSim(days):
#     results = []
#     for day in range(days):
#         results.append(random.randint(0,9))

#     timesteps = list(range(days))
#     data = {'timesteps': timesteps,
#             'results': results}

#     return data