# DestinE_SPDT
This is the public relase of the development version of the Scenario Planning Digital Twin web app for the [Earth observation-informed agent-based models for scenario planning digital twins](https://www.turing.ac.uk/research/research-projects/earth-observation-informed-agent-based-models-scenario-planning-digital) project. 


## Description
The aim of this project is to pioneer the development of a scenario-planning digital twin (SPDT) for the European Space Agency, creating a prototype multi-level agent-based model (MABM) that will simulate energy consumption for residential heating energy use at the household level. For this demonstrator, we use synthetic datasets built based on the UK cities of Newcastle and Sunderland.

This web app is built using flask to give users an accessible way to run the MABM and to explore the results.


## Initial set up (windows)

1. Clone this repo to your machine, using one of the options from the green "code" button above [(more information)](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) or use `git clone https://github.com/TuringDestinEABM/DestinE_SPDT`

2. Unzip `data.zip` into the `digitalTwin` folder. This data is required for the app to function. The resulting file structure should be as below. If unsure, you can check the file paths against those in `config.py` 
```
├───digitalTwin/   
...                               
│   └───data/
│       ├───initial_data/                                        
│       │   ├───epc_abm_newcastle.geojson
│       │   ├───epc_abm_sunderland.geojson
│       │   └───hidp_uprn_matches_tiered.csv
│       ├───ncc_2t_timeseries_2010_2039.parquet
│       └───Wards_(May_2025)_Names_and_Codes_in_the_UK.geojson
...
```


3. Create a virtual environment in the same folder as the code:

    ```python -m venv .env ```


    ```.env\Scripts\activate ```

4. Install dependencies:

    ```python.exe -m pip install --upgrade pip```
 
    ```pip install -r requirements.txt```

5. Create the database:
    ```set FLASK_APP=digitalTwin.py```

    ```flask db init```

    ```flask db migrate -m "first migration"```

    ```flask db upgrade```
6. Upload the initial data to the database
    ```py populateDB.py```

7. Run the app

    ```flask run```

    After a few seconds you should see this message:
    ```
    * Serving Flask app 'digitalTwin.py'
    * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on http://127.0.0.1:5000
    ```
    Click the hyperlink to open the webapp in your browser

## Standard usage
After your first set up, you can run the code by first activating the virtual environment

```.env\Scripts\activate ```

and then running flask

```set FLASK_APP=digitalTwin.py```

```flask run```.

## Features
### Home page
On opening the SPDT, you should be redirected to the home page. You can access this page at any time by clicking the `Home` button in the navigation bar.

From the home page, you can choose to `Create new scenario`  or `Create policy selection`. On first usage, start with the policy selection, as this is required before a new scenario can be created

You also have a list of available reports, if any are in the database. These reports describe the output of the MABM. The table includes the user created name of the report, the date it was created, the user name of the person who created the report, and a link to view the summary report.

### Create New Policy
This page allows you to create a policy selection. This will be used when simulating a scenario to decide which agents get converted to a heatpump. Policy selections consist of multiople rules, as well as some general parameters.

Once you have created a policy selection, selecting `Submit` will save it, allowing it to be used to create scenarios.

#### Policy details
This tab is used to define some general information about your policy.

| Option                    | Description |
|---------------------------|-------------|
|`Policy Name` |A user generated name for the policy selection|
|`Description` |A user generated name text description (optional)|
|`Adoption rate (%)` |Percentage of eligible agents who will adopt the technology|
|`Candidates` |Describes how easy a heatpump is to install. By default only `priority` and `possible` are selected|

#### Add Rule to Policy
This tab allows you to define the rules which will be applied.

Assuming an adoption rate of 100%, if an agent is eligible for a heatpump according to the `Candidates` selection, then at simulation time they will be converted to a heatpump **if** they match *at least one* of the `Qualifying` criteria **and** they  match *none* of the `Disqualifying` criteria for *at least one* of the rules.

Rules stack sequentially, in the order they are added to the policy selection. 

#### Staged Rules
This tab shows you a summary of the rules you have added to your policy selection. You can delete any individual rules by clicking `delete` or all rules by clicking `clear all`.

### New Scenario
To create a new scenario, click the link on the home page. You will be guided through the set up through a series of four webpages. At the end you can choose to save the scenario or run it immediately.

>[!WARNING] 
> Leaving the process before the scenario is saved will result in all progress being lost

#### Set up
Here you select some general parameters for your scenario.
| Option                    | Description |
|---------------------------|-------------|
|`Scenario Name` |A user generated name for the scenario|
|`Description` |A user generated name text description (optional)|
|`City` |Which city to simulate|
| `Technology` |Which technology to simulate|
| `Start date` |The first day of the simulation|
| `End date` |The final day of the simulation|
|`Record every (hrs)`| How often the simulation will save a full record (choosing higher values improves performance and decreases memory required for larger simulations)|

Once you fill these in, click `Continue` will take you to `New Scenario: Agents`.

#### Agents
This page allows you to select which agents will be simulated in your scenario. 

| Option                    | Description |
|---------------------------|-------------|
|`Wards` |The city's council wards, based on 2025 boundaries|
|`Property types` |The classes of building|
|`Income` |The income quintiles (20%) of the building occupants|
|`Schedule` |Classes of schedule for the building occupants|

Clicking `Continue` will take you to `New Scenario: Select Policy`.

#### Select Policy
This page allows you to select a policy selection from those previously generated. 

Clicking `View` will open up a summary for inspection. 

Clicking `Select` will take you to `New Scenario: Review Scenario`.

#### Review Scenario
This page shows you a summary of your scenario. You can click edit on any of the sections to return to that page and make edits.

Clicking `Save` save the scenario and take you to a landing page. 

Clicking `Run` will save the scenario and then run it immediately.

### Run scenario
You can run scenarios immediately on creation or by clicking `run` next to the scenario on the homepage.

On running you will be taken to a loading screen, which will update you on progress while the scenario runs in the background.

>[!WARNING] 
> LExiting this page before the scenario has finished running will end the simulation and prevent the results from being saved

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
This opens a new page with an interactive map showing the energy use of each property at each time step. The slider at the top left allows you to scroll through the hours, while the arrows allow you to select days. Each property is denoted by a circle with its colour corresponding to its energy use at the given time step, as described by the colour bar in the top left.

Clicking on a property will bring up a text box containing information about the property, and its energy consumption during that time step.

### Manage data
This page acts as a front end on the database.

#### Scenarios
This tab shows the scenarios, as well as which simulation data (if any) is saved for rach.

Clicking `Clear` will delete any results data associated with a scenario, allowing it to be run again.

Clicking `Delete` will delete the scenario, along with any results associated with it

#### Policy Choices
This tab shows the policy choices in the database.

Clicking `Delete` will delete the policy choice.

#### Population
This tab shows the agents associated with each scenario.

#### Source Data
This tab shows the synthetic data set.

## Datasets

### epc datasets

We include two synthetic datasets `epc_abm_newcastle.geojson` and `epc_abm_sunderland.geojson`, representing properties in Newcastle and Sunderland respectively. These datasets are derived from the open [Energy Performance af Buildings Dataset](https://epc.opendatacommunities.org/)

The datasets are `geojson` feature collections containing the following properties for each feature:
- `UPRN` [Unique Property Reference Number](https://www.geoplace.co.uk/addresses-streets/location-data/the-uprn) of the location
- `lsoa_code` [Lower Layer Super Output Area](https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups/namesandcodeslistings/namesandcodesforsuperoutputareassoa) code for the property
- `local_authority` Corresponding local authority code
- `ward_code` Code for the ward corresponding to the feature
- `habitable_rooms` Number of habitable rooms
- `sap_rating` [Standard Assessment Procedure](https://www.gov.uk/guidance/standard-assessment-procedure) rating of the energy performance
- `floor_area_m2` Floor area of the property in metres squared
- `property_type` Description of the property type
- `main_fuel_type` The type of fuel used to power the central heating 
- `main_heating_system` Type of main heating controls
- `sap_band_ord` 
- `retrofit_envelope_score`: 
- `is_off_gas` logical corresponding to whether the property is (1) or isn't (0) off gas
- `energy_demand_kwh` 
- `factor` 
- `energy_cal_kwh` 
- `heating_controls` Type of main heating controls
- `meter_type` 
- `cwi_flag` 
- `swi_flag` 
- `loft_ins_flag` 
- `floor_ins_flag` 
- `glazing_flag` 
- `is_electric_heating` 
- `is_gas` 
- `is_solid_fuel`
- `epc_lodgement_date_year` Year in which the data was lodged on the Energy Performance of Buildings Register
- `geometry` Coordinates of the point representing the property ([lon., lat.])

### hidp data
`hidp_uprn_matches_tiered.csv` contains additional household data for Newcastle, based on the [UK household longitudinal survey](https://www.understandingsociety.ac.uk/documentation/mainstage/variables/hidp/):

- `uprn_chr` Unique Property Reference Number of the location
- `lsoa_code` Lower Layer Super Output Area code for the property
- `dwelling bucket` Type of property
- `tenure` Ownership/tenure status of the property
- `size_band` Size band
- `hidp` Household identifier
- `hh_n_people` Number of occupants
- `hh_children` Children (True/False)
- `hh_income` Household monthly income (GBP)
- `hh_income_band` Household income quintile
- `schedule_type` Household schedule
- `hh_edu_detail` Highest level of education

### Temperature
`ncc_2t_timeseries_2010_2039.parquet`  is  an hourly temperature parquet with a UTC time axis and a spatial grid of points covering the study area. Data are retrieved from the [Destination-Earth](https://destination-earth.eu/) API platform (climate-dt dataset, 2 m above-surface temperature, ERA5-Land) for a polygon drawn around the local authority boundary plus a configurable buffer. Current deployment covers 2020–2039 for the study areas.

### Wards
`Wards_(May_2025)_Names_and_Codes_in_the_UK.geojson` is a local copy of the [Office for National Statistics ward administrative names and codes 2025 release](https://geoportal.statistics.gov.uk/datasets/wards-may-2025-names-and-codes-in-the-uk/about).
