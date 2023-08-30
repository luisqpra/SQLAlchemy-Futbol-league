'''
from models import Team, Match
from config import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Operación CRUD - Crear un equipo
new_team = Team(name="New Team", defence=5, midfielder=7, forward=8)
session.add(new_team)
session.commit()

# Operación CRUD - Leer todos los equipos
teams = session.query(Team).all()
for team in teams:
    print("ID:", team.id, "- Name:", team.name)

# Operación CRUD - Actualizar un equipo
team_to_update = session.query(Team).filter_by(name="New Team").first()
if team_to_update:
    team_to_update.forward = 9
    session.commit()

# Operación CRUD - Borrar un equipo
team_to_delete = session.query(Team).filter_by(name="New Team").first()
if team_to_delete:
    session.delete(team_to_delete)
    session.commit()

# Operación CRUD - Crear un partido
new_match = Match(num_match=1, day_match=1, team_id=1, team_score=2)
session.add(new_match)
session.commit()

# Operación CRUD - Leer todos los partidos
matches = session.query(Match).all()
for match in matches:
    print("ID:", match.id, "- Match:", match.num_match, "- Team ID:", match.team_id, "- Team Score:", match.team_score)

# Leer un partido por ID
match_to_read = session.query(Match).filter_by(id=1).first()
if match_to_read:
    print("ID:", match_to_read.id, "- Match:", match_to_read.num_match,
          "- Team ID:", match_to_read.team_id, "- Team Score:", match_to_read.team_score)

# Actualizar un partido por ID
match_to_update = session.query(Match).filter_by(id=1).first()
if match_to_update:
    match_to_update.team_score = 3
    session.commit()
    print("Partido actualizado:", match_to_update.id, "- Nuevo puntaje:", match_to_update.team_score)

# Borrar un partido por ID
match_to_delete = session.query(Match).filter_by(id=2).first()
if match_to_delete:
    session.delete(match_to_delete)
    session.commit()
    print("Partido eliminado:", match_to_delete.id)
    
session.close()
'''
