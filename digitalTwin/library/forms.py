''' Forms to enable user submitted information to flask. Default method for selecting options'''

from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, SelectField, SelectMultipleField, IntegerField, DecimalField, HiddenField, TextAreaField, DateField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from digitalTwin import db
from digitalTwin.models import models
from . import dataManager, populations 
import sqlalchemy as sa
import string, datetime




class CreateScenarioForm(FlaskForm):
    Name = StringField('Scenario Name', validators=[DataRequired(), Length(1,32)])
    # Days = IntegerField('Days', validators=[DataRequired(), NumberRange(1, 9125)] )
    # TODO: change to start date, finish date
    City = SelectField('City', choices = ["newcastle",
                                         "sunderland"],
                                                validators=[DataRequired()])
    Technology = SelectField('Technology', choices = ["Heat pumps"],
                                                validators=[DataRequired()])
    
    Description = TextAreaField('Description', [Length(min=0, max=200)])
    StartDay = DateField('Start Date', 
                         format='%Y-%m-%d', 
                         default=datetime.date.today, 
                         validators=[DataRequired()],
                         render_kw={"type": "date"})
    EndDay = DateField('End Date', 
                         format='%Y-%m-%d', 
                         default=datetime.date.today() + datetime.timedelta(days=1) , 
                         validators=[DataRequired()],
                         render_kw={"type": "date"})
    SimStep = RadioField('Step size (hrs)',
                         choices = [1, 2, 4, 12, 24],
                         default = 1,
                         validators = [DataRequired()] )
    RecordEvery = RadioField('Record every (hrs)',
                         choices = [1, 2, 4, 12, 24],
                         default= 1,
                         validators = [DataRequired()] )

    def validate_Name(self, Name):
        # check valid characters (needs to work in a url)
        valid_chars = list(string.ascii_letters) + list(string.digits) + ['-', '_']
        for s in str(Name.data):
            if s not in valid_chars:
                raise ValidationError('Please only use alphanumeric characters, hyphens or underscores (a-z, A-Z, 0-9, -, _).')
        # check uniqueness
        scenario = db.session.scalar(sa.select(models.Scenario).where(
            models.Scenario.scenario_name == Name.data))
        if scenario is not None:
            raise ValidationError('This scenario name is already in use. Please use a unique value.')

            # TODO: check EndDay after StartDay, check both within range
        
                
    Submit = SubmitField('Continue')

