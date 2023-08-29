'''
from models import Team, Match
from config import session

# Operación CRUD - Crear un equipo
new_team = Team(name="New Team", ataque=7, creacion=5, defensa=6)
session.add(new_team)
session.commit()

# Operación CRUD - Leer todos los equipos
teams = session.query(Team).all()
for team in teams:
    print(team.id, team.name, team.forward, team.midfielder,
          team.defence)

# Operación CRUD - Actualizar un equipo
team_to_update = session.query(Team).filter_by(name="New Team").first()
team_to_update.ataque = 8
session.commit()

# Operación CRUD - Borrar un equipo
team_to_delete = session.query(Team).filter_by(name="New Team").first()
session.delete(team_to_delete)
session.commit()

# Operación CRUD - Crear un partido
new_match = Match(home_team_id=1, away_team_id=2, goles_equipo_local=2,
                  goles_equipo_visitante=1)
session.add(new_match)
session.commit()

# Operación CRUD - Leer todos los partidos
matches = session.query(Match).all()
for match in matches:
    print(match.id, match.home_team_id, match.away_team_id,
          match.home_team_score, match.away_team_score)

# Actualizar un equipo por ID
team_to_update = session.query(Team).filter_by(id=1).first()
if team_to_update:
    team_to_update.ataque = 9
    session.commit()
    print("Equipo actualizado:", team_to_update.id, team_to_update.name,
          team_to_update.forward)

# Borrar un equipo por ID
team_to_delete = session.query(Team).filter_by(id=2).first()
if team_to_delete:
    session.delete(team_to_delete)
    session.commit()
    print("Equipo eliminado:", team_to_delete.id, team_to_delete.name)

session.close()
'''
