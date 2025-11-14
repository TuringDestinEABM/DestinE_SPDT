"""
This __init__.py can create global functions that can be called by any modules. Things to investigate include bootstrap js/html for global 
front-end functions, class definitions, and various "app" related functions/variables.

Makes use of bootstrap5 for responsive site design.

Secret key not currently used, required for wtforms functionality
"""
### Non-docker version for development
from flask_bootstrap import Bootstrap5
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pathlib import Path
from flask import g
from .config import Config

def create_app(test_config = None):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['RESULTS_DIR'] = initialise_data_db('data/geo_data/results') # should be deletable once db set up
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)



    bootstrap = Bootstrap5(app)
    from . import digitaltwin
    app.register_blueprint(digitaltwin.bp)
    
    return app

# check if data_db exists, create if not, and then add to global context
# a fudge for now, until I set up databasing properly
def initialise_data_db(extension):
    results_dir = Path(__file__).parents[0] / extension
    if not results_dir:
        results_dir.mkdir()

    return str(results_dir)
        



# '''
# Everything below here is for the deployment version
# '''

# from celery import Celery, Task
# from flask_bootstrap import Bootstrap5
# from flask import Flask

# def create_app(test_config = None):
#     app = Flask(__name__)
#     app.config.from_mapping(
#         CELERY=dict(
#             broker_url="redis://redis:6379/0",
#             result_backend="redis://redis:6379/0",
#             task_ignore_result=True,
#         ),
#     )
#     app.config.from_prefixed_env()
#     celery_init_app(app)

#     bootstrap = Bootstrap5(app)

#     from . import digitaltwin
#     app.register_blueprint(digitaltwin.bp)

#     return app



# def celery_init_app(app: Flask) -> Celery:
#     class FlaskTask(Task):
#         def __call__(self, *args: object, **kwargs: object) -> object:
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery_app = Celery(app.name, task_cls=FlaskTask)
#     celery_app.config_from_object(app.config["CELERY"])
#     celery_app.set_default()
#     app.extensions["celery"] = celery_app
#     return celery_app


