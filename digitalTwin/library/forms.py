''' Forms to enable user submitted information to flask. Default method for selecting options'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from digitalTwin import db
from digitalTwin.models import models
import sqlalchemy as sa
import string

# Form for createScenario.py route
# class CreateScenarioFormLEGACY(FlaskForm):
#     ScenarioName = StringField('Scenario Name', validators=[DataRequired(), Length(1,32)])
#     Days = IntegerField('Days', validators=[DataRequired(), NumberRange(1, 9125)] )
#     # DataSource = SelectField('Data Source', choices = ["ncc_neighborhood.geojson", "ncc_neighborhood_10k.geojson"],validators=[DataRequired()])
#     DataSource = SelectField('Data Source', choices = ["epc_abm_newcastle.geojson",
#                                                        "epc_abm_newcastle_div10.geojson",
#                                                        "epc_abm_newcastle_div50.geojson",
#                                                        "epc_abm_newcastle_div100.geojson",
#                                                        "epc_abm_sunderland.geojson",
#                                                        "epc_abm_sunderland_div10.geojson",
#                                                        "epc_abm_sunderland_div50.geojson",
#                                                        "epc_abm_sunderland_div100.geojson",
#                                                        ],
#                                                         validators=[DataRequired()])
    
#     def validate_ScenarioName(self, ScenarioName):
#         # check valid characters (needs to work in a url)
#         valid_chars = list(string.ascii_letters) + list(string.digits) + ['-', '_']
#         for s in str(ScenarioName.data):
#             if s not in valid_chars:
#                 raise ValidationError('Please only use alphanumeric characters, hyphens or underscores (a-z, A-Z, 0-9, -, _).')
#         # check uniqueness
#         scenario = db.session.scalar(sa.select(models.Scenario).where(
#             models.Scenario.scenario_name == ScenarioName.data))
#         if scenario is not None:
#             raise ValidationError('This scenario name is already in use. Please use a unique value.')
       
                
#     Submit = SubmitField('Run')

class CreateScenarioForm(FlaskForm):
    ScenarioName = StringField('Scenario Name', validators=[DataRequired(), Length(1,32)])
    Days = IntegerField('Days', validators=[DataRequired(), NumberRange(1, 9125)] )
    # DataSource = SelectField('Data Source', choices = ["ncc_neighborhood.geojson", "ncc_neighborhood_10k.geojson"],validators=[DataRequired()])
    City = SelectField('Data Source', choices = ["newcastle",
                                                        "sunderland",
                                                        ],
                                                        validators=[DataRequired()])
    Subset = IntegerField('Subset (%)', validators=[DataRequired(), NumberRange(1, 100)], default=100 )

    def validate_ScenarioName(self, ScenarioName):
        # check valid characters (needs to work in a url)
        valid_chars = list(string.ascii_letters) + list(string.digits) + ['-', '_']
        for s in str(ScenarioName.data):
            if s not in valid_chars:
                raise ValidationError('Please only use alphanumeric characters, hyphens or underscores (a-z, A-Z, 0-9, -, _).')
        # check uniqueness
        scenario = db.session.scalar(sa.select(models.Scenario).where(
            models.Scenario.scenario_name == ScenarioName.data))
        if scenario is not None:
            raise ValidationError('This scenario name is already in use. Please use a unique value.')
        
                
    Submit = SubmitField('Save')