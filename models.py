from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Crear la clase base declarativa
Base = declarative_base()


class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    num_match = Column(Integer)
    day_match = Column(Integer)
    team_id = Column(Integer, ForeignKey('teams.id'))
    bonus_defence = Column(Float)
    bonus_midfielder = Column(Float)
    bonus_forward = Column(Float)
    team = relationship('Team', foreign_keys=[team_id],
                        back_populates='team')
    team_score = Column(Integer)
    season = Column(Integer)


class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    defence = Column(Float)
    midfielder = Column(Float)
    forward = Column(Float)
    # Define relación uno a muchos con partidos donde el equipo es local
    team = relationship('Match', back_populates='team')
