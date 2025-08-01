from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class CreateScenarioForm(FlaskForm):
    ScenarioName = StringField('Scenario Name', validators=[DataRequired(), Length(1,32)])
    Days = DecimalField('Days', places=0, validators=[DataRequired(), NumberRange(1, 9125)] )
    DataSource = SelectField('Data Source', choices = ["ncc_neighborhood.geojson"],validators=[DataRequired()])
    Submit = SubmitField('Run')