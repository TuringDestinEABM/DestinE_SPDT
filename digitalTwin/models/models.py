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

    results: so.WriteOnlyMapped[Optional['Result']] = so.relationship(
        back_populates='scenario')

    def __repr__(self):
        return '<scenario {}>'.format(self.username)
    
class Result(db.Model):
    __tablename__ = "result"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # agent_ts: so.Mapped[str] = 
    # energy_ts: so.Mapped[str] = 
    # model_ts: so.Mapped[str] = 

    scenario_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Scenario.id),
                                               index=True)

    scenario: so.Mapped[Scenario] = so.relationship(back_populates='results')

    def __repr__(self):
        return '<Post {}>'.format(self.body)