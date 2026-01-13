"""
This __init__.py can create global functions that can be called by any modules. Things to investigate include bootstrap js/html for global 
front-end functions, class definitions, and various "app" related functions/variables.

Makes use of bootstrap5 for responsive site design.

Secret key not currently used, required for wtforms functionality
"""
### Non-docker version for development
import json
from flask_bootstrap import Bootstrap5
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pathlib import Path
from flask import g
from .config import Config
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import event
from sqlalchemy.engine import Engine


migrate = Migrate()
db = SQLAlchemy()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_app(test_config = None):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    bootstrap = Bootstrap5(app)
    from . import digitaltwin
    app.register_blueprint(digitaltwin.bp)

    return app


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


