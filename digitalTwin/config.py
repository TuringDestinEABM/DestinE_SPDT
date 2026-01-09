import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey'
    
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_BINDS = {"gis": "sqlite:///gis.db"}
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    POSTS_PER_PAGE = 3

    INITIAL_DATA_LOC = os.path.join(basedir, "data", "initial_data", "epc_abm_data.geojson")
