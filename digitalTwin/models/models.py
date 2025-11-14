"""Database models. For the other kinds of models (MABM, climate models etc) look in /modelling."""

from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Scenario(db.Model):
    __tablename__ = "scenario"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    scenario_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,unique=True)
    days: so.Mapped[int] = so.mapped_column(sa.Int(120))
    data_source: so.Mapped[str] = so.mapped_column(sa.String(64))
    job_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    user_name: so.Mapped[str] = so.mapped_column(sa.String(64))

    def __repr__(self):
        return '<scenario {}>'.format(self.username)