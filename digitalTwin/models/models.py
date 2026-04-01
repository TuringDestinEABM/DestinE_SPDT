"""Database models. For the other kinds of models (MABM, climate models etc) look in /modelling."""
from datetime import datetime, timezone
from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.mutable import MutableList
from digitalTwin import db

class Scenario(db.Model):
    __tablename__ = "scenario"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    scenario_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column()
    days: so.Mapped[int] = so.mapped_column()
    city: so.Mapped[str] = so.mapped_column(sa.String(64))
    subset: so.Mapped[int] = so.mapped_column()
    user_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    init_lat: so.Mapped[int] = so.mapped_column()
    init_lon: so.Mapped[int] = so.mapped_column()
    start_day: so.Mapped[datetime] = so.mapped_column()
    simulation_step: so.Mapped[int] = so.mapped_column()
    record_every: so.Mapped[int] = so.mapped_column()
    climate_model_id: so.Mapped[Optional[int]] = so.mapped_column()
    policy_id: so.Mapped[Optional[int]] = so.mapped_column()
    population_id: so.Mapped[Optional[int]] = so.mapped_column()

    agent_time_series: so.WriteOnlyMapped[Optional['AgentTimeSeries']] = so.relationship(
        back_populates="scenario", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    energy_time_series: so.WriteOnlyMapped[Optional['EnergyTimeSeries']] = so.relationship(
        back_populates="scenario", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    model_time_series: so.WriteOnlyMapped[Optional['ModelTimeSeries']] = so.relationship(
        back_populates="scenario", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return '<scenario {}>'.format(self.scenario_name)

class AgentTimeSeries(db.Model):
    __tablename__ = "agent_time_series"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    scenario_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Scenario.id, ondelete="CASCADE"), 
        index=True)
    scenario: so.Mapped[Scenario] = so.relationship(back_populates='agent_time_series')
    energy: so.Mapped[int] = so.mapped_column()
    energy_consumption: so.Mapped[int] = so.mapped_column()
    step: so.Mapped[int] = so.mapped_column()
    Agent_id: so.Mapped[int] = so.mapped_column()

    def __repr__(self):
        return '<agent_ts {}>'.format(self.id)  

class EnergyTimeSeries(db.Model):
    __tablename__ = "energy_time_series"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    scenario_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Scenario.id, ondelete="CASCADE"), 
        index=True)
    scenario: so.Mapped[Scenario] = so.relationship(back_populates='energy_time_series')
    step: so.Mapped[int] = so.mapped_column()
    hour: so.Mapped[int] = so.mapped_column()
    day: so.Mapped[int] = so.mapped_column()
    total_energy: so.Mapped[int] = so.mapped_column()
    average_energy: so.Mapped[int] = so.mapped_column()

    def __repr__(self):
        return '<energy_ts {}>'.format(self.id)
    
    
class ModelTimeSeries(db.Model):
    __tablename__ = "model_time_series"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # scenario_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Scenario.id),
    #                                            index=True)
    scenario_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Scenario.id, ondelete="CASCADE"), 
        index=True)
    scenario: so.Mapped[Scenario] = so.relationship(back_populates='model_time_series')
    mid_terraced_house: so.Mapped[float] = so.mapped_column()
    semi_detached_house: so.Mapped[float] = so.mapped_column()
    flats_small: so.Mapped[float] = so.mapped_column()
    flats_large: so.Mapped[float] = so.mapped_column()
    flats_block: so.Mapped[float] = so.mapped_column()
    end_terrace_house: so.Mapped[float] = so.mapped_column()
    detached_house: so.Mapped[float] = so.mapped_column()
    flat_mixed_use: so.Mapped[float] = so.mapped_column()
    high: so.Mapped[float] = so.mapped_column()
    medium: so.Mapped[float] = so.mapped_column()
    low: so.Mapped[float] = so.mapped_column()
    total_energy: so.Mapped[float] = so.mapped_column()
    cumulative_energy: so.Mapped[float] = so.mapped_column()

    def __repr__(self):
        return '<model_ts {}>'.format(self.id)
    

class EPCABMdata(db.Model):
    # __bind_key__ = "gis"
    __tablename__ = "epc_abm_data"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    city: so.Mapped[str] = so.mapped_column()
    UPRN: so.Mapped[int] = so.mapped_column()
    lsoa_code: so.Mapped[str] = so.mapped_column()
    local_authority: so.Mapped[str] = so.mapped_column()
    ward_code: so.Mapped[str] = so.mapped_column()
    habitable_rooms: so.Mapped[Optional[int]] = so.mapped_column()
    sap_rating: so.Mapped[int] = so.mapped_column()
    floor_area_m2: so.Mapped[float] = so.mapped_column()
    property_type: so.Mapped[str] = so.mapped_column()
    property_age: so.Mapped[str] = so.mapped_column()
    main_fuel_type: so.Mapped[Optional[str]] = so.mapped_column()
    main_heating_system: so.Mapped[str] = so.mapped_column()
    sap_band_ord: so.Mapped[int] = so.mapped_column()
    retrofit_envelope_score: so.Mapped[float] = so.mapped_column()
    is_off_gas: so.Mapped[Optional[bool]] = so.mapped_column()
    energy_demand_kwh: so.Mapped[float] = so.mapped_column()
    factor: so.Mapped[float] = so.mapped_column()
    energy_cal_kwh: so.Mapped[float] = so.mapped_column()
    is_heatpump_candidate: so.Mapped[bool] = so.mapped_column()
    heatpump_candidate_class: so.Mapped[bool] = so.mapped_column()
    heating_controls: so.Mapped[Optional[str]] = so.mapped_column()
    meter_type: so.Mapped[str] = so.mapped_column()
    cwi_flag: so.Mapped[bool] = so.mapped_column()
    swi_flag: so.Mapped[bool] = so.mapped_column()
    loft_ins_flag: so.Mapped[bool] = so.mapped_column()
    floor_ins_flag: so.Mapped[bool] = so.mapped_column()
    glazing_flag: so.Mapped[bool] = so.mapped_column()
    is_electric_heating: so.Mapped[Optional[bool]] = so.mapped_column()
    is_gas: so.Mapped[Optional[bool]] = so.mapped_column()
    is_oil: so.Mapped[Optional[bool]] = so.mapped_column()
    is_solid_fuel: so.Mapped[Optional[bool]] = so.mapped_column()
    epc_lodgement_date_year: so.Mapped[int] = so.mapped_column()
    geometry_type: so.Mapped[str] = so.mapped_column()
    geometry_coordinates_lat: so.Mapped[float] = so.mapped_column()
    geometry_coordinates_lon: so.Mapped[float] = so.mapped_column()

    def __repr__(self):
        return '<epc_abm_data {}>'.format(self.id)    
    
