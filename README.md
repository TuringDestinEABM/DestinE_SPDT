# DestinE_SPDT
This is the public relase of the development version of the Scenario Planning Digital Twin web app for the [Earth observation-informed agent-based models for scenario planning digital twins](https://www.turing.ac.uk/research/research-projects/earth-observation-informed-agent-based-models-scenario-planning-digital) project. 

> [!WARNING]
> This is a pre-release development version of the software and does not include all of the planned functionality of the final release.


## Description
The aim of this project is to pioneer the development of a scenario-planning digital twin (SPDT) for the European Space Agency, creating a prototype multi-level agent-based model (MABM) that will simulate energy consumption for residential heating energy use at the household level. For this demonstrator, we use synthetic datasets built based on the UK cities of Newcastle and Sunderland.

This web app is built using flask to give users an accessible way to run the MABM and to explore the results.

## Directory layout

```
├───digitalTwin/                                   # Main folder
│   ├───data/
│   │   ├───geo_data/                              # Geographic data           
│   │   │   └───results/                           # Results from each MABM run
│   │   └───synthetic_data/                        # Synthetic source data
|   |   
│   ├───library/                                  # Python scripts for the flask web app
│   │   ├───forms.py                              # wtforms webforms
│   │   ├───getData.py                            # Scripts for collecting different file types into the web app
│   │   ├───plotting.py                           # Plotting and GIS
│   │   └───model.py                              # Call the MABM and saves the data
|   |   
│   ├───modelling/
│   │   ├───agent.py                              # HouseholdAgent & PersonAgent
│   │   ├───analyze.py                            # Post-run plots & maps
│   │   ├───energyABM.py                          # Main ABM script
│   │   └───model.py                              # EnergyModel (ABM core)
|   |   
│   ├───routes/                                   # Flask routes for web app pages
|   |   
│   ├───static/                                   # Static files
│   │   └───img/                                  # Images
│   │       ├───logos/                            # Logos
│   │       └───map_icons/                        # map icons
|   |   
│   ├───templates/                                # HTML templates for the web app pages
|   | 
│   ├───__init.py__                               # Initialisation
|   | 
│   └───digitalTwin.py                            # Main flask script
├───README.md
└───requirements.txt


```

## Initial set up (windows)

1. Clone this repo to your machine, using one of the options from the green "code" button above
[(more information)](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
or use

```git clone https://github.com/TuringDestinEABM/DestinE_SPDT```

2. Unzip the two folders from `ZippedData/`. Move the contents of `results.zip` into `digitalTwin/data/geodata/results/` and the contents of `synthetic_data.zip` into `digitalTwin/data/synthetic_data`. The resulting local file structure should be this
```
├───digitalTwin/                                  
│   └───data/
│       ├───geo_data/                                        
│       │   ├───results/
|       │   │   ├───20251007_example/
|       │   │   │   ├───agent_timeseries.parquet
|       │   │   │   ├───energy_timeseries.csv
|       │   │   │   ├───metadata.json
|       │   │   │   └───model_timeseries.parquet
|       │   │   └───20251007_example3/
|       │   │       ├───agent_timeseries.parquet
|       │   │       ├───energy_timeseries.csv
|       │   │       ├───metadata.json
|       │   │       └───model_timeseries.parquet
|       │   └───.gitkeep 
│       └───synthetic_data/  
|           ├───.gitkeep  
|           ├───epc_abm_newcastle_div10.geojson
|           ├───epc_abm_newcastle_div50.geojson
|           ├───epc_abm_newcastle_div100.geojson
|           ├───epc_abm_newcastle.geojson
|           ├───epc_abm_sunderland_div10.geojson
|           ├───epc_abm_sunderland_div50.geojson
|           ├───epc_abm_sunderland_div100.geojson
|           └───epc_abm_sunderland.geojson
...
```


3. Create a virtual environment in the same folder as the code

```python -m venv .env ```


```.env\Scripts\activate ```

4. Install dependencies

```python.exe -m pip install --upgrade pip```
 
```pip install -r requirements.txt```


5. Run flask

```set FLASK_APP=digitalTwin.py```

```flask run```

## Standard usage
After your first set up, you can run the code by first activating the virtual environment

```.env\Scripts\activate ```

and then running flask

```set FLASK_APP=digitalTwin.py```

```flask run```.

On running flask, you should be presented with a hyperlink to the local port where the SPDT is running. This link should open in your browser. If it doesn't, try copying and pasting it address bar of your browser.

### Home page
On opening the SPDT, you should be redircted to the home page. You can access this page at any time by clicking the `Home` button in the navigation bar.

From the home page, you can choose to `Create` a new Scenario or `Load from Template` [currently inactive]. 

You also have a list of available reports, including the examples included in this repository and any which you have previously created. These reports describe the output of the MABM. The table includes the user created name of the report, the date it was created, the user name of the person who created the report, and a link to view the summary report.

### New Scenario
Clicking the `Create` button should take you to the new scenario page. From here you can design a simulation using the following options:
| Option                    | Description |
|---------------------------|-------------|
|`Scenario Name` |A user generated name for the scenario|
| `Days` |Number of days to run the scenario over|
|`Data Source`| Which data set to use to populate the MABM (for more information see **Datasets**, below)|

More options will be included in future versions of the app.

Clicking `Run` will submit the web form and run the simulation. This will create a new folder for the simulation results in `data/geodata/results` which will contain the following after the simulation completes:
| File                       | Description |
|---------------------------|-------------|
| `agent_timeseries.parquet`| Agent-level DataCollector (if not `--no-agent-level`) |
|`energy_timeseries.csv`   | Simple per-hour totals & average (compat CSV) |
|`metadata.json`|Metadata describing the report|
| `model_timeseries.parquet`| Model-level DataCollector (indexed by UTC hour) |

>[!WARNING] 
> Running the MABM can take a long time. Refreshing the webpage will cancel the run but will not remove the results folder

Once the model has finished running, you will be automatically redirected to the **Success** page, which gives you the option to view the results or return home

### Summary report
This page gives you a summary of the simulation results. At the top is a table containing the summary information about the report (ID, Days, Date submitted, and Username). There is also a link to open the **detailed timeline**.

Below this are three graphs, each in their own tabs.
| Graph                      | Description |
|---------------------------|-------------|
|Daily Average by Property Type|Bar chart showing the average daily usage in kilo watt hours for each type of property |
|Average by Wealth Group|Bar chart showing the average daily usage of members of each the 'high', 'medium' and 'low' wealth groups|
|`Heatmap`|A heat map showing the average demand for each hour and day|

### Detailed timeline
This opens a new page with an interactive map showing the energy use of each property at each time step (hour). The slider at the top left allows you to scroll through the timesteps. Each property is denoted by a circle with its colour corresponding to its energy use at the given time step, as described by the colour bar in the top left.

Clicking on a property will bring up a text box containing information about the property, and its energy consumption during that time step.

## Datasets
> [!CAUTION]
> The main datasets are large and this development version of the web app does not include task queueing or databasing. Running the MABM using the full dataset for many days is slow and can crash your browser; instead use one of the reduced datasets.

> [!WARNING]
> This documentation is incomplete and will be updated in future releases.

We include two synthetic datasets `epc_abm_newcastle.geojson` and `epc_abm_sunderland.geojson`, representing properties in Newcastle and Sunderland respectively. These datasets are derived from the open [Energy Performance aof Buildings Dataset](https://epc.opendatacommunities.org/)

The datasets are `geojson` feature collections containing the following properties for each feature:
- `UPRN` [Unique Property Reference Number](https://www.geoplace.co.uk/addresses-streets/location-data/the-uprn) of the locastion
- `lsoa_code` [Lower Layer Super Output Area](https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups/namesandcodeslistings/namesandcodesforsuperoutputareassoa) code for the property
- `local_authority` Corresponding local authority code
- `ward_code` Code for the ward corresponding to the feature
- `habitable_rooms` Number of habitable rooms
- `sap_rating` [Standard Assessment Procedure](https://www.gov.uk/guidance/standard-assessment-procedure) rating of the energy performance
- `floor_area_m2` Floor area of the property in metres squared
- `property_type` Description of the property type
- `main_fuel_type` The type of fuel used to power the central heating 
- `main_heating_system` Type of main heating controls
- `sap_band_ord` ??
- `retrofit_envelope_score`: ??
- `is_off_gas` logical corresponding to whether the propert is (1) or isn't (0) off gas
- `energy_demand_kwh` ??
- `factor` ??
- `energy_cal_kwh` ??
- `heating_controls` Type of main heating controls
- `meter_type` ??
- `cwi_flag` ??
- `swi_flag` ??
- `loft_ins_flag` ??
- `floor_ins_flag` ??
- `glazing_flag` ??
- `is_electric_heating` ??
- `is_gas` ??
- `is_solid_fuel` ??
- `epc_lodgement_date_year` Year in which the data was lodged on the Energy Performance of Buildings Register
- `geometry` Coordinates of the point representing the property ([lon., lat.])


We also include reduced order datasets of each of these (`..._div10.geojson`, `..._div50.geojson` and `..._div100.geojson`), which respectively include 10%, 2% and 1% of the points of the originals, with the same distribution.