class PopulationModelForm(FlaskForm):
    Wards = SelectMultipleField('Wards',
                                choices = [])
    PropertyTypes = SelectMultipleField('Property Types',
                                        choices = [],
                                        validators=[DataRequired()])
    Subset = IntegerField('Subset (%)', 
                          default = 100,
                          validators=[DataRequired(), NumberRange(0,100)])
    IncomeTypes = SelectMultipleField('Income',
                                        choices =['lowest quintile',
                                                  'second lowest quintile',
                                                  'median quintile',
                                                  'second highest quintile',
                                                  'highest quintile'],
                                        validators=[DataRequired()])
    ScheduleTypes = SelectMultipleField('Schedule',
                                        choices =['dual earner',
                                                  'family with children',
                                                  'retired household',
                                                  'single parent with children',
                                                  'student',
                                                  'unemployed_or_inactive',
                                                  'working adult'],
                                            validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # populate wards
        wards = populations.wardNames('newcastle')
        self.Wards.choices = [(ward, ward) for ward in wards if ward]

        # populate Property types
        propertyTypes = populations.propertyTypes('newcastle')
        self.PropertyTypes.choices = [(ptype, ptype) for ptype in propertyTypes if ptype]

    View = SubmitField('Select')            
    Submit = SubmitField('Continue')

class ClimateModelForm(FlaskForm):
    Name = StringField('Model Name', validators=[DataRequired(), Length(1,32)])
    BaseData = SelectField('Base Data', choices = ["ncc_2t_timeseries"
                                                        ],
                                                        validators=[DataRequired()])
    TemperatureVar = SelectField('Temperature Variation', choices = ["base", "add", "subtract", "extreme"
                                                        ],
                                                        validators=[DataRequired()])
    
    temp_scale = FloatField('Temperature Variation amount', validators=[DataRequired(), NumberRange(0.0, 5.0)])
     
    def validate_Name(self, Name):
        # check valid characters (needs to work in a url)
        valid_chars = list(string.ascii_letters) + list(string.digits) + ['-', '_']
        for s in str(Name.data):
            if s not in valid_chars:
                raise ValidationError('Please only use alphanumeric characters, hyphens or underscores (a-z, A-Z, 0-9, -, _).')
        # check uniqueness
        ClimateModel = db.session.scalar(sa.select(models.ClimateModel).where(
            models.ClimateModel.model_name == Name.data))
        if ClimateModel is not None:
            raise ValidationError('This scenario name is already in use. Please use a unique value.') 
                
    Submit = SubmitField('Save')

class SelectPresetsClimate(FlaskForm):
    selected_climate_id = QuerySelectField(
        'Base Data',
        query_factory=lambda: dataManager.findDBData('ClimateModel'), 
        get_label='model_name' 
    )
    View = SubmitField('Select')
    Submit = SubmitField('Select')

class SelectPresetsPolicy(FlaskForm):
    selected_policy_id = QuerySelectField(
        'Base Data',
        query_factory=lambda: dataManager.findDBData('PolicyChoices'), 
        get_label='policy_name' 
    )
    View = SubmitField('View')
    Submit = SubmitField('Select')

class PolicyChoicesForm(FlaskForm):
    Name = StringField('Model Name', validators=[DataRequired(), Length(1,32)])
    Description = TextAreaField('Description', [Length(min=0, max=45)])
    AdoptionRate = IntegerField('Adoption Rate (%)', 
                          default = 100,
                          validators = [DataRequired(), NumberRange(0,100)],
                          description = 'Percentage of eligible agents who will adopt the technology')
    CandidateClasses = SelectMultipleField('Candidates',
                            choices =['priority',
                                    'possible',
                                    'difficult',
                                    'non-possible'],
                            default = ['priority','possible'],
                            validators = [DataRequired()],
                            description = 'Candidates for converting to heat pumps')

    def validate_Name(self, Name):
        # check valid characters (needs to work in a url)
        valid_chars = list(string.ascii_letters) + list(string.digits) + ['-', '_']
        for s in str(Name.data):
            if s not in valid_chars:
                raise ValidationError('Please only use alphanumeric characters, hyphens or underscores (a-z, A-Z, 0-9, -, _).')
        # check uniqueness
        PolicyChoice = db.session.scalar(sa.select(models.PolicyChoices).where(
            models.PolicyChoices.policy_name == Name.data))
        if PolicyChoice is not None:
            raise ValidationError('This scenario name is already in use. Please use a unique value.') 
        
    Submit = SubmitField('Submit')

class PolicyChoicesForm(FlaskForm):
    Name = StringField('Policy Name', validators=[DataRequired(), Length(1,32)])
    Description = TextAreaField('Description', [Length(min=0, max=45)])
    AdoptionRate = IntegerField('Adoption Rate (%)', 
                          default = 100,
                          validators = [DataRequired(), NumberRange(0,100)],
                          description = 'Percentage of eligible agents who will adopt the technology')
    CandidateClasses = SelectMultipleField('Candidates',
                            choices =['priority',
                                    'possible',
                                    'difficult',
                                    'non-possible'],
                            default = ['priority','possible'],
                            validators = [DataRequired()],
                            description = 'Candidates for converting to heat pumps')

    def validate_Name(self, Name):
        valid_chars = list(string.ascii_letters) + list(string.digits) + ['-', '_']
        for s in str(Name.data):
            if s not in valid_chars:
                raise ValidationError('Please only use alphanumeric characters, hyphens or underscores (a-z, A-Z, 0-9, -, _).')
        
        PolicyChoice = db.session.scalar(sa.select(models.PolicyChoices).where(
            models.PolicyChoices.policy_name == Name.data))
        if PolicyChoice is not None:
            raise ValidationError('This scenario name is already in use. Please use a unique value.') 
        
    Submit = SubmitField('Submit')
    
class PolicyRulesForm(FlaskForm):
    QualifyingCharacteristics = SelectMultipleField('Qualifying',
                                                    choices =['Ward',
                                                            'Income',
                                                            'Schedule',
                                                            'Tenure'
                                                            ],
                                                    description = 'Agents must meet at least one qualifying characteristic'                                                    
                                                )
        
    DisqualifyingCharacteristics = SelectMultipleField('Disqualifying',
                                                    choices =['Ward',
                                                            'Income',
                                                            'Schedule',
                                                            'Tenure'
                                                            ],
                                                    description = 'Agents must not meet any disqualifying characteristic'
                                                )
    
    Wards = SelectMultipleField('Wards',
                                choices = [])
    IncomeTypes = SelectMultipleField('Income',
                                        choices =['lowest quintile',
                                                  'second lowest quintile',
                                                  'median quintile',
                                                  'second highest quintile',
                                                  'highest quintile'])
    ScheduleTypes = SelectMultipleField('Schedule',
                                        choices =['dual earner',
                                                  'family with children',
                                                  'retired household',
                                                  'single parent with children',
                                                  'student',
                                                  'unemployed_or_inactive',
                                                  'working adult'])
    TenureTypes = SelectMultipleField('Tenure',
                            choices =['owner_occupied',
                                    'private_rent',
                                    'social_rent'],
                            default = ['owner_occupied',
                                    'private_rent',
                                    'social_rent'])
    
    Submit = SubmitField('Add to policy selection')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        wards = populations.wardNames('newcastle')
        self.Wards.choices = [(ward, ward) for ward in wards if ward]

    def validate(self, extra_validators=None):
        
        if not super().validate(extra_validators=extra_validators):
            return False

        selected_triggers = set()
        for field in [self.QualifyingCharacteristics, self.DisqualifyingCharacteristics]:
            if field.data:
                selected_triggers.update(field.data)

        if not selected_triggers:
            self.QualifyingCharacteristics.errors.append(
                'You must select at least one option from within Qualifying, Required, or Disqualifying.'
            )
            return False

        field_map = {
            'Ward':     self.Wards,
            'Income':   self.IncomeTypes,
            'Tenure': self.TenureTypes,
            'Schedule': self.ScheduleTypes
        }

        validation_passed = True
        
        for trigger in selected_triggers:
            target_field = field_map.get(trigger)

            if target_field and not target_field.data:
                target_field.errors.append(
                    f"You selected '{trigger}' as a characteristic, so you must select at least one option here."
                )
                validation_passed = False

        return validation_passed

class SubmitForm(FlaskForm):
    Save = SubmitField('Save')
    Run = SubmitField('Run')