class UPRNdata(db.Model):
    # __bind_key__ = "gis"
    __tablename__ = "uprn_data"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    city: so.Mapped[str] = so.mapped_column()
    UPRN: so.Mapped[int] = so.mapped_column()
    lsoa_code: so.Mapped[str] = so.mapped_column()
    dwelling_bucket: so.Mapped[Optional[str]] = so.mapped_column()
    tenure: so.Mapped[Optional[str]] = so.mapped_column()
    size_band: so.Mapped[Optional[int]] = so.mapped_column()
    hidp: so.Mapped[Optional[int]] = so.mapped_column()
    hh_n_people: so.Mapped[Optional[int]] = so.mapped_column()
    hh_children: so.Mapped[Optional[bool]] = so.mapped_column()
    hh_income: so.Mapped[Optional[float]] = so.mapped_column()
    hh_income_band: so.Mapped[Optional[str]] = so.mapped_column()
    schedule_type: so.Mapped[Optional[str]] = so.mapped_column()
    hh_edu_detail: so.Mapped[Optional[str]] = so.mapped_column()
   
    def __repr__(self):
        return '<uprn_data {}>'.format(self.id)    
    
class ClimateModel(db.Model):
    __tablename__ = "climate_model"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    model_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    user_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    base_data: so.Mapped[str] = so.mapped_column()
    temp_var_Type: so.Mapped[str] = so.mapped_column()
    # temp_var_vals: so.Mapped[List[int]] = so.mapped_column(MutableList.as_mutable(sa.PickleType))
    temp_scale: so.Mapped[Optional[float]] = so.mapped_column()
    
    def __repr__(self):
        return '<climate_model {}>'.format(self.id)    

class Population(db.Model):
    __tablename__ = "population"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    wards: so.Mapped[Optional[List[str]]] = so.mapped_column(MutableList.as_mutable(sa.JSON)) 
    property_types: so.Mapped[Optional[List[str]]] = so.mapped_column(MutableList.as_mutable(sa.JSON)) 
    income_types: so.Mapped[Optional[List[str]]] = so.mapped_column(MutableList.as_mutable(sa.JSON))
    schedule_types: so.Mapped[Optional[List[str]]] = so.mapped_column(MutableList.as_mutable(sa.JSON))  

    def __repr__(self):
        return '<population {}>'.format(self.id)    
   

    def __repr__(self):
        return '<population {}>'.format(self.id)        

class PolicyChoices(db.Model):
    __tablename__ = "policy_choices"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    policy_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column()
    user_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    rules: so.Mapped[List['Rules']] = so.relationship(
        back_populates="policy_choice", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    adoption_rate: so.Mapped[int] = so.mapped_column()
    candidate_classes: so.Mapped[Optional[List[str]]] = so.mapped_column(MutableList.as_mutable(sa.JSON))

    def __repr__(self):
        return '<policy_choices {}>'.format(self.id)    

class Rules(db.Model):
    __tablename__ = "rules"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    policy_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("policy_choices.id", ondelete="CASCADE"), 
        index=True
    )
    policy_choice: so.Mapped['PolicyChoices'] = so.relationship(
        back_populates="rules"
    )
    qualifying_characteristics: so.Mapped[Optional[List[str]]] = so.mapped_column(MutableList.as_mutable(sa.JSON))
    disqualifying_characteristics: so.Mapped[Optional[List[str]]] = so.mapped_column(MutableList.as_mutable(sa.JSON))
    wards: so.Mapped[Optional[List[str]]] = so.mapped_column(MutableList.as_mutable(sa.JSON)) 
    tenure_types: so.Mapped[Optional[List[str]]] = so.mapped_column(MutableList.as_mutable(sa.JSON)) 
    income_types: so.Mapped[Optional[List[str]]] = so.mapped_column(MutableList.as_mutable(sa.JSON))
    schedule_types: so.Mapped[Optional[List[str]]] = so.mapped_column(MutableList.as_mutable(sa.JSON))

    def __repr__(self):
    # Required fields
        parts = [
            f"id={self.id}",
            f"policy_id={self.policy_id}"
        ]

        optional_fields = [
            "qualifying_characteristics",
            "disqualifying_characteristics",
            "wards",
            "tenure_types",
            "income_types",
            "schedule_types",
        ]

    # Append any optional fields which exist
        for field in optional_fields:
            value = getattr(self, field)
            if value is not None:
                parts.append(f"{field}={value}")

        return f"<Rules({', '.join(parts)})>"