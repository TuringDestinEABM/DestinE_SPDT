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
                {"id": "20251007_example",
                  "name": "example1",
                   "Days": 5,
                   "DataSource": "epc_abm_newcastle_div100.geojson",
                  "JobSubmitted": "2025-10-07 11:26:10.938755",
                   "UserName": "Foo",
                    "OutputLocation": "C:\\Users\\notARealFilePath\\Results\\1"
                }

@pytest.fixture(scope="session")
def dummy_metadata_2():
                {"id": "20251007_example",
                  "name": "example2",
                   "Days": 100,
                   "DataSource": "epc_abm_newcastle_div50.geojson",
                  "JobSubmitted": "1998-01-01 00:00:00:1234",
                   "UserName": "Bar",
                   "OutputLocation": "C:\\Users\\notARealFilePath\\Results\\2"
                }                

# @pytest.fixture(scope="session")
# def tmp_metadata_1(tmp_path_factory, dummy_metadata_1):
#     file = tmp_path_factory.mktemp("result") / "dummy_metadata.json"
#     with open(file, 'w') as f:
#             json.dump(dummy_metadata_1,f)
#     return file

def populate_dir(parent_dir, path_name, dummy_metadata):
    fullpath = path_name + "/metadata.json"
    file = parent_dir / fullpath
    file.mkdir()
    with open(file, 'w') as f:
            json.dump(dummy_metadata, f)
            #TODO: add other dummy files (agent_timeseries.parquet, energy_timeseries.csv, and model_timeseries.parquet)

@pytest.fixture(scope="session")
def tmp_geodata(tmp_path_factory, dummy_metadata_1,dummy_metadata_2):
    results = tmp_path_factory.mktemp("geodata") / "results" # create temporary directory
    """Populate with dummy results"""
    populate_dir(results, "example1", dummy_metadata_1)
    populate_dir(results, "example2", dummy_metadata_2)
    
    return results