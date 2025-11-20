''' Forms to enable user submitted information to flask. Default method for selecting options'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from digitalTwin import db
from digitalTwin.models import models
import sqlalchemy as sa

# Form for createScenario.py route
class CreateScenarioForm(FlaskForm):
    ScenarioName = StringField('Scenario Name', validators=[DataRequired(), Length(1,32)])
    Days = IntegerField('Days', validators=[DataRequired(), NumberRange(1, 9125)] )
    # DataSource = SelectField('Data Source', choices = ["ncc_neighborhood.geojson", "ncc_neighborhood_10k.geojson"],validators=[DataRequired()])
    DataSource = SelectField('Data Source', choices = ["epc_abm_newcastle.geojson",
                                                       "epc_abm_newcastle_div10.geojson",
                                                       "epc_abm_newcastle_div50.geojson",
                                                       "epc_abm_newcastle_div100.geojson",
                                                       "epc_abm_sunderland.geojson",
                                                       "epc_abm_sunderland_div10.geojson",
                                                       "epc_abm_sunderland_div50.geojson",
                                                       "epc_abm_sunderland_div100.geojson",
                                                       ],
                                                        validators=[DataRequired()])
    
    def validate_ScenarioName(self, ScenarioName):
        scenario = db.session.scalar(sa.select(models.Scenario).where(
            models.Scenario.scenario_name == ScenarioName.data))
        if scenario is not None:
            raise ValidationError('Please use a unique Scenario Name.')
        
    Submit = SubmitField('Run')