"""Database models. For the other kinds of models (MABM, climate models etc) look in /modelling."""
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from digitalTwin import db

class Scenario(db.Model):
    __tablename__ = "scenario"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    scenario_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    days: so.Mapped[int] = so.mapped_column()
    data_source: so.Mapped[str] = so.mapped_column(sa.String(64))
    user_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    agent_time_series: so.WriteOnlyMapped[Optional['AgentTimeSeries']] = so.relationship(
        back_populates='scenario')
    energy_time_series: so.WriteOnlyMapped[Optional['EnergyTimeSeries']] = so.relationship(
        back_populates='scenario')
    model_time_series: so.WriteOnlyMapped[Optional['ModelTimeSeries']] = so.relationship(
        back_populates='scenario')

    def __repr__(self):
        return '<scenario {}>'.format(self.scenario_name)

class AgentTimeSeries(db.Model):
    __tablename__ = "agent_time_series"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    scenario_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Scenario.id),
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
    scenario_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Scenario.id),
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
    scenario_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Scenario.id),
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