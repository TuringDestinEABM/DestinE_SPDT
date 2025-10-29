import pytest
from digitalTwin import create_app
import json

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope="session")
def dummy_metadata_1():
            data = {"id": "20251007_example1",
                  "name": "example1",
                   "Days": 5,
                   "DataSource": "epc_abm_newcastle_div100.geojson",
                  "JobSubmitted": "2025-10-07 11:26:10.938755",
                   "UserName": "Foo",
                    "OutputLocation": "C:\\Users\\notARealFilePath\\Results\\1"
                }
            return data

@pytest.fixture(scope="session")
def dummy_metadata_2():
            data = {"id": "20251007_example2",
                  "name": "example2",
                   "Days": 100,
                   "DataSource": "epc_abm_newcastle_div50.geojson",
                  "JobSubmitted": "1998-01-01 00:00:00:1234",
                   "UserName": "Bar",
                   "OutputLocation": "C:\\Users\\notARealFilePath\\Results\\2"
                }      
            return data          

def populate_dir(parent_dir, path_name, dummy_metadata):
    """Populates parent directory with the expected folder and file structure."""
    example = parent_dir / path_name
    example.mkdir()
    file = example / "metadata.json"
    with open(file, 'x') as f:
            json.dump(dummy_metadata, f)
#TODO: add other dummy files (agent_timeseries.parquet, energy_timeseries.csv, and model_timeseries.parquet)

@pytest.fixture(scope="session")
def tmp_geodata(tmp_path_factory, dummy_metadata_1,dummy_metadata_2):
    """Creates and populates a temporary folder structure for tests dependent on 'data/geodata/'.
    Temporary folder structure:
    └───tmp_geodata/                                   
         └───results/
            ├───example1/
            │   └───metadata.json
            └───example2/
                └───metadata.json  
    """
    basedir = tmp_path_factory.mktemp("tmp_geodata") 
    results = basedir / "results" # create temporary directory
    results.mkdir()
    """Populate with dummy results""" 
    # there's probably a cleaner way to do this with parameterize but this works for now
    populate_dir(results, "example1", dummy_metadata_1 )
    populate_dir(results, "example2", dummy_metadata_2 )    
    return basedir