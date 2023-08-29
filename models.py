from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Crear la clase base declarativa
Base = declarative_base()


class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    home_team_id = Column(Integer, ForeignKey('teams.id'))
    away_team_id = Column(Integer, ForeignKey('teams.id'))
    home_team = relationship('Team', foreign_keys=[home_team_id],
                             back_populates='home_matches')
    away_team = relationship('Team', foreign_keys=[away_team_id],
                             back_populates='away_matches')
    home_team_score = Column(Integer)
    away_team_score = Column(Integer)


class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    defence = Column(Integer)
    midfielder = Column(Integer)
    forward = Column(Integer)
    # Define relación uno a muchos con partidos donde el equipo es local
    home_matches = relationship('Match', back_populates='home_team')
    # Define relación uno a muchos con partidos donde el equipo es visitante
    away_matches = relationship('Match', back_populates='away_team')
