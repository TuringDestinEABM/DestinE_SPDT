import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey'
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    POSTS_PER_PAGE = 10

    INITIAL_DATA_LOC = os.path.join(basedir, "data", "initial_data")
    CLIMATE_DATA = os.path.join(basedir, "data", "ncc_2t_timeseries_2010_2039.parquet")
    WARD_CODES = os.path.join(basedir, "data", "Wards_(May_2025)_Names_and_Codes_in_the_UK.geojson")

"""Configuration loader for household_energy.

Provides a simple way to externalize model parameters into a YAML/JSON file.
Defaults live in ``config_defaults.yaml``; users can pass ``config_path`` to override.
"""
