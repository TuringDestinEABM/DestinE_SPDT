"""
This __init__.py can create global functions that can be called by any modules. Things to investigate include bootstrap js/html for global 
front-end functions, class definitions, and various "app" related functions/variables.
"""
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

### Non-docker version for development
from flask_bootstrap import Bootstrap5
from flask import Flask

def create_app(test_config = None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    bootstrap = Bootstrap5(app)

    from . import digitaltwin
    app.register_blueprint(digitaltwin.bp)

    return app